import json
from typing import Dict

from robyn import SubRouter, status_codes, Response, jsonify, Headers
from robyn.robyn import Request

from backend.core.logic import obtain_jwt_logic
from backend.views.auth.schemas import ObtainTokenSchemaIn


auth_router = SubRouter(__name__, prefix="/auth")


@auth_router.post(f"/obtain-token")
async def obtain_token_view(request: Request) -> Response:
    print(request, dir(request), request.body, type(request.body), json.loads(request.body))
    try:
        data_in = ObtainTokenSchemaIn(**json.loads(request.body))
    except ValueError:
        return Response(status_code=400, headers=Headers({}), description=json.dumps({"error": "invalid request format"}))

    try:
        token_data = await obtain_jwt_logic(user_email=data_in.email, user_password=data_in.password)
    except ValueError:
        return Response(status_code=400, headers=Headers({}), description=json.dumps({"error": "invalid credentials"}))

    return Response(
        status_code=200,
        headers=Headers({}),
        description=json.dumps(token_data),
    )

