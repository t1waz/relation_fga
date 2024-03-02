from __future__ import annotations

import jwt

from backend.core import constants
from backend.core.entites import User
from backend import settings
from backend.core.utils import get_now


class JWTService:
    ALGORITHM = "HS256"

    def __init__(self, user: User) -> None:
        self._user = user

    def _get_access_token_data(self) -> dict:
        return {
            "iat": get_now(),
            "id": self._user.id,
            "kind": constants.JWTTokenKind.ACCESS.value,
        }

    def _get_refresh_token_data(self) -> dict:
        return {
            "iat": get_now(),
            "id": self._user.id,
            "kind": constants.JWTTokenKind.REFRESH.value,
        }

    @classmethod
    def setup_from_access_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    @classmethod
    def setup_from_refresh_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    def generate_access_jwt(self) -> str:
        return jwt.encode(
            key=settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
            payload=self._get_access_token_data(),
        )

    def generate_refresh_jwt(self) -> str:
        return jwt.encode(
            key=settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
            payload=self._get_refresh_token_data(),
        )

    @property
    def user(self) -> User:
        return self._user
