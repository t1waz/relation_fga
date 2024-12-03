from dataclasses import asdict
from typing import List, Optional, Any

from graph_fga.command import (
    GraphListCommand,
    GraphInstanceCommand,
    GraphRelationsCommand,
)
from graph_fga.entities import (
    CheckRequest,
    RelationTuple,
    ListObjectsRequest,
)
from graph_fga.exceptions import InvalidRelationTupleException
from graph_fga.interpreter.auth_model import AuthModel
from graph_fga.interpreter.entites import ModelType
from graph_fga.interpreter.services import AuthModelService
from graph_fga.logger import logger
from graph_fga.repository import RelationTupleRepository


class PermissionEngine:
    def __init__(
        self,
        driver,
        model: AuthModel,
        relation_tuple_repository: RelationTupleRepository,
    ) -> None:
        self._model = model
        self._driver = driver
        self._relation_tuple_repository = relation_tuple_repository
        self._model_service = AuthModelService(auth_model=self._model)

    def check_permission(self, store_id: str, check_request: CheckRequest) -> bool:
        source_type: ModelType = self._model.get_type(name=check_request.source_type)
        if not source_type:
            return False

        target_type: ModelType = self._model.get_type(name=check_request.target_type)
        if not target_type:
            return False

        type_relation: Any = self._model.get_type_relation(
            name=check_request.permission, type_name=target_type.name
        )
        if not type_relation:
            return False

        cmd = GraphInstanceCommand(
            source_gid=check_request.source,
            target_gid=check_request.target,
            store_id=store_id,
        )
        for cmd_str in self._model_service.get_paths_cmds(
            start=source_type.name, end=target_type.name, relation=type_relation.name
        ):
            cmd.add_cmd_str(cmd_str=cmd_str)

        with self._driver.session(database="memgraph") as session:
            with session.begin_transaction() as tx:
                for context_tuple in check_request.contextual_tuples:
                    self._relation_tuple_repository.save(
                        store_id=store_id, relation_tuple=context_tuple, tx=tx
                    )

                logger.debug(f"check permission cmd: {cmd.graph_cmd}")
                result = tx.run(cmd.graph_cmd, database_="memgraph")
                data = result.data()

                tx.rollback()

        result = next(iter(data[0][cmd.result_key]), False)

        return bool(result)

    def get_relations(
        self,
        store_id: str,
        source_type: str,
        source_id: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
    ) -> List[RelationTuple]:
        cmd = GraphRelationsCommand(
            store_id=store_id,
            source_id=source_id,
            target_id=target_id,
            source_type=source_type,
            target_type=target_type,
        )

        with self._driver.session(database="memgraph") as session:
            logger.debug(f"get relations cmd: {cmd.graph_cmd}")
            result = session.run(cmd.graph_cmd, database_="memgraph")
            data = result.data()

        relations = [d["r"] for d in data]
        return [
            RelationTuple(
                source=f"{d[0]['type']}:{d[0]['id']}",
                target=f"{d[2]['type']}:{d[2]['id']}",
                relation=d[1],
            )
            for d in relations
        ]

    def get_objects(
        self, store_id: str, list_objects_request: ListObjectsRequest
    ) -> List[str]:
        source_type: ModelType = self._model.get_type(
            name=list_objects_request.source_type
        )
        if not source_type:
            return []

        target_type: ModelType = self._model.get_type(
            name=list_objects_request.target_type
        )
        if not target_type:
            return []

        type_relation: Any = self._model.get_type_relation(
            name=list_objects_request.permission, type_name=target_type.name
        )
        if not type_relation:
            return []

        cmd = GraphListCommand(
            store_id=store_id,
            source_gid=list_objects_request.source,
            target_type=list_objects_request.target_type,
        )
        for cmd_str in self._model_service.get_paths_cmds(
            start=source_type.name, end=target_type.name, relation=type_relation.name
        ):
            cmd.add_cmd_str(cmd_str=cmd_str)

        with self._driver.session(database="memgraph") as session:
            with session.begin_transaction() as tx:
                for context_tuple in list_objects_request.contextual_tuples:
                    self._relation_tuple_repository.save(
                        store_id=store_id, relation_tuple=context_tuple, tx=tx
                    )

                logger.debug(f"get objects cmd: {cmd.graph_cmd}")
                result = tx.run(cmd.graph_cmd, database_="memgraph")
                data = result.data()

                tx.rollback()

        return [str(d) for d in data[0][cmd.result_key]]

    def validate_relation_tuple(self, relation_tuple: RelationTuple) -> None:
        target_type = self.auth_model.get_type(name=relation_tuple.target_name)
        if not target_type:
            raise InvalidRelationTupleException(f"invalid target type")

        relation = self.auth_model.get_relation(
            name=relation_tuple.relation,
            type_name=target_type.name,
        )

        if not relation:
            raise InvalidRelationTupleException(
                f'invalid relation: "{relation_tuple.relation}" '
                f"for tuple: {asdict(relation_tuple)} "
                f"allowed: {[r.name for r in self.auth_model.relations if r.model_type == target_type]} "
                f"type: {target_type.name}"
            )

        allowed_source_names = self.auth_model.get_relation_related_names(
            relation=relation
        )

        if relation_tuple.source_full_name not in allowed_source_names:
            raise InvalidRelationTupleException(
                f'invalid source type: "{relation_tuple.source_name}" '
                f"for tuple: {asdict(relation_tuple)} "
                f"allowed: {allowed_source_names} "
                f"type: {target_type.name}"
            )

        if not relation_tuple.source_id:
            raise InvalidRelationTupleException(
                f'invalid source_id: "{relation_tuple.source_id}" '
                f"for tuple: {asdict(relation_tuple)} "
                f"error: missing source_id"
            )

        if not relation_tuple.target_id:
            raise InvalidRelationTupleException(
                f"invalid target_id: {relation_tuple.target_id} "
                f"for tuple: {asdict(relation_tuple)} "
                f"error: missing target_id"
            )

    @property
    def auth_model(self) -> AuthModel:
        return self._model
