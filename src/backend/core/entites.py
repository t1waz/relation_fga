from __future__ import annotations

import dataclasses
import inspect
from typing import Dict
from typing import Optional


@dataclasses.dataclass(frozen=True)
class User:
    email: str
    password: str
    first_name: Optional[str] = None
    second_name: Optional[str] = None

    @classmethod
    def from_dict(cls, **data) -> User:
        class_fields = {f.name for f in dataclasses.fields(cls)}

        return User(**{k: v for k, v in data.items() if k in class_fields})

    @property
    def as_dict(self) -> Dict:
        return dataclasses.asdict(self)
