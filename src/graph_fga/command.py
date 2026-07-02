from typing import Any, List, Optional, Sequence, Tuple

from graph_fga.interpreter.services import PathHop


class GraphTraversalQuery:
    RESULT_KEY = "res"

    def __init__(self, paths: Sequence[Tuple[PathHop, ...]]) -> None:
        if not paths:
            raise ValueError("at least one path is required")

        self._paths = list(paths)

    @staticmethod
    def _hop_cypher(k: int, i: int, hop: PathHop) -> str:
        a, b = f"a{k}_{i}", f"b{k}_{i}"
        f_prev, f_next, db = f"f{k}_{i}", f"f{k}_{i + 1}", f"db{k}_{i}"

        return (
            f"OPTIONAL MATCH ({a}:{hop.src_type} {{store: $store_id}})"
            f"-[:{hop.relation}]->"
            f"({b}:{hop.tgt_type} {{store: $store_id}})\n"
            f"WHERE {a}.id IN {f_prev}\n"
            f"WITH {f_prev}, collect(DISTINCT {b}.id) AS {db}\n"
            f"WITH {db} + ["
            f"ct IN $ctx WHERE ct.relation = '{hop.relation}' "
            f"AND ct.src_type = '{hop.src_type}' "
            f"AND ct.tgt_type = '{hop.tgt_type}' "
            f"AND ct.src_id IN {f_prev} "
            f"| ct.tgt_id] AS {f_next}\n"
        )

    def _path_chain(self, k: int, hops: Tuple[PathHop, ...]) -> str:
        parts = [f"WITH [$source_id] AS f{k}_0\n"]
        for i, hop in enumerate(hops):
            parts.append(self._hop_cypher(k=k, i=i, hop=hop))

        return "".join(parts)

    @property
    def check_cmd(self) -> str:
        branches = []
        for k, hops in enumerate(self._paths):
            branches.append(
                f"{self._path_chain(k=k, hops=hops)}"
                f"RETURN any(x IN f{k}_{len(hops)} WHERE x = $target_id) "
                f"AS {self.RESULT_KEY}"
            )

        return "\nUNION\n".join(branches)

    @property
    def list_cmd(self) -> str:
        branches = []
        for k, hops in enumerate(self._paths):
            branches.append(
                f"{self._path_chain(k=k, hops=hops)}"
                f"UNWIND f{k}_{len(hops)} AS obj{k}\n"
                f"RETURN obj{k} AS {self.RESULT_KEY}"
            )

        return "\nUNION\n".join(branches)


class GraphRelationsCommand:
    def __init__(
        self,
        store_id: str,
        source_type: str,
        source_id: Optional[str],
        target_type: Optional[str],
        target_id: Optional[str],
    ) -> None:
        if target_id and not target_type:
            raise ValueError("need to pass target_type with target_id")

        self._store_id = store_id
        self._source_id = source_id
        self._target_id = target_id
        self._source_type = source_type
        self._target_type = target_type

        self._validate()

    def _validate(self) -> None:
        if self._target_id and not self._target_type:
            raise ValueError("need to pass target_type with target_id")

    @property
    def graph_cmd(self) -> Any:
        return f"MATCH {self.source_cmd}-[r]->{self.target_cmd}\n" f"RETURN s, r, t"

    @property
    def source_cmd(self) -> str:
        cmd = f'(s:{self._source_type} {{store: "{self._store_id}"'
        if self._source_id:
            cmd = f'{cmd}, id: "{self._source_id}"'

        return f"{cmd}}})"

    @property
    def target_cmd(self) -> str:
        if not self._target_type and not self._target_id:
            return "(t)"

        cmd = f"(t"
        if self._target_type:
            cmd = f"{cmd}:{self._target_type}"
        if self._target_id:
            cmd = f'{cmd} {{id: "{self._target_id}"'

        return f"{cmd}}})"
