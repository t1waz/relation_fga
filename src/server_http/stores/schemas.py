from attrs import define, field
from typing import List, Dict


@define
class StoreWriteRequestTuple:
    user: str
    relation: str
    object: str


@define
class StoreWriteRequest:
    writes: Dict[str, List[StoreWriteRequestTuple]] = field()
    deletes: Dict[str, List[StoreWriteRequestTuple]] = field()
