from __future__ import annotations

from datetime import datetime
from typing import Dict

import jwt

from backend import settings
from backend.core import constants
from backend.core.entites import User
from backend.core.utils import get_now
from datetime import timezone


class JWTService:
    ALGORITHM = "HS256"

    def __init__(self, user: User) -> None:
        self._user = user

    def _get_access_token_data(self) -> dict:
        user_data = self._user.as_dict

        return {
            "user_id": user_data["id"],
            "iat": int(get_now().timestamp()),
            "kind": constants.JWTTokenKind.ACCESS.value,
        }

    def _get_refresh_token_data(self) -> dict:
        user_data = self._user.as_dict

        return {
            "user_id": user_data["id"],
            "iat": int(get_now().timestamp()),
            "kind": constants.JWTTokenKind.REFRESH.value,
        }

    @classmethod
    def _decode_token(cls, token: str) -> Dict:
        try:
            return jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=[cls.ALGORITHM]
            )
        except (ValueError, jwt.exceptions.DecodeError) as exc:
            raise ValueError("invalid token") from exc

    @classmethod
    def setup_from_access_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    @classmethod
    def setup_from_refresh_jwt(cls) -> JWTService:
        return cls(user=User(email="a", password="b"))

    @classmethod
    def get_refresh_token_payload(cls, refresh_token: str):
        payload = cls._decode_token(token=refresh_token)
        iat = payload.pop("iat", None)
        if not iat:
            raise ValueError("invalid token")

        iat_datetime = datetime.fromtimestamp(iat).astimezone(tz=timezone.utc)
        ttl_delta = get_now() - iat_datetime
        if ttl_delta.seconds > settings.JWT_REFRESH_TTL:
            raise ValueError("outdated token")

        return payload

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
