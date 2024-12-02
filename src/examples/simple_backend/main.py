from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from graph_fga.entities import RelationTuple, CheckRequest
from graph_fga.grpc.clients import GraphFgaGrpcClient


DEFAULT_STORE_PERMISSION_MODEL = """
type user

"""

def get_or_create_default_store(fga_client: GraphFgaGrpcClient) -> str:
    existing_store_ids = fga_client.store_list()
    if existing_store_ids:
        store_id = existing_store_ids[0]
    else:
        store_id = fga_client.store_create(
            model_str=DEFAULT_STORE_PERMISSION_MODEL
        )

    return store_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    fga_client = GraphFgaGrpcClient(host="localhost", port=80)
    store_id = get_or_create_default_store(fga_client=fga_client)

    app.state.store_id = store_id
    app.state.fga_client = fga_client

    yield



app = FastAPI(
    title="FGA API demo",
    description="API for demo Fine Grained Access Control",
    lifespan=lifespan
)


@app.post(
    "/create",
    status_code=200,
    description="Create a new resource with specified permissions"
)
async def create_resource(request_data: RelationTuple, request: Request):
    relation_tuple = RelationTuple(
        source=request_data.source,
        target=request_data.target,
        relation=request_data.relation,
    )
    try:
        request.app.state.fga_client.store_write(
            store_id=request.app.state.store_id,
            writes=[relation_tuple]
        )
    except Exception as _:
        return Response(status_code=400)

    return Response(status_code=200)


@app.post(
    "/check",
    status_code=200,
    description="Check access permissions for a given user and object"
)
async def check_access(request_data: CheckRequest, request: Request):
    has_access = request.app.state.fga_client.store_check(
        user=request_data.source,
        object=request_data.target,
        permission=request_data.permission,
        store_id=request.app.state.store_id,
    )

    if has_access:
        return Response(status_code=200)

    return Response(status_code=403)
