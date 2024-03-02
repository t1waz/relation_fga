import json

from robyn import SubRouter, Response
from robyn.robyn import Request

from backend.core.logic import obtain_jwt_logic
from backend.core.utils import build_response
from backend.views.auth.schemas import ObtainTokenSchemaIn


auth_router = SubRouter(__name__, prefix="/auth")


@auth_router.post(f"/obtain-token")
async def obtain_token_view(request: Request) -> Response:
    try:
        data_in = ObtainTokenSchemaIn(**json.loads(request.body))
    except ValueError:
        return build_response(status_code=400, data={"error": "invalid request data"})

    try:
        token_data = await obtain_jwt_logic(
            user_email=data_in.email, user_password=data_in.password
        )
    except ValueError:
        return build_response(status_code=400, data={"error": "invalid credentials"})

    return build_response(status_code=201, data=token_data)
