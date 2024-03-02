from __future__ import annotations

import dataclasses
import uuid
from typing import Dict
from typing import Optional


@dataclasses.dataclass(frozen=True)
class User:
    email: str
    password: str
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    first_name: Optional[str] = None
    second_name: Optional[str] = None

    @classmethod
    def from_dict(cls, **data) -> User:
        class_fields = {f.name for f in dataclasses.fields(cls)}

        return User(**{k: v for k, v in data.items() if k in class_fields})

    @property
    def as_dict(self) -> Dict:
        data = dataclasses.asdict(self)
        user_id = data.pop("id")

        return {"id": str(user_id), **data}
