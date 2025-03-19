import time
from collections.abc import Sequence
from copy import copy
from typing import TYPE_CHECKING
from typing import Any
from typing import Union

import amsdal_glue as glue
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.data_models.enums import BaseClasses
from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.data_models.reference import ReferenceData
from amsdal_utils.models.enums import ModuleType
from amsdal_utils.models.enums import Versions
from amsdal_utils.models.utils.reference_builders import build_reference
from amsdal_utils.utils.identifier import get_identifier

from amsdal_data.connections.constants import METADATA_KEY
from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_ID
from amsdal_data.connections.constants import OBJECT_VERSION
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.data_mutation_transform.base import BaseDataMutationTransform
from amsdal_data.connections.historical.data_query_transform import DEFAULT_PKS
from amsdal_data.connections.historical.data_query_transform import META_CLASS_NAME
from amsdal_data.connections.historical.data_query_transform import META_FOREIGN_KEYS
from amsdal_data.connections.historical.data_query_transform import META_PRIMARY_KEY_FIELDS
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.connections.historical.data_query_transform import PK_FIELD_ALIAS_FOR_METADATA
from amsdal_data.connections.historical.data_query_transform import build_simple_query_statement_with_metadata
from amsdal_data.connections.historical.metadata_query import build_metadata_query
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.connections.historical.table_name_transform import TableNameTransform
from amsdal_data.errors import MetadataInfoQueryError
from amsdal_data.transactions.manager import AmsdalTransactionManager

if TYPE_CHECKING:
    from amsdal_data.connections.postgresql_historical import PostgresHistoricalConnection
    from amsdal_data.connections.sqlite_historical import SqliteHistoricalConnection


class DataMutationTransform(BaseDataMutationTransform):
    def __init__(
        self,
        connection: Union['SqliteHistoricalConnection', 'PostgresHistoricalConnection'],
        mutation: DataMutation,
    ) -> None:
        self.connection = connection
        self.mutation = copy(mutation)
        self._data: list[glue.Data] | None = None

    @property
    def is_internal_tables(self) -> bool:
        return self.mutation.schema.name in (METADATA_TABLE, REFERENCE_TABLE, TRANSACTION_TABLE)

    @property
    def data(self) -> list[glue.Data] | None:
        return self._data

    def transform(self) -> Sequence[DataMutation]:
        if self.is_internal_tables:
            return [self.mutation]

        if isinstance(self.mutation, glue.InsertData):
            return self._transform_insert_data(self.mutation)
        if isinstance(self.mutation, glue.UpdateData):
            return self._transform_update_data(self.mutation)
        if isinstance(self.mutation, glue.DeleteData):
            return self._transform_delete_data(self.mutation)

        msg = f'Unsupported mutation type: {type(self.mutation)}'
        raise ValueError(msg)

    def _transform_insert_data(self, mutation: glue.InsertData) -> Sequence[DataMutation]:
        self._process_foreign_keys(mutation.data)
        self._process_data(mutation.schema, mutation.data, action=glue.InsertData)
        self._data = mutation.data

        return self._build_insert_mutations(mutation.schema, mutation.data)

    def _transform_update_data(self, mutation: glue.UpdateData) -> Sequence[DataMutation]:
        # AMSDAL ORM always put whole object in update mutation
        self._process_foreign_keys([mutation.data])
        self._process_data(mutation.schema, [mutation.data], action=glue.UpdateData)
        self._data = [mutation.data]

        return self._build_insert_mutations(mutation.schema, [mutation.data])

    def _transform_delete_data(self, mutation: glue.DeleteData) -> Sequence[DataMutation]:
        query = self._process_foreign_keys_for_conditions(mutation.schema.metadata, mutation.query)
        _next_version_field = glue.FieldReference(
            field=glue.Field(name=NEXT_VERSION_FIELD),
            table_name=METADATA_TABLE_ALIAS,
        )
        if query:
            query = query & glue.Conditions(
                glue.Condition(
                    left=glue.FieldReferenceExpression(field_reference=_next_version_field),
                    lookup=glue.FieldLookup.ISNULL,
                    right=glue.Value(value=True),
                ),
                glue.Condition(
                    left=glue.FieldReferenceExpression(field_reference=_next_version_field),
                    lookup=glue.FieldLookup.EQ,
                    right=glue.Value(value=''),
                ),
                connector=glue.FilterConnector.OR,
            )

        stored_items = self.connection.query(
            build_simple_query_statement_with_metadata(
                table=mutation.schema,
                where=query,
            ),
        )

        # TODO: possible OOM, need to implement pagination
        for item in stored_items:
            item.data.pop(SECONDARY_PARTITION_KEY)
            item.data = {key: val for key, val in item.data.items() if not key.startswith(PK_FIELD_ALIAS_FOR_METADATA)}
            item.metadata = mutation.schema.metadata

        self._process_data(mutation.schema, stored_items, action=glue.DeleteData)
        self._data = stored_items

        return self._build_insert_mutations(mutation.schema, stored_items)

    def _process_data(
        self,
        schema_reference: glue.SchemaReference,
        data: list[glue.Data],
        action: type[glue.InsertData | glue.UpdateData | glue.DeleteData],
    ) -> None:
        for _data in data:
            _object_version, _prior_version = self._resolve_object_versions(schema_reference, _data, action=action)
            _metadata = self.build_metadata(
                schema_reference,
                _data,
                _object_version,
                _prior_version,
                action=action,
            )
            _data.data[METADATA_KEY] = _metadata.model_dump()
            _data.data[SECONDARY_PARTITION_KEY] = _metadata.object_version

    def _resolve_object_versions(
        self,
        schema_reference: glue.SchemaReference,
        glue_data: glue.Data,
        action: type[glue.InsertData | glue.UpdateData | glue.DeleteData],
    ) -> tuple[str, str | None]:
        prior_version = None
        _meta = schema_reference.metadata or {}
        class_name = _meta.get(META_CLASS_NAME) or schema_reference.name

        if action is glue.UpdateData and METADATA_KEY not in glue_data.data:
            pks = (glue_data.metadata or {}).get(META_PRIMARY_KEY_FIELDS, {}) or DEFAULT_PKS
            glue_data.data[METADATA_KEY] = self._fetch_metadata(
                [glue_data.data[_pk] for _pk in pks],
                class_name=class_name,
                is_class_meta=schema_reference.name == BaseClasses.CLASS_OBJECT_META,
            ).model_dump()

        if action in (glue.DeleteData, glue.UpdateData):
            # for deleting we always fetch data from the lakehouse, see _transform_delete_data method
            prior_version = glue_data.data[METADATA_KEY][OBJECT_VERSION]

        schema_version_manager = HistoricalSchemaVersionManager()

        # usually SECONDARY_PARTITION_KEY is not present in the data. It presents only if we need to store
        # the specific version of the object. In all other cases, we always generate a new version.
        object_version = glue_data.data.get(SECONDARY_PARTITION_KEY, glue.Version.LATEST)

        # try to resolve from SchemaVersionManager in case if data represents the schema object
        if schema_reference.name in (BaseClasses.OBJECT.value, BaseClasses.CLASS_OBJECT.value):
            if object_version in (glue.Version.LATEST, Versions.LATEST):
                object_version = schema_version_manager.get_latest_schema_version(
                    glue_data.data.get('table_name') or glue_data.data[PRIMARY_PARTITION_KEY],
                    from_cache_only=True,
                )

        # if we still have Versions.LATEST, then we need to generate a new version
        if object_version in (glue.Version.LATEST, Versions.LATEST):
            object_version = get_identifier()

        return object_version, prior_version

    def _fetch_metadata(self, object_id: list[Any], class_name: str, *, is_class_meta: bool) -> Metadata:
        query = build_metadata_query(object_id, class_name, is_class_meta=is_class_meta)
        data = self.connection.query(query)

        if not data:
            msg = f'Metadata not found for object_id: {object_id}. Query: {query}'
            raise MetadataInfoQueryError(msg)

        return Metadata(**data[0].data)

    @staticmethod
    def build_metadata(
        schema_reference: glue.SchemaReference,
        glue_data: glue.Data,
        object_version: str,
        prior_version: str | None,
        action: type[glue.InsertData | glue.UpdateData | glue.DeleteData],
    ) -> Metadata:
        if action in (glue.UpdateData, glue.DeleteData):
            _metadata = Metadata(**glue_data.data[METADATA_KEY])
            _metadata.object_version = object_version
            _metadata.prior_version = prior_version
            _metadata.updated_at = round(time.time() * 1000)

            transaction_ref = None
            if _transaction := AmsdalTransactionManager().transaction_object:
                transaction_ref = Reference(ref=ReferenceData(**_transaction.address.model_dump()))

            _metadata.transaction = transaction_ref

            if action is glue.DeleteData:
                _metadata.is_deleted = True
            elif action is glue.UpdateData:
                # updating deleted object leads to undelete it
                _metadata.is_deleted = False

            return _metadata

        schema_version_manager = HistoricalSchemaVersionManager()
        _pk_meta = (glue_data.metadata or {}).get(META_PRIMARY_KEY_FIELDS) or {PRIMARY_PARTITION_KEY: str}
        _fks_meta = (glue_data.metadata or {}).get(META_FOREIGN_KEYS) or {}
        _object_id_per_pk = {}

        for _pk in _pk_meta:
            if _pk in glue_data.data:
                _object_id_per_pk[_pk] = glue_data.data[_pk]
                continue

            for _fk, (_fk_ref, _fk_fields) in _fks_meta.items():
                if _pk in _fk_fields:
                    _object_id_per_pk[_fk] = _fk_ref.model_dump()
                    break

        object_id = list(_object_id_per_pk.values())

        class_name = (schema_reference.metadata or {}).get(META_CLASS_NAME) or schema_reference.name
        schema_type = schema_version_manager.resolve_schema_type(class_name)

        if schema_type == ModuleType.TYPE or class_name in (
            BaseClasses.OBJECT,
            BaseClasses.CLASS_OBJECT,
            BaseClasses.CLASS_OBJECT_META,
        ):
            schema_storage_class_name = BaseClasses.OBJECT.value
        else:
            schema_storage_class_name = BaseClasses.CLASS_OBJECT.value

        _class_schema_reference = build_reference(
            class_name=schema_storage_class_name,
            class_version=schema_version_manager.get_latest_schema_version(schema_storage_class_name),
            object_id=class_name,
            object_version=schema_version_manager.get_latest_schema_version(class_name),
        )

        _class_meta_schema_reference = None
        if class_name == BaseClasses.CLASS_OBJECT_META:
            _class_name = BaseClasses.CLASS_OBJECT.value
            class_version = schema_version_manager.get_latest_schema_version(_class_name)
            original_object_version = schema_version_manager.get_latest_schema_version(object_id[0])

            _class_meta_schema_reference = build_reference(
                class_name=_class_name,
                class_version=class_version,
                object_id=object_id,
                object_version=original_object_version,
            )

        transaction_ref = None
        if _transaction := AmsdalTransactionManager().transaction_object:
            transaction_ref = Reference(ref=ReferenceData(**_transaction.address.model_dump()))

        return Metadata(
            object_id=object_id,
            object_version=object_version,
            class_schema_reference=_class_schema_reference,
            class_meta_schema_reference=_class_meta_schema_reference,
            transaction=transaction_ref,
        )

    @classmethod
    def _build_insert_mutations(cls, schema: glue.SchemaReference, data: list[glue.Data]) -> Sequence[glue.InsertData]:
        TableNameTransform.process_table_name(schema)
        _mutations = []

        for _data in data:
            _pk_meta = (_data.metadata or {}).get(META_PRIMARY_KEY_FIELDS) or {PRIMARY_PARTITION_KEY: str}
            _fks_meta = (_data.metadata or {}).get(META_FOREIGN_KEYS) or {}
            _item = copy(_data.data)
            _metadata_data = _item.pop(METADATA_KEY)
            _metadata_object = Metadata(**_metadata_data)

            _object_id_per_pk = {}
            for _pk in _pk_meta:
                if _pk in _item:
                    _object_id_per_pk[_pk] = _item[_pk]
                    continue

                for _fk, (_fk_ref, _fk_fields) in _fks_meta.items():
                    if _pk in _fk_fields:
                        _object_id_per_pk[_fk] = _fk_ref.model_dump()
                        break

            _object_id = list(_object_id_per_pk.values())

            _metadata = _metadata_object.model_dump()
            _metadata[PRIMARY_PARTITION_KEY] = get_identifier()
            _metadata[OBJECT_ID] = _object_id
            _metadata[OBJECT_VERSION] = _item[SECONDARY_PARTITION_KEY]

            _inserts = [
                glue.InsertData(schema=schema, data=[glue.Data(data=_item)]),
                glue.InsertData(
                    schema=glue.SchemaReference(name=METADATA_TABLE, version=glue.Version.LATEST),
                    data=[glue.Data(data=_metadata)],
                ),
            ]
            _references: list[glue.Data] = []
            cls._generate_references(_metadata_object.address, _item, _references)

            if _references:
                _inserts.append(
                    glue.InsertData(
                        schema=glue.SchemaReference(name=REFERENCE_TABLE, version=glue.Version.LATEST),
                        data=_references,
                    ),
                )

            _mutations.extend(_inserts)

        return _mutations
