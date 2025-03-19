import amsdal_glue as glue
from _typeshed import Incomplete
from amsdal_data.connections.constants import METADATA_KEY as METADATA_KEY, METADATA_TABLE as METADATA_TABLE, OBJECT_ID as OBJECT_ID, OBJECT_VERSION as OBJECT_VERSION, PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, REFERENCE_TABLE as REFERENCE_TABLE, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY, TRANSACTION_TABLE as TRANSACTION_TABLE
from amsdal_data.connections.historical.data_mutation_transform.base import BaseDataMutationTransform as BaseDataMutationTransform
from amsdal_data.connections.historical.data_query_transform import DEFAULT_PKS as DEFAULT_PKS, METADATA_TABLE_ALIAS as METADATA_TABLE_ALIAS, META_CLASS_NAME as META_CLASS_NAME, META_FOREIGN_KEYS as META_FOREIGN_KEYS, META_PRIMARY_KEY_FIELDS as META_PRIMARY_KEY_FIELDS, NEXT_VERSION_FIELD as NEXT_VERSION_FIELD, PK_FIELD_ALIAS_FOR_METADATA as PK_FIELD_ALIAS_FOR_METADATA, build_simple_query_statement_with_metadata as build_simple_query_statement_with_metadata
from amsdal_data.connections.historical.metadata_query import build_metadata_query as build_metadata_query
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager as HistoricalSchemaVersionManager
from amsdal_data.connections.historical.table_name_transform import TableNameTransform as TableNameTransform
from amsdal_data.connections.postgresql_historical import PostgresHistoricalConnection as PostgresHistoricalConnection
from amsdal_data.connections.sqlite_historical import SqliteHistoricalConnection as SqliteHistoricalConnection
from amsdal_data.errors import MetadataInfoQueryError as MetadataInfoQueryError
from amsdal_data.transactions.manager import AmsdalTransactionManager as AmsdalTransactionManager
from amsdal_glue_core.common.operations.mutations.data import DataMutation as DataMutation
from amsdal_utils.models.data_models.metadata import Metadata
from collections.abc import Sequence
from typing import Any

class DataMutationTransform(BaseDataMutationTransform):
    connection: Incomplete
    mutation: Incomplete
    _data: list[glue.Data] | None
    def __init__(self, connection: SqliteHistoricalConnection | PostgresHistoricalConnection, mutation: DataMutation) -> None: ...
    @property
    def is_internal_tables(self) -> bool: ...
    @property
    def data(self) -> list[glue.Data] | None: ...
    def transform(self) -> Sequence[DataMutation]: ...
    def _transform_insert_data(self, mutation: glue.InsertData) -> Sequence[DataMutation]: ...
    def _transform_update_data(self, mutation: glue.UpdateData) -> Sequence[DataMutation]: ...
    def _transform_delete_data(self, mutation: glue.DeleteData) -> Sequence[DataMutation]: ...
    def _process_data(self, schema_reference: glue.SchemaReference, data: list[glue.Data], action: type[glue.InsertData | glue.UpdateData | glue.DeleteData]) -> None: ...
    def _resolve_object_versions(self, schema_reference: glue.SchemaReference, glue_data: glue.Data, action: type[glue.InsertData | glue.UpdateData | glue.DeleteData]) -> tuple[str, str | None]: ...
    def _fetch_metadata(self, object_id: list[Any], class_name: str, *, is_class_meta: bool) -> Metadata: ...
    @staticmethod
    def build_metadata(schema_reference: glue.SchemaReference, glue_data: glue.Data, object_version: str, prior_version: str | None, action: type[glue.InsertData | glue.UpdateData | glue.DeleteData]) -> Metadata: ...
    @classmethod
    def _build_insert_mutations(cls, schema: glue.SchemaReference, data: list[glue.Data]) -> Sequence[glue.InsertData]: ...
