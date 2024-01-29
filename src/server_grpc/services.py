from __future__ import annotations

from typing import List, Optional

from graph_fga.engine import PermissionEngine
from graph_fga.entities import RelationTuple, CheckRequest, ListObjectsRequest
from graph_fga.exceptions import InvalidRelationTupleException
from graph_fga.interpreter.auth_model import AuthModel
from server_grpc.repositories import (
    model_config_repository,
    fga_driver,
    relation_tuple_repository,
)
from neo4j import Session, Transaction


def get_permission_engine(store_id: str) -> PermissionEngine:
    auth_model = model_config_repository.get_model_config(store_id=store_id)
    if not auth_model:
        raise ValueError("invalid store_id")

    return PermissionEngine(
        driver=fga_driver,
        model=auth_model,
    )


def get_graph_session() -> Session:
    return fga_driver.session(database="memgraph")


class StoreLogic:
    def __init__(self, permission_engine: PermissionEngine, store_id: str) -> None:
        self._store_id = store_id
        self._permission_engine = permission_engine

    @classmethod
    def setup(cls, store_id: str) -> StoreLogic:
        return cls(
            store_id=store_id,
            permission_engine=get_permission_engine(store_id=store_id),
        )

    def validate_relation_tuple(self, relation_tuple: RelationTuple) -> None:
        try:
            self._permission_engine.validate_relation_tuple(
                relation_tuple=relation_tuple
            )
        except ValueError as exc:
            raise InvalidRelationTupleException(exc)

    def validate_relation_tuples(self, relation_tuples: List[RelationTuple]) -> None:
        for relation_tuple in relation_tuples:
            self.validate_relation_tuple(relation_tuple=relation_tuple)

    def persist_relation_tuples(
        self,
        writes: List[RelationTuple],
        deletes: List[RelationTuple],
        skip_validation: bool = False,
    ):
        session = get_graph_session()
        with session.begin_transaction() as tx:
            self.add_relation_tuples(
                relation_tuples=writes, skip_validation=skip_validation, tx=tx
            )
            self.delete_relation_tuples(
                relation_tuples=deletes, skip_validation=skip_validation, tx=tx
            )
            tx.commit()

    def add_relation_tuples(
        self,
        relation_tuples: List[RelationTuple],
        skip_validation: bool = False,
        tx: Optional[Transaction] = None,
    ) -> None:
        if not skip_validation:
            self.validate_relation_tuples(relation_tuples=relation_tuples)

        for relation_tuple in relation_tuples:
            relation_tuple_repository.save(
                store_id=self._store_id, relation_tuple=relation_tuple, tx=tx
            )

    def delete_relation_tuples(
        self,
        relation_tuples: List[RelationTuple],
        skip_validation: bool = False,
        tx: Optional[Transaction] = None,
    ) -> None:
        if not skip_validation:
            self.validate_relation_tuples(relation_tuples=relation_tuples)

        for relation_tuple in relation_tuples:
            relation_tuple_repository.delete(
                store_id=self._store_id, relation_tuple=relation_tuple, tx=tx
            )

    def is_allowed(self, check_request: CheckRequest) -> bool:
        return self._permission_engine.check_permission(
            store_id=self._store_id, check_request=check_request
        )

    def list_objects(self, list_objects_request: ListObjectsRequest) -> List[str]:
        return self._permission_engine.get_objects(
            store_id=self._store_id, list_objects_request=list_objects_request
        )

    def list_relations(
        self,
        source_type: str,
        source_id: Optional[str],
        target_type: Optional[str],
        target_id: Optional[str],
    ) -> List[RelationTuple]:
        return self._permission_engine.get_relations(
            source_id=source_id,
            target_id=target_id,
            store_id=self._store_id,
            source_type=source_type,
            target_type=target_type,
        )

    @property
    def auth_model(self) -> AuthModel:
        return self._permission_engine.auth_model
