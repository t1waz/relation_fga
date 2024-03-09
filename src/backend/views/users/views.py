from robyn import SubRouter, Response
from robyn.robyn import Request

from backend.core.entites import User
from backend.core.utils import build_response
from backend.utils import jwt_required

users_router = SubRouter(__name__, prefix="/users")


@users_router.get("/me")
@jwt_required
async def me(request: Request) -> Response:
    user = User.from_request(request=request)

    return build_response(
        status_code=200,
        data={
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "second_name": user.second_name,
        },
    )
