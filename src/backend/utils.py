import functools
import json

from robyn import Request
from robyn.authentication import Identity

from backend.core.logic import request_jwt_user
from backend.core.utils import build_response


def jwt_required(func):
    @functools.wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            user = await request_jwt_user(request=request)
        except ValueError as exc:
            return build_response(status_code=403, data={"error": str(exc)})

        request.identity = Identity(claims={"user": json.dumps(user.as_dict)})

        return await func(request, *args, **kwargs)

    return wrapper
