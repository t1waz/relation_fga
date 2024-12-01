import dataclasses
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class AIMessage:
    role: str
    content: Any

    @property
    def as_api_data(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
        }
