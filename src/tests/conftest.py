import pytest

import graph_fga.grpc.pb2.services_pb2_grpc as services_pb2_grpc
from server_grpc.main import GraphFgaServicer
from graph_fga.interpreter.auth_model import AuthModel
from graph_fga.repository import AuthModelRepository, RelationTupleRepository
from neo4j import GraphDatabase


@pytest.fixture(scope="module")
def grpc_add_to_server():
    yield services_pb2_grpc.add_GraphFgaServiceServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    yield GraphFgaServicer()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    yield services_pb2_grpc.GraphFgaServiceStub(grpc_channel)


@pytest.fixture(scope="session")
def graph_driver():
    yield GraphDatabase.driver(uri="bolt://graph-db:7687", auth=("", ""))


@pytest.fixture(autouse=True)
def clear_graph_db(graph_driver):
    yield
    with graph_driver.session(database="memgraph") as session:
        session.run("MATCH (n) DETACH DELETE n;")


@pytest.fixture(scope="session")
def model_config_repository(graph_driver):
    yield AuthModelRepository(driver=graph_driver)


@pytest.fixture(scope="session")
def relation_tuple_repository(graph_driver):
    yield RelationTupleRepository(driver=graph_driver)


@pytest.fixture
def f_auth_model_1(model_config_repository):
    config = """
    type user

    type foo
      relations
        define manager: [user]
    
    type group
      relations
        define comrade: [user, foo#manager]
        define root: [group]
    
    type issue
      relations
        define manager: [user, group, group#comrade]
        define viewer: [user, group]
        define can_edit: viewer or manager
        define can_view: manager or viewer      
    """
    auth_model_1 = AuthModel(config=config)
    model_config_repository.save(auth_model=auth_model_1)

    yield auth_model_1


@pytest.fixture
def f_auth_model_2(model_config_repository):
    config = """
    type user

    type group
      relations
        define comrade: [user]
        define root: [group]
    
    type issue
      relations
        define owner: [user]
        define root: [group, user]
    
    type document
      relations
        define attached: [issue, user]
        define manager: [user, group, group#comrade]
        define owner: [user]
        define root: [group]
        define participant: [user]
        define viewer: [user, group, group#comrade]
    
    type bar
      relations
        define attached: [issue]
        define can_edit: task_manager or manager or owner
        define can_view: task_viewer or can_edit or viewer or participant
        define manager: [user, group, group#comrade]
        define owner: [user]
        define root: [group]
        define participant: [user]
        define viewer: [user, group, group#comrade]
    """
    auth_model_2 = AuthModel(config=config)
    model_config_repository.save(auth_model=auth_model_2)

    yield auth_model_2


@pytest.fixture
def f_auth_model_3(model_config_repository):
    config = """
    type user

    type group
      relations
        define comrade: [user]
    
    
    type issue
      relations
        define attached: [task]
        define can_edit: can_edit from attached or viewer
        define viewer: [user]
    
    type task
      relations
        define can_edit: manager or owner
        define manager: [user]
        define owner: [user]
    """
    auth_model_3 = AuthModel(config=config)
    model_config_repository.save(auth_model=auth_model_3)

    yield auth_model_3


@pytest.fixture
def f_auth_model_4(model_config_repository):
    config = """
    type user

    type group
      relations
        define comrade: [user]
    
    type issue
      relations
        define attached: [task]
        define can_edit: can_edit from attached or manager or owner
        define manager: [user]
        define owner: [user]
    
    type task
      relations
        define can_edit: manager or owner
        define manager: [user, group, group#comrade]
        define owner: [user]
    """

    auth_model_4 = AuthModel(config=config)
    model_config_repository.save(auth_model=auth_model_4)

    yield auth_model_4


@pytest.fixture
def f_auth_model_5(model_config_repository):
    config = """
    type user

    type group
      relations
        define comrade: [user]
    
    type issue
      relations
        define attached: [ticket]
        define can_edit: can_edit from attached or manager or owner
        define can_view: can_view from attached or can_edit or tribe_member
        define manager: [user]
        define tribe_member: [user]
        define owner: [user]
    
    type ticket
      relations
        define attached: [parcel]
        define can_edit: can_edit from attached or owner or manager
        define can_view: can_edit or viewer or tribe_member
        define manager: [user, group, group#comrade]
        define owner: [user]
        define master: [group]
        define tribe_member: [user]
        define viewer: [user, group, group#member]
    
    type parcel
      relations
        define can_edit: manager or owner
        define manager: [user, group, group#comrade]
        define owner: [user]
    """
    auth_model_5 = AuthModel(config=config)
    model_config_repository.save(auth_model=auth_model_5)

    yield auth_model_5
