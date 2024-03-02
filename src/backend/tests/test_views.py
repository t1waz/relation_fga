import datetime

import pytest
from freezegun import freeze_time

from backend import settings
from backend.core.jwt import JWTService
from backend.core.utils import get_now
from backend.tests.utils import make_test_get, make_test_post


class TestHealthCheck:
    ENDPOINT = "/health"

    async def test_health_check_endpoint_is_working(self):
        response = await make_test_get("/health")

        assert response.status_code == 200

    async def test_health_check_endpoint_post_request(self):
        response = await make_test_post(self.ENDPOINT, data={})

        assert response.status_code == 404


class TestObtainTokenView:
    ENDPOINT = "/auth/obtain-token"

    async def test_obtain_token_data_get_request(self):
        response = await make_test_get(self.ENDPOINT)

        assert response.status_code == 404

    async def test_obtain_token_data_missing_password(self, f_user_1):
        response = await make_test_post(self.ENDPOINT, data={"email": f_user_1.email})

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_missing_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"password": f_user_1.password}
        )

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_empty_data(self):
        response = await make_test_post(self.ENDPOINT, data={})

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_email_not_a_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": "not_a_email", "password": f_user_1.password}
        )

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_not_existing_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT,
            data={"email": "aa@example.com", "password": f_user_1.password},
        )

        assert response.status_code == 400
        assert "credentials" in response.text

    async def test_obtain_token_data_invalid_password(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": f_user_1.email, "password": "invalid"}
        )

        assert response.status_code == 400
        assert "credentials" in response.text

    async def test_obtain_token_data_valid_request(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": f_user_1.email, "password": f_user_1.password}
        )

        assert response.status_code == 201

        data = response.json()

        assert "access" in data
        assert "refresh" in data
        assert len(data["access"]) > 10
        assert len(data["refresh"]) > 10


class TestRefreshTokenView:
    ENDPOINT = "/auth/refresh-token"

    async def test_refresh_token_get_request(self):
        response = await make_test_get(self.ENDPOINT)

        assert response.status_code == 404

    async def test_refresh_token_empty_post(self):
        response = await make_test_post(self.ENDPOINT, data={})

        assert response.status_code == 400
        assert "refresh" in response.text

    async def test_refresh_token_missing_refresh(self):
        response = await make_test_post(self.ENDPOINT, data={"foo": "bar"})

        assert response.status_code == 400
        assert "refresh" in response.text

    @pytest.mark.parametrize("invalid_refresh", [123, 3.14, False, "", "aaa"])
    async def test_refresh_token_invalid_token_data(self, invalid_refresh):
        response = await make_test_post(
            self.ENDPOINT, data={"refresh": invalid_refresh}
        )

        assert response.status_code == 400

    async def test_refresh_token_not_app_token(self):
        invalid_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
            "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        )

        response = await make_test_post(self.ENDPOINT, data={"refresh": invalid_token})

        assert response.status_code == 400

    async def test_refresh_token_outdated_refresh(self, f_user_1):
        with freeze_time(
            get_now() - datetime.timedelta(seconds=settings.JWT_REFRESH_TTL + 1)
        ):
            refresh_jwt = JWTService(user=f_user_1).generate_refresh_jwt()

        response = await make_test_post(self.ENDPOINT, data={"refresh": refresh_jwt})

        assert response.status_code == 400
        assert "outdated" in response.text

    async def test_refresh_token_valid_refresh(self, f_user_1):
        refresh_jwt = JWTService(user=f_user_1).generate_refresh_jwt()

        response = await make_test_post(self.ENDPOINT, data={"refresh": refresh_jwt})

        assert response.status_code == 201

        data = response.json()

        assert "access" in data
        assert "refresh" in data
        assert len(data["access"]) > 10
        assert len(data["refresh"]) > 10


class TestGetStoresView:
    ENDPOINT = "/stores/"

    async def test_get_stores(self, f_store_1, f_store_2, f_store_3):
        response = await make_test_get(self.ENDPOINT)

        assert response.status_code == 200

        data = response.json()

        assert {d["id"] for d in data} == {f_store_1.id, f_store_2.id, f_store_3.id}
        assert {d["name"] for d in data} == {f_store_1.name, f_store_2.name, f_store_3.name}
