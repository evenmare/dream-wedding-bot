"""Module contains base repository implementation."""

import abc
from typing import Generic

from typings.repositories import Model_, Schema


class BaseDatabaseRepository(abc.ABC, Generic[Model_, Schema]):
    """Implements base logic for repositories."""

    @abc.abstractmethod
    @property
    def schema(self) -> Schema:
        """Returns the schema for the repository."""
        raise NotImplementedError('schema')

    @abc.abstractmethod
    @property
    def _model(self) -> Model_:
        """Returns the model that this repository represents."""
        raise NotImplementedError('model')

    def _serialize_model(self, obj_orm: Model_) -> Schema:
        """Method implements logic for serializing a model record."""
        return self.schema.model_validate(
            obj_orm,
            from_attributes=True,
        )
