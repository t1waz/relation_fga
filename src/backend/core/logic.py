import secrets
import string

from robyn import Request

from backend.core.entites import User, Store
from backend.core.jwt import JWTService
from backend.repositories import user_repository, store_repository


def generate_store_auth_token():
    characters = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(characters) for _ in range(256))

    return secure_string


async def obtain_jwt(user_email: str, user_password: str) -> dict:
    user = await user_repository.get_from_email(user_email=user_email)

    if not user or user.password != user_password:
        raise ValueError("invalid credentials")

    jwt_service = JWTService(user=user)

    return {
        "access": jwt_service.generate_access_jwt(),
        "refresh": jwt_service.generate_refresh_jwt(),
    }


async def refresh_jwt(refresh_token: str) -> dict:
    refresh_token_data = JWTService.get_refresh_token_payload(
        refresh_token=refresh_token
    )
    user_id = refresh_token_data.get("user_id")
    if not user_id:
        raise ValueError("invalid token data")

    user = await user_repository.get_from_id(id=user_id)
    if not user:
        raise ValueError("invalid token user")

    jwt_service = JWTService(user=user)

    return {
        "access": jwt_service.generate_access_jwt(),
        "refresh": jwt_service.generate_refresh_jwt(),
    }


async def request_jwt_user(request: Request) -> User:
    try:
        request_token = request.headers.get("authorization")
    except (KeyError, TypeError) as exc:
        raise ValueError("login required") from exc

    access_token_data = JWTService.get_access_token_payload_from_header(header_token=request_token)
    user_id = access_token_data.get("user_id")
    if not user_id:
        raise ValueError("invalid token data")

    user = await user_repository.get_from_id(id=user_id)
    if not user:
        raise ValueError("invalid token user")

    return user


async def handle_create_store(user: User, **store_data) -> Store:
    store_data["owner"] = user
    store_data["auth_token"] = generate_store_auth_token()

    store = Store(**store_data)

    await store_repository.save(store=store)

    return store
