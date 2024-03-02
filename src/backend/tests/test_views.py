import pytest
import httpx


TEST_PORT = 8000
TEST_DOMAIN = "127.0.0.1"


async def get(path: str) -> httpx.Response:
    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.get(f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}")


async def post(path: str, data: dict) -> httpx.Response:
    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.post(f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}", json=data, headers={"content-type": "application/json"})


class TestHealthCheck:
    ENDPOINT = "/health"

    async def test_health_check_endpoint_is_working(self):
        response = await get("/health")

        assert response.status_code == 200


class TestObtainTokenView:
    ENDPOINT = "/auth/obtain-token"

    async def test_obtain_token_data_valid_request(self, f_user_1):
        response = await post(self.ENDPOINT, data={"email": f_user_1.email, "password": f_user_1.password})
        print(response.status_code, response.text)
        assert 1 == 0
