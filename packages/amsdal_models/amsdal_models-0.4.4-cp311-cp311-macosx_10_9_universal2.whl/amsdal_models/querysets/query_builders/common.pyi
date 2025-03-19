import abc
import amsdal_glue as glue
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal_models.classes.model import Model as Model
from amsdal_models.classes.relationships.constants import FOREIGN_KEYS as FOREIGN_KEYS, PRIMARY_KEY_FIELDS as PRIMARY_KEY_FIELDS
from amsdal_models.classes.relationships.meta.common import resolve_model_type as resolve_model_type
from amsdal_models.classes.relationships.meta.references import build_fk_db_fields as build_fk_db_fields
from amsdal_models.querysets.base_queryset import QuerySetBase as QuerySetBase
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import NumberPaginator as NumberPaginator
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q as Q
from typing import Any, TypeVar

ModelType = TypeVar('ModelType', bound='Model')

class BaseQueryBuilder:
    qs_table_name: str
    qs_model: type['ModelType']
    qs_select_related: dict[tuple[str, type['ModelType'], str], Any] | None
    qs_only: list[str] | None
    qs_conditions: Q | None
    qs_order_by: list[OrderBy]
    qs_limit: NumberPaginator
    _queryset: Incomplete
    def __init__(self, queryset: QuerySetBase) -> None: ...
    def build_limit(self) -> glue.LimitQuery | None: ...
    @staticmethod
    def build_field(field_name: str) -> glue.Field: ...
    @staticmethod
    def build_table_name(model: type['ModelType']) -> str: ...
    def normalize_primary_key(self, pk: str) -> str | list[str]: ...
    def _extract_select_related(self) -> dict[tuple[str, type['ModelType'], str], Any] | None: ...
    def _process_select_related(self, select_related: dict[str, Any], model: type['ModelType'], alias_index: int = 0) -> dict[tuple[str, type['ModelType'], str], Any] | None: ...
    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup: ...
    @classmethod
    def _process_nested_rest(cls, rest: str, select_related: dict[tuple[str, type['ModelType'], str], Any] | None = None) -> str: ...

class QueryBuilder(BaseQueryBuilder, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def transform(self) -> glue.QueryStatement: ...
    @abstractmethod
    def transform_count(self) -> glue.QueryStatement: ...
    @classmethod
    @abstractmethod
    def _build_nested_only(cls, select_related: dict[tuple[str, type['ModelType'], str], Any]) -> list[glue.FieldReferenceAliased]: ...
    def build_only(self, model: type['ModelType'], only: list[str] | None = None, select_related: dict[tuple[str, type['ModelType'], str], Any] | None = None) -> list[glue.FieldReference | glue.FieldReferenceAliased] | None: ...

class AsyncQueryBuilder(BaseQueryBuilder, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    async def transform(self) -> glue.QueryStatement: ...
    @abstractmethod
    async def transform_count(self) -> glue.QueryStatement: ...
    @abstractmethod
    async def _build_nested_only(self, select_related: dict[tuple[str, type['ModelType'], str], Any]) -> list[glue.FieldReferenceAliased]: ...
    async def build_only(self, model: type['ModelType'], only: list[str] | None = None, select_related: dict[tuple[str, type['ModelType'], str], Any] | None = None) -> list[glue.FieldReference | glue.FieldReferenceAliased] | None: ...
