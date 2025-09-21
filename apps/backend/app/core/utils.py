from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_pydantic(db_object, pydantic_model: Type[T]) -> T:
    """Convert a SQLAlchemy model instance to a Pydantic model.

    Uses Pydantic v2 model_validate with from_attributes=True.
    """
    return pydantic_model.model_validate(db_object, from_attributes=True)
