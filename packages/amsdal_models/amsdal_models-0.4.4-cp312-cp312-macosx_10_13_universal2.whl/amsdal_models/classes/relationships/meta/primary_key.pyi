from amsdal_models.classes.model import Model as Model
from amsdal_models.classes.relationships.constants import ANNOTATIONS as ANNOTATIONS, DEFERRED_PRIMARY_KEYS as DEFERRED_PRIMARY_KEYS, PRIMARY_KEY as PRIMARY_KEY, PRIMARY_KEY_FIELDS as PRIMARY_KEY_FIELDS
from amsdal_models.classes.relationships.meta.common import get_type_for as get_type_for, is_model_subclass as is_model_subclass
from typing import Any

def resolve_primary_keys(bases: tuple[type[Any], ...], namespace: dict[str, Any]) -> list[str]: ...
def process_primary_keys(pks: list[str], bases: tuple[type[Any], ...], namespace: dict[str, Any]) -> None: ...
def _build_pk_fields(model: type['Model'], prefix: str = '') -> dict[str, Any]: ...
def build_metadata_primary_key(model: type['Model']) -> dict[str, Any]: ...
