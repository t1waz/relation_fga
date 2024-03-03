from __future__ import annotations

import dataclasses
import datetime
import uuid
from typing import Dict
from typing import Optional
from dataclasses import field
from backend.core.utils import get_now


def get_entity_id():
    return str(uuid.uuid4())


@dataclasses.dataclass(frozen=True)
class User:
    email: str
    password: str
    id: str = field(default_factory=get_entity_id)
    first_name: Optional[str] = None
    second_name: Optional[str] = None

    @classmethod
    def from_dict(cls, **data) -> User:
        class_fields = {f.name for f in dataclasses.fields(cls)}

        return User(**{k: v for k, v in data.items() if k in class_fields})

    @property
    def as_dict(self) -> Dict:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class Store:
    name: str
    owner: User
    auth_token: Optional[str] = None
    id: str = field(default_factory=get_entity_id)
    created_at: datetime.datetime = field(default_factory=get_now)

    @property
    def as_dict(self) -> Dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, **data) -> Store:
        class_fields = {f.name for f in dataclasses.fields(cls)}

        return Store(**{k: v for k, v in data.items() if k in class_fields})
