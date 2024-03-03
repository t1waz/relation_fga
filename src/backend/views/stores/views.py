import json

from robyn import SubRouter, Response
from robyn.robyn import Request

from backend.core import constants
from backend.core.entites import User
from backend.core.logic import handle_create_store
from backend.core.utils import build_response
from backend.repositories import store_repository
from backend.utils import jwt_required
from backend.views.stores.schemas import CreateStoreSchemaIn


stores_router = SubRouter(__name__, prefix="/stores")


@stores_router.get("")
@jwt_required
async def get_all_stores(request: Request) -> Response:
    print(request.identity.claims["user"], '!!!!!')
    return build_response(
        status_code=200,
        data=[
            {
                "id": str(store.id),
                "name": store.name,
                "created_at": store.created_at.strftime(constants.DATETIME_FORMAT),
            }
            for store in await store_repository.get_all()
        ],
    )


@stores_router.options("")
async def get_all_stores_options_view(request: Request) -> Response:
    return build_response(status_code=200, data={})


@stores_router.post("")
@jwt_required
async def create_store(request: Request) -> Response:
    try:
        refresh_data_in = CreateStoreSchemaIn(**json.loads(request.body))
    except ValueError as exc:
        return build_response(status_code=400, data={"error": str(exc)})

    store = await handle_create_store(user=User.from_dict(**json.loads(request.identity.claims["user"])), **refresh_data_in.dict())

    return build_response(
        status_code=201,
        data={
            "id": str(store.id),
            "name": store.name,
            "auth_token": store.auth_token,
            "created_at": store.created_at.strftime(constants.DATETIME_FORMAT),
        }
    )
