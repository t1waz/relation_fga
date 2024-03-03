import json

from robyn import SubRouter, Response
from robyn.robyn import Request

from backend.core.logic import obtain_jwt, refresh_jwt
from backend.core.utils import build_response
from backend.views.auth.schemas import ObtainTokenSchemaIn, RefreshTokenSchemaIn


auth_router = SubRouter(__name__, prefix="/auth")


@auth_router.post("/obtain-token")
async def obtain_token_view(request: Request) -> Response:
    try:
        obtain_data_in = ObtainTokenSchemaIn(**json.loads(request.body))
    except ValueError:
        return build_response(status_code=400, data={"error": "invalid request data"})

    try:
        token_data = await obtain_jwt(
            user_email=obtain_data_in.email, user_password=obtain_data_in.password
        )
    except ValueError:
        return build_response(status_code=400, data={"error": "invalid credentials"})

    return build_response(status_code=201, data=token_data)


@auth_router.options("/obtain-token")
async def obtain_token_options_view(request: Request) -> Response:
    return build_response(status_code=200, data={})


@auth_router.post("/refresh-token")
async def refresh_token_view(request: Request) -> Response:
    try:
        refresh_data_in = RefreshTokenSchemaIn(**json.loads(request.body))
    except ValueError as exc:
        return build_response(status_code=400, data={"error": str(exc)})

    try:
        token_data = await refresh_jwt(refresh_token=refresh_data_in.refresh)
    except ValueError as exc:
        return build_response(status_code=400, data={"error": str(exc)})

    return build_response(status_code=201, data=token_data)


@auth_router.options("/refresh-token")
async def refresh_token_options_view(request: Request) -> Response:
    return build_response(status_code=200, data={})
