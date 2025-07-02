import random

import httpx
from neo4j import GraphDatabase
from tqdm import tqdm

from graph_fga.entities import RelationTuple
from graph_fga.grpc.clients import GraphFgaGrpcClient
from graph_fga.repository import RelationTupleRepository
from benchmark.benchmark import settings as benchhmark_settings


RELATIONS = ["editor", "viewer"]

MAGNITUDE = 1


class GraphService:
    def __init__(self) -> None:
        self._store_id = self._setup_store_id()
        self._repo = RelationTupleRepository(
            driver=GraphDatabase.driver(
                uri=f"bolt://{benchhmark_settings.GRAPH_DB_HOST}:{benchhmark_settings.GRAPH_DB_PORT}",
                auth=("", ""),
            )
        )

    @staticmethod
    def _setup_store_id() -> str:
        client = GraphFgaGrpcClient(
            host=benchhmark_settings.GRAPH_FGA_HOST,
            port=benchhmark_settings.GRAPH_FGA_PORT,
        )

        return client.store_create(model_str=benchhmark_settings.SCHEMA)

    def save(self, relation_tuple: RelationTuple) -> None:
        self._repo.save(relation_tuple=relation_tuple, store_id=self._store_id)

    @property
    def credentials(self) -> dict:
        return {"store_id": self._store_id}


class OpenFgaService:
    def __init__(self) -> None:
        self._fga_url = f"http://{benchhmark_settings.OPENFGA_HOST}:{benchhmark_settings.OPENFGA_PORT}"
        self._store_id = self._setup_store_id()
        self._auth_id = self._setup_auth_model()

    def _setup_store_id(self) -> str:
        response = httpx.post(f"{self._fga_url}/stores", json={"name": "test"})
        if response.status_code != 201:
            raise ValueError("cannot create store")

        return response.json()["id"]

    def _setup_auth_model(self) -> str:
        response = httpx.post(
            f"{self._fga_url}/stores/{self._store_id}/authorization-models",
            json=benchhmark_settings.JSON_SCHEMA,
        )
        if response.status_code != 201:
            raise ValueError("cannot create auth model")

        return response.json()["authorization_model_id"]

    def save(self, relation_tuple: RelationTuple) -> None:
        response = httpx.post(
            f"{self._fga_url}/stores/{self._store_id}/write",
            json={
                "writes": {
                    "tuple_keys": [
                        {
                            "user": relation_tuple.source,
                            "relation": relation_tuple.relation,
                            "object": relation_tuple.target,
                        }
                    ]
                },
                "authorization_model_id": self._auth_id,
            },
        )
        if response.status_code != 200:
            raise ValueError(f"cannot create tuple {relation_tuple}")

    @property
    def credentials(self) -> dict:
        return {"store_id": self._store_id, "auth_id": self._auth_id}


def generate_test_data(graph_service: GraphService, openfga_service: OpenFgaService):
    print("loading users")
    for i in tqdm(range(int(100 * MAGNITUDE))):
        user = RelationTuple(
            source=f"user:{i}",
            target=f"unit:{random.randint(1, 100)}",
            relation="member",
        )
        try:
            graph_service.save(relation_tuple=user)
            openfga_service.save(relation_tuple=user)
        except:
            print(user)
            pass

    print("loading issues")
    for i in tqdm(range(int(10000 * MAGNITUDE))):
        issue = RelationTuple(
            source=f"user:{random.randint(1, 1000)}",
            target=f"issue:{i}",
            relation=random.choice(RELATIONS),
        )
        if random.randint(1, 10) > 3:
            issue = RelationTuple(
                source=f"user:1", target=f"issue:{i}", relation=random.choice(RELATIONS)
            )
        try:
            graph_service.save(relation_tuple=issue)
            openfga_service.save(relation_tuple=issue)
        except:
            print(issue)
            pass

    print("loading unit issue")
    for _ in tqdm(range(int(500 * MAGNITUDE))):
        unit = RelationTuple(
            source=f"unit:{random.randint(1, 100)}#member",
            target=f"issue:{random.randint(1, 100000)}",
            relation=random.choice(RELATIONS),
        )
        try:
            graph_service.save(relation_tuple=unit)
            openfga_service.save(relation_tuple=unit)
        except:
            print(unit)
            pass


if __name__ == "__main__":
    graph_service = GraphService()
    openfga_service = OpenFgaService()
    generate_test_data(graph_service=graph_service, openfga_service=openfga_service)

    print(f"graph -> {graph_service.credentials}")
    print(f"openfga -> {openfga_service.credentials}")
