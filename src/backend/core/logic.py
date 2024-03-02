from backend.core.jwt import JWTService
from backend.repositories import user_repository


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
