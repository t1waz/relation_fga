from typing import Optional, Any

from graph_fga.utils import get_id_from_gid, get_type_from_gid


class GraphListCommand:
    def __init__(self, source_gid: str, target_type: str, store_id: str) -> None:
        self._store_id = store_id
        self._source_gid = source_gid
        self._target_type = target_type

        self._call_cmd_count = 0
        self._cmd = (
            f"MATCH (s:{self.source_type} "
            f'{{id: "{self.source_id}", store: "{self._store_id}"}})\n'
        )

    def add_cmd_str(self, cmd_str: str) -> None:
        cmd_str = cmd_str.replace(f"({self.source_type})", "(s)", 1)
        target = f'(t{self.var_num}:{self.target_type}  {{store: "{self._store_id}"}})'
        cmd_str = cmd_str[::-1].replace(f"({self.target_type})"[::-1], target[::-1], 1)[
            ::-1
        ]

        cmd_part = (
            f"CALL {{\n"
            f"  WITH s\n"
            f"  MATCH {cmd_str}\n"
            f"  RETURN collect(t{self.var_num}.id) as t{self.var_num}\n"
            f"}}"
        )
        self._cmd = f"{self._cmd}{cmd_part}\n"
        self._call_cmd_count += 1

    @property
    def var_num(self) -> int:
        return self._call_cmd_count

    @property
    def source_type(self) -> str:
        return get_type_from_gid(gid_key=self._source_gid)

    @property
    def source_id(self) -> str:
        return get_id_from_gid(gid_key=self._source_gid)

    @property
    def target_type(self) -> str:
        return self._target_type

    @property
    def graph_cmd(self) -> Any:
        variables = [f"t{i}" for i in range(self.var_num)]
        return (
            f"{self._cmd} WITH {', '.join(variables)}\n"
            f"UNWIND {' + '.join(variables)} AS results\n"
            f"RETURN COLLECT(DISTINCT results) as {self.result_key}"
        )

    @property
    def result_key(self) -> str:
        return "res"


class GraphInstanceCommand:
    def __init__(self, source_gid: str, target_gid: str, store_id: str) -> None:
        self._store_id = store_id
        self._source_gid = source_gid
        self._target_gid = target_gid

        self._call_cmd_count = 0
        self._cmd = (
            f"MATCH (s:{self.source_type} "
            f'{{id: "{self.source_id}", store: "{self._store_id}"}})\n'
        )

    def add_cmd_str(self, cmd_str: str) -> None:
        cmd_str = cmd_str.replace(f"({self.source_type})", "(s)", 1)
        target = (
            f"(t{self.var_num}:{self.target_type}  "
            f'{{id: "{self.target_id}", store: "{self._store_id}"}})'
        )
        cmd_str = cmd_str[::-1].replace(f"({self.target_type})"[::-1], target[::-1], 1)[
            ::-1
        ]

        cmd_part = (
            f"CALL {{\n"
            f"  WITH s\n"
            f"  MATCH {cmd_str}\n"
            f"  RETURN collect(t{self.var_num}.id) as t{self.var_num}\n"
            f"  LIMIT 1\n"
            f"}}"
        )
        self._cmd = f"{self._cmd}{cmd_part}\n"
        self._call_cmd_count += 1

    @property
    def var_num(self) -> int:
        return self._call_cmd_count

    @property
    def source_type(self) -> str:
        return get_type_from_gid(gid_key=self._source_gid)

    @property
    def source_id(self) -> str:
        return get_id_from_gid(gid_key=self._source_gid)

    @property
    def target_id(self) -> str:
        return get_id_from_gid(gid_key=self._target_gid)

    @property
    def target_type(self) -> str:
        return get_type_from_gid(gid_key=self._target_gid)

    @property
    def result_key(self) -> str:
        return "res"

    @property
    def graph_cmd(self) -> Any:
        variables = [f"t{i}" for i in range(self.var_num)]
        return (
            f"{self._cmd} WITH {', '.join(variables)}\n"
            f"UNWIND {' + '.join(variables)} AS results\n"
            f"RETURN COLLECT(DISTINCT results) as {self.result_key}\n"
            f"LIMIT 1"
        )


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
            cmd = f'{cmd} {{id: "{self._source_id}"'

        return f"{cmd}}})"
