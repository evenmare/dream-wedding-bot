"""Module contains base repository implementation."""

import abc
from typing import Generic

from typings.repositories import ManyToManyModel, Model_, Schema


class BaseDatabaseRepository(abc.ABC, Generic[Model_, Schema]):
    """Implements base logic for repositories."""

    @property
    @abc.abstractmethod
    def schema(self) -> Schema:
        """Returns the schema for the repository."""
        raise NotImplementedError('schema')

    @property
    @abc.abstractmethod
    def _model(self) -> Model_:
        """Returns the model that this repository represents."""
        raise NotImplementedError('_model')

    def _serialize_model(self, obj_orm: Model_) -> Schema:
        """Method implements logic for serializing a model record."""
        return self.schema.model_validate(
            obj_orm,
            from_attributes=True,
        )


class BaseManyToManyRepository(
    BaseDatabaseRepository[Model_, Schema],
    abc.ABC,
    Generic[Model_, ManyToManyModel, Schema],
):
    """Implements base logic for many2many repositories."""

    @property
    def _m2m_model(self) -> ManyToManyModel:
        """Returns the model that this repository uses for relations."""
        raise NotImplementedError('_m2m_model')
