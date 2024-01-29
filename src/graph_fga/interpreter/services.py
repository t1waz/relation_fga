from __future__ import annotations

from typing import List, Any

import networkx as nx

from graph_fga.interpreter.auth_model import AuthModel


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

    def _parse_path_to_cmd(self, path: List[Any]) -> str:
        start_type = path.pop(0)
        path.pop(-1)

        cmd = f"({start_type.name})"
        last_node = None
        for i, node in enumerate(path):
            r = None
            successor = self._get_relation_successor(relation=node)
            if node.type == "permission":
                node_data = self.auth_model.g[last_node or start_type][node]
                if node_data:
                    r = node_data["allowed"]

            elif last_node:
                r = f"{node.name}111{last_node.name}"
            elif r is None:
                r = node.name

            if r:
                cmd = f"{cmd}-[:{r}]->({successor.name})"

            last_node = node

        return cmd

    def _filter_paths(self, paths: List[Any], relation: str) -> List[Any]:
        no_types_paths = filter(
            lambda path: all(p.type in ("relation", "permission") for p in path[1:-1]),
            paths,
        )
        relation_paths = filter(lambda path: path[-2].name == relation, no_types_paths)

        return list(relation_paths)

    def get_paths_cmds(self, start: str, end: str, relation: str) -> List[str]:
        start_type = self.auth_model.get_type(name=start)
        end_type = self.auth_model.get_type(name=end)
        if not start_type or not end_type:
            return []

        graph_paths = list(nx.all_simple_paths(self.auth_model.g, start_type, end_type))
        if not graph_paths:
            return []

        return list(
            {
                self._parse_path_to_cmd(path=path)
                for path in self._filter_paths(paths=graph_paths, relation=relation)
            }
        )

    @property
    def auth_model(self) -> AuthModel:
        return self._auth_model
