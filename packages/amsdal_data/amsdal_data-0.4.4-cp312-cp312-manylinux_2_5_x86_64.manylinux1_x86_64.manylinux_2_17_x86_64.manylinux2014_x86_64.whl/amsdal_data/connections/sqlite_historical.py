from copy import copy

import amsdal_glue as glue
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.enums import Versions

from amsdal_data.connections.base_sqlite_historical import BaseSqliteHistoricalConnection
from amsdal_data.connections.common import get_class_name
from amsdal_data.connections.common import get_table_version
from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_TABLE
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.data_mutation_transform import DataMutationTransform
from amsdal_data.connections.historical.data_query_transform import DataQueryTransform
from amsdal_data.connections.historical.query_builder import pull_out_filter_from_query
from amsdal_data.connections.historical.query_builder import sort_items
from amsdal_data.connections.historical.query_builder import split_conditions
from amsdal_data.connections.historical.schema_command_transform import SchemaCommandExecutor
from amsdal_data.connections.historical.schema_query_filters_transform import SchemaQueryFiltersTransform
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.connections.historical.table_name_transform import TableNameTransform


class SqliteHistoricalConnection(BaseSqliteHistoricalConnection, glue.SqliteConnection):
    def __init__(self) -> None:
        super().__init__()
        self.schema_version_manager = HistoricalSchemaVersionManager()

    def query(self, query: glue.QueryStatement) -> list[glue.Data]:
        _transform = DataQueryTransform(query)
        _query = _transform.transform()

        _table_transform = TableNameTransform(_query)

        if _table_transform.table_name in (METADATA_TABLE, REFERENCE_TABLE, TRANSACTION_TABLE):
            return super().query(_table_transform.transform())

        items: list[glue.Data] = []
        queries = self._build_queries_by_version(_query)

        for _query_version in queries:
            # Historical table name
            _table_transform = TableNameTransform(_query_version)
            items.extend(super().query(_table_transform.transform()))

        if len(queries) > 1:
            items = sort_items(items, _query.order_by)
            items = self._apply_pagination(items, _query.limit)

        return items

    def query_schema(self, filters: glue.Conditions | None = None) -> list[glue.Schema]:
        _transform = SchemaQueryFiltersTransform(filters)
        _conditions = _transform.transform()

        data = super().query_schema(_conditions)

        return _transform.process_data(data)

    def _run_mutation(self, mutation: DataMutation) -> list[glue.Data] | None:
        _transform = DataMutationTransform(self, mutation)
        _mutations = _transform.transform()

        for _mutation in _mutations:
            super()._run_mutation(_mutation)

        return _transform.data

    def run_schema_command(self, command: glue.SchemaCommand) -> list[glue.Schema | None]:
        _executor = SchemaCommandExecutor(self, command)

        return _executor.execute()

    def run_schema_mutation(self, mutation: glue.SchemaMutation) -> glue.Schema | None:
        return super()._run_schema_mutation(mutation)

    def _build_queries_by_version(self, query: glue.QueryStatement) -> list[glue.QueryStatement]:
        if not query.where:
            return self._to_queries_by_version(get_table_version(query.table), query)  # type: ignore[arg-type]

        class_name = get_class_name(query.table)
        queries_by_version: dict[str, glue.QueryStatement] = {}
        field = glue.Field(name='_address', child=glue.Field(name='class_version'))
        field.child.parent = field  # type: ignore[union-attr]

        for _conditions in split_conditions(query.where):
            _class_versions, _query = pull_out_filter_from_query(_conditions, field)

            if not _class_versions:
                _class_versions = {query.table.version}  # type: ignore[union-attr]

            if _query is None:
                _query = ~glue.Conditions(
                    # TODO: It should use actual primary keys instead if PRIMARY_PARTITION_KEY
                    glue.Condition(
                        left=glue.FieldReferenceExpression(
                            field_reference=glue.FieldReference(
                                field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                table_name=query.table.name,  # type: ignore[union-attr]
                            ),
                        ),
                        lookup=glue.FieldLookup.EQ,
                        right=glue.Value('_empty-'),
                    ),
                )

            for _class_version in _class_versions:
                if _class_version in (glue.Version.ALL, Versions.ALL):
                    _versions = set()
                    for _item_version in self.schema_version_manager.get_all_schema_versions(class_name):
                        if _item_version or query.table.name in {  # type: ignore[union-attr]
                            TRANSACTION_TABLE,
                            METADATA_TABLE,
                            REFERENCE_TABLE,
                            OBJECT_TABLE,
                        }:
                            _versions.add(_item_version)
                elif _class_version in (glue.Version.LATEST, Versions.LATEST):
                    _versions = {self.schema_version_manager.get_latest_schema_version(class_name)}
                else:
                    _versions = {_class_version}

                for _specific_current_version in _versions:
                    _query_version = copy(query)
                    _query_version.table = copy(query.table)
                    _query_version.table.version = _specific_current_version  # type: ignore[union-attr]
                    _query_version.where = _query

                    if _specific_current_version not in queries_by_version:
                        queries_by_version[_specific_current_version] = _query_version
                    else:
                        _q_version = queries_by_version[_specific_current_version]

                        if _q_version.where is not None:
                            _q_version.where |= _query

        return list(queries_by_version.values())

    def _to_queries_by_version(
        self,
        version: glue.Version | Versions,
        query: glue.QueryStatement,
    ) -> list[glue.QueryStatement]:
        queries = []

        _table = query.table
        _class_name = get_class_name(_table)

        if isinstance(_table, glue.SubQueryStatement):
            return [query]

        if version in (glue.Version.ALL, Versions.ALL):
            for _class_version in self.schema_version_manager.get_all_schema_versions(_class_name):
                _query = copy(query)
                _query.table = copy(_table)
                _query.table.version = _class_version
                queries.append(_query)
        elif version in (glue.Version.LATEST, Versions.LATEST):
            _latest_class_version = self.schema_version_manager.get_latest_schema_version(_class_name)
            _table.version = _latest_class_version
            queries.append(query)
        else:
            queries.append(query)

        return queries
