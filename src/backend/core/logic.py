from backend.core.jwt import JWTService
from backend.repositories import user_repository


async def obtain_jwt_logic(user_email: str, user_password: str) -> dict:
    user = await user_repository.get_from_email(user_email=user_email)

    if not user or user.password != user_password:
        raise ValueError("invalid credentials")

    jwt_service = JWTService(user=user)

    return {
        "access": jwt_service.generate_access_jwt(),
        "refresh": jwt_service.generate_refresh_jwt(),
    }
