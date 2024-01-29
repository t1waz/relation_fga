from neo4j import GraphDatabase

from graph_fga.repository import AuthModelRepository, RelationTupleRepository
from server_grpc.settings import settings


fga_driver = GraphDatabase.driver(
    uri=f"bolt://{settings.GRAPH_DB_HOST}:{settings.GRAPH_DB_PORT}", auth=("", "")
)

model_config_repository = AuthModelRepository(driver=fga_driver)

relation_tuple_repository = RelationTupleRepository(driver=fga_driver)
