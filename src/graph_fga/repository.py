import base64
import pickle
from typing import Optional, List

from neo4j import Driver, Transaction

from graph_fga.entities import RelationTuple
from graph_fga.interpreter.auth_model import AuthModel


class RelationTupleRepository:
    def __init__(self, driver: Driver):
        self._driver = driver

    @staticmethod
    def _get_relation(relation_tuple: RelationTuple) -> str:
        if relation_tuple.condition_type:
            return f"{relation_tuple.relation}111{relation_tuple.condition_type}"  # TODO: move to constants
        else:
            return relation_tuple.relation

    def _get_tuple_save_cmd(self, store_id: str, relation_tuple: RelationTuple) -> str:
        merge_source_cmd = (
            f"MERGE (s:{relation_tuple.source_name} "
            f'{{id: "{relation_tuple.source_id}", '
            f'store: "{store_id}",'
            f'type: "{relation_tuple.source_name}"}})'
        )
        merge_target_cmd = (
            f"MERGE (t:{relation_tuple.target_name} "
            f'{{id: "{relation_tuple.target_id}", '
            f'store: "{store_id}",'
            f'type: "{relation_tuple.target_name}"}})'
        )
        relation = self._get_relation(relation_tuple=relation_tuple)
        relation_cmd = f"MERGE (s)-[:{relation}]->(t)"

        return " ".join([merge_source_cmd, merge_target_cmd, relation_cmd])

    def _get_tuple_delete_cmd(
        self, store_id: str, relation_tuple: RelationTuple
    ) -> str:
        relation = self._get_relation(relation_tuple=relation_tuple)
        return (
            f"MATCH (s:{relation_tuple.source_name})-[r:{relation}]->(t:{relation_tuple.target_name})\n"
            f'WHERE s.id = "{relation_tuple.source_id}" '
            f'  AND s.store = "{store_id}" '
            f'  AND t.id = "{relation_tuple.target_id}"\n'
            f"DELETE r"
        )

    def is_exists(self, store_id: str, relation_tuple: RelationTuple) -> bool:
        relation = self._get_relation(relation_tuple=relation_tuple)
        with self._driver.session(database="memgraph") as session:
            result = session.run(
                f"MATCH (s:{relation_tuple.source_name} "
                f'{{id: "{relation_tuple.source_id}", store: "{store_id}"}})'
                f"-[r:{relation}]->(t:{relation_tuple.target_name} "
                f'{{id: "{relation_tuple.target_id}", store: "{store_id}"}})'
                f" RETURN s LIMIT 1"
            )
            data = result.data()

        return bool(data) and len(data) > 0

    def save(
        self,
        store_id: str,
        relation_tuple: RelationTuple,
        tx: Optional[Transaction] = None,
    ) -> None:
        tuple_save_cmd = self._get_tuple_save_cmd(
            store_id=store_id, relation_tuple=relation_tuple
        )
        if tx:
            tx.run(tuple_save_cmd)
        else:
            with self._driver.session(database="memgraph") as session:
                session.run(tuple_save_cmd, database_="memgraph")

    def delete(
        self,
        store_id: str,
        relation_tuple: RelationTuple,
        tx: Optional[Transaction] = None,
    ) -> None:
        tuple_delete_cmd = self._get_tuple_delete_cmd(
            store_id=store_id, relation_tuple=relation_tuple
        )
        if tx:
            tx.run(tuple_delete_cmd, database_="memgraph")
        else:
            with self._driver.session(database="memgraph") as session:
                session.run(tuple_delete_cmd, database_="memgraph")


class AuthModelRepository:
    def __init__(self, driver: Driver):
        self._driver = driver

    @staticmethod
    def _model_to_blob(auth_model: AuthModel) -> str:
        b_data = pickle.dumps(auth_model)

        return base64.b64encode(b_data).decode()

    @staticmethod
    def _blob_to_model(blob: str):  # TODO - typing
        b_data = base64.b64decode(blob)

        return pickle.loads(b_data)

    @staticmethod
    def _get_auth_model_create_indexes_cmds(auth_model: AuthModel) -> List[str]:
        cmds = [f"CREATE INDEX ON :store(id);"]
        for type_name in auth_model.type_names:
            cmds.append(f"CREATE INDEX ON :{type_name}(id);")
            cmds.append(f"CREATE INDEX ON :{type_name}(type);")
            cmds.append(f"CREATE INDEX ON :{type_name}(store);")

        return cmds

    def _get_auth_model_save_cmd(self, auth_model: AuthModel) -> str:
        data = self._model_to_blob(auth_model=auth_model)

        return f'CREATE (m:store {{id: "{auth_model.id}", data: "{data}"}});'

    def create_indexes(
        self, auth_model: AuthModel, tx: Optional[Transaction] = None
    ) -> None:
        index_cms = self._get_auth_model_create_indexes_cmds(auth_model=auth_model)
        if tx:
            for cmd in index_cms:
                tx.run(cmd)
        else:
            with self._driver.session(database="memgraph") as session:
                for cmd in index_cms:
                    session.run(cmd)

    def save(self, auth_model: AuthModel, tx: Optional[Transaction] = None) -> str:
        save_cmd = self._get_auth_model_save_cmd(auth_model=auth_model)
        if tx:
            tx.run(save_cmd)
        else:
            with self._driver.session(database="memgraph") as session:
                session.run(save_cmd, database_="memgraph")

        return auth_model.id

    def delete(self, auth_model_id: str, tx: Optional[Transaction] = None) -> None:
        delete_cmd = f'MATCH (m:store {{id: "{auth_model_id}"}}) DELETE m'

        if tx:
            tx.run(delete_cmd)
        else:
            with self._driver.session(database="memgraph") as session:
                session.run(delete_cmd, database_="memgraph")

    def get_model_config(self, store_id: str) -> Optional[AuthModel]:
        with self._driver.session(database="memgraph") as session:
            result = session.run(
                f'MATCH (m:store {{id: "{store_id}"}}) RETURN m.data AS blob'
            )

            try:
                blob = result.data()[0]["blob"]
            except IndexError:
                return None

            return self._blob_to_model(blob=blob)
