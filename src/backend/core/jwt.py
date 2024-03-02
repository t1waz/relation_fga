from __future__ import annotations

from backend.core.entites import User


class JWTService:
    def __init__(self, user: User) -> None:
        self._user = user

    @classmethod
    def setup_from_access_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    @classmethod
    def setup_from_refresh_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    def generate_access_jwt(self) -> str:
        return "foo"

    def generate_refresh_jwt(self) -> str:
        return "bar"

    @property
    def user(self) -> User:
        return self._user
