from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple

import networkx as nx

from graph_fga.constants import CONDITION_SEPARATOR
from graph_fga.interpreter.auth_model import AuthModel


@dataclass(frozen=True)
class PathHop:
    """One traversal step: (:src_type)-[:relation]->(:tgt_type)."""

    src_type: str
    relation: str
    tgt_type: str


class AuthModelService:
    def __init__(self, auth_model: AuthModel) -> None:
        self._auth_model = auth_model

    def _get_relation_successor(self, relation: Any) -> Any:
        return next(
            iter(
                (s for s in self.auth_model.g.successors(relation) if s.type == "type")
            ),
            None,
        )

    def _parse_path_to_hops(self, path: List[Any]) -> Tuple[PathHop, ...]:
        """Walk a model-graph path and emit structured hops.

        Same traversal logic as the old _parse_path_to_cmd, but returns
        data instead of a Cypher fragment, so query builders can decide
        how to render each hop (and how to splice in contextual tuples).
        """
        path = list(path)  # nx yields fresh lists, but don't rely on it
        current_type = path.pop(0)
        path.pop(-1)

        hops: List[PathHop] = []
        last_node = None
        for node in path:
            r = None
            successor = self._get_relation_successor(relation=node)

            if node.type == "permission":
                node_data = self.auth_model.g[last_node or current_type][node]
                if node_data:
                    r = node_data["allowed"]
            elif last_node:
                r = f"{node.name}{CONDITION_SEPARATOR}{last_node.name}"
            else:
                r = node.name

            if r:
                hops.append(
                    PathHop(
                        src_type=current_type.name,
                        relation=r,
                        tgt_type=successor.name,
                    )
                )
                current_type = successor

            last_node = node

        return tuple(hops)

    def _filter_paths(self, paths: List[Any], relation: str) -> List[Any]:
        no_types_paths = filter(
            lambda path: all(p.type in ("relation", "permission") for p in path[1:-1]),
            paths,
        )
        relation_paths = filter(lambda path: path[-2].name == relation, no_types_paths)

        return list(relation_paths)

    def get_paths_hops(
        self, start: str, end: str, relation: str
    ) -> List[Tuple[PathHop, ...]]:
        start_type = self.auth_model.get_type(name=start)
        end_type = self.auth_model.get_type(name=end)
        if not start_type or not end_type:
            return []

        graph_paths = list(nx.all_simple_paths(self.auth_model.g, start_type, end_type))
        if not graph_paths:
            return []

        unique_hops = {
            self._parse_path_to_hops(path=path)
            for path in self._filter_paths(paths=graph_paths, relation=relation)
        }

        return [hops for hops in unique_hops if hops]

    def get_paths_cmds(self, start: str, end: str, relation: str) -> List[str]:
        """Kept for backward compatibility (tests, debugging).

        Renders the same hop lists as the old implementation did.
        """
        cmds = set()
        for hops in self.get_paths_hops(start=start, end=end, relation=relation):
            cmd = f"({hops[0].src_type})" + "".join(
                f"-[:{h.relation}]->({h.tgt_type})" for h in hops
            )
            cmds.add(cmd)

        return list(cmds)

    @property
    def auth_model(self) -> AuthModel:
        return self._auth_model
