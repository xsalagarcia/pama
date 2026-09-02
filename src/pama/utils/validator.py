from typing import Any, Annotated

from pydantic import TypeAdapter, ValidationError
from sqlmodel import SQLModel


def is_valid(model: type[SQLModel], field: str, value: Any) -> bool:
    """
    Check if a value is a valid field for a given model.
    :param model:
    :param field:
    :param value:
    :return:
    """

    field_info = model.model_fields.get(field)
    adapter = TypeAdapter(Annotated[field_info.annotation, *field_info.metadata])
    try:
        adapter.validate_python(value)
        return True
    except ValidationError:
        return False