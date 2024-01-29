from __future__ import annotations

import uuid


class ModelType:
    def __init__(self, name):
        self._name = name
        self._id = str(uuid.uuid4())

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return "type"

    @property
    def id(self) -> str:
        return self._id


class ModelTypeRelation:
    def __init__(self, name: str, model_type: ModelType) -> None:
        self._name = name
        self._model_type = model_type
        self._id = str(uuid.uuid4())

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"<relation: {self._name} for: {self.model_type.name}>"

    @property
    def name(self) -> str:
        return self._name

    @property
    def model_type(self) -> ModelType:
        return self._model_type

    @property
    def type(self) -> str:
        return "relation"

    @property
    def id(self) -> str:
        return self._id


class ModelTypePermission:
    def __init__(self, name: str, model_type: ModelType) -> None:
        self._name = name
        self._model_type = model_type
        self._id = str(uuid.uuid4())

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"<permission: {self._name} for: {self.model_type.name}>"

    @property
    def name(self) -> str:
        return self._name

    @property
    def model_type(self) -> ModelType:
        return self._model_type

    @property
    def type(self) -> str:
        return "permission"

    @property
    def id(self) -> str:
        return self._id
