from robyn import SubRouter, Response
from robyn.robyn import Request

from backend.core.utils import build_response
from backend.repositories import store_repository
from backend.core import constants

stores_router = SubRouter(__name__, prefix="/stores")


@stores_router.get("")
async def get_all_stores(request: Request) -> Response:
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
