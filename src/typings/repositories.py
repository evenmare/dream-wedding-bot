"""Module contains typings for repositories."""

from typing import TypeVar

from pydantic import BaseModel
from tortoise.models import Model

Model_ = TypeVar('Model_', bound=Model)
ManyToManyModel = TypeVar('ManyToManyModel', bound=Model)
Schema = TypeVar('Schema', bound=BaseModel)
