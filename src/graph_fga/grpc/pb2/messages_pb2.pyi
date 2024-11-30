from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class StoreRelationTuple(_message.Message):
    __slots__ = ("user", "relation", "object")
    USER_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    user: str
    relation: str
    object: str
    def __init__(
        self,
        user: _Optional[str] = ...,
        relation: _Optional[str] = ...,
        object: _Optional[str] = ...,
    ) -> None: ...

class StoreWriteRequest(_message.Message):
    __slots__ = ("store_id", "writes", "deletes")
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    WRITES_FIELD_NUMBER: _ClassVar[int]
    DELETES_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    writes: _containers.RepeatedCompositeFieldContainer[StoreRelationTuple]
    deletes: _containers.RepeatedCompositeFieldContainer[StoreRelationTuple]
    def __init__(
        self,
        store_id: _Optional[str] = ...,
        writes: _Optional[_Iterable[_Union[StoreRelationTuple, _Mapping]]] = ...,
        deletes: _Optional[_Iterable[_Union[StoreRelationTuple, _Mapping]]] = ...,
    ) -> None: ...

class StoreWriteResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class StoreCheckRequest(_message.Message):
    __slots__ = ("user", "permission", "object", "store_id", "contextual_tuples")
    USER_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_TUPLES_FIELD_NUMBER: _ClassVar[int]
    user: str
    permission: str
    object: str
    store_id: str
    contextual_tuples: _containers.RepeatedCompositeFieldContainer[StoreRelationTuple]
    def __init__(
        self,
        user: _Optional[str] = ...,
        permission: _Optional[str] = ...,
        object: _Optional[str] = ...,
        store_id: _Optional[str] = ...,
        contextual_tuples: _Optional[
            _Iterable[_Union[StoreRelationTuple, _Mapping]]
        ] = ...,
    ) -> None: ...

class StoreCheckResponse(_message.Message):
    __slots__ = ("allowed",)
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    allowed: bool
    def __init__(self, allowed: bool = ...) -> None: ...

class StoreCreateRequest(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: str
    def __init__(self, model: _Optional[str] = ...) -> None: ...

class StoreCreateResponse(_message.Message):
    __slots__ = ("status", "store_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    status: str
    store_id: str
    def __init__(
        self, status: _Optional[str] = ..., store_id: _Optional[str] = ...
    ) -> None: ...

class StoreUpdateRequest(_message.Message):
    __slots__ = ("store_id", "model")
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    model: str
    def __init__(
        self, store_id: _Optional[str] = ..., model: _Optional[str] = ...
    ) -> None: ...

class StoreUpdateResponse(_message.Message):
    __slots__ = ("status", "store_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    status: str
    store_id: str
    def __init__(
        self, status: _Optional[str] = ..., store_id: _Optional[str] = ...
    ) -> None: ...

class StoreViewRequest(_message.Message):
    __slots__ = ("store_id",)
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    def __init__(self, store_id: _Optional[str] = ...) -> None: ...

class StoreViewResponse(_message.Message):
    __slots__ = ("store_id", "model")
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    model: str
    def __init__(
        self, store_id: _Optional[str] = ..., model: _Optional[str] = ...
    ) -> None: ...

class StoreListObjectsRequest(_message.Message):
    __slots__ = ("store_id", "user", "permission", "type", "contextual_tuples")
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_TUPLES_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    user: str
    permission: str
    type: str
    contextual_tuples: _containers.RepeatedCompositeFieldContainer[StoreRelationTuple]
    def __init__(
        self,
        store_id: _Optional[str] = ...,
        user: _Optional[str] = ...,
        permission: _Optional[str] = ...,
        type: _Optional[str] = ...,
        contextual_tuples: _Optional[
            _Iterable[_Union[StoreRelationTuple, _Mapping]]
        ] = ...,
    ) -> None: ...

class StoreListObjectsResponse(_message.Message):
    __slots__ = ("objects",)
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, objects: _Optional[_Iterable[str]] = ...) -> None: ...

class StoreReadObj(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    def __init__(
        self, id: _Optional[str] = ..., type: _Optional[str] = ...
    ) -> None: ...

class StoreReadRequest(_message.Message):
    __slots__ = ("store_id", "relation", "source", "target")
    STORE_ID_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    store_id: str
    relation: str
    source: StoreReadObj
    target: StoreReadObj
    def __init__(
        self,
        store_id: _Optional[str] = ...,
        relation: _Optional[str] = ...,
        source: _Optional[_Union[StoreReadObj, _Mapping]] = ...,
        target: _Optional[_Union[StoreReadObj, _Mapping]] = ...,
    ) -> None: ...

class StoreReadResponse(_message.Message):
    __slots__ = ("objects",)
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[StoreRelationTuple]
    def __init__(
        self, objects: _Optional[_Iterable[_Union[StoreRelationTuple, _Mapping]]] = ...
    ) -> None: ...
