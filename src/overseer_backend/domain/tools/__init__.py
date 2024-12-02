from typing import Dict


class Tool:
    NAME = "base tool"
    DESCRIPTION = ""

    def call(self, *args, **kwargs) -> str:
        raise NotImplemented

    @property
    def input_schema(self) -> Dict:
        raise NotImplemented
