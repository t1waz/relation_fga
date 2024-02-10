from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Optional, List

from graph_fga.utils import get_type_from_gid, get_id_from_gid


@dataclass(frozen=True)
class RelationTuple:
    source: str
    target: str
    relation: str

    @cached_property
    def target_name(self) -> Optional[str]:
        return get_type_from_gid(gid_key=self.target)

    @cached_property
    def source_name(self) -> str:
        return get_type_from_gid(gid_key=self.source)

    @cached_property
    def target_id(self) -> str:
        target_id = get_id_from_gid(gid_key=self.target)
        if "#" in target_id:
            return target_id.split("#")[0]

        return target_id

    @cached_property
    def source_id(self) -> str:
        source_id = get_id_from_gid(gid_key=self.source)
        if "#" in source_id:
            return source_id.split("#")[0]

        return source_id

    @cached_property
    def condition_type(self) -> Optional[str]:
        try:
            return self.source.split("#")[1]
        except (KeyError, ValueError, IndexError):
            return None


@dataclass(frozen=True)
class CheckRequest:
    source: str
    target: str
    permission: str
    contextual_tuples: Optional[List[RelationTuple]] = None

    @cached_property
    def target_type(self) -> str:
        return get_type_from_gid(gid_key=self.target)

    @cached_property
    def source_type(self) -> str:
        return get_type_from_gid(gid_key=self.source)

    @cached_property
    def source_id(self) -> str:
        return get_id_from_gid(gid_key=self.source)

    @cached_property
    def target_id(self) -> str:
        return get_id_from_gid(gid_key=self.target)


@dataclass(frozen=True)
class ListObjectsRequest:
    source: str
    target_type: str
    permission: str

    @cached_property
    def source_type(self) -> str:
        return get_type_from_gid(gid_key=self.source)

    @cached_property
    def source_id(self) -> str:
        return get_id_from_gid(gid_key=self.source)
