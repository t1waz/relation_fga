import httpx
from backend.core.entites import User
from backend.core.jwt import JWTService


TEST_PORT = 8000
TEST_DOMAIN = "127.0.0.1"


async def make_test_get(path: str) -> httpx.Response:
    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.get(f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}")


async def make_test_post(path: str, data: dict) -> httpx.Response:
    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.post(
            f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}",
            json=data,
            headers={"content-type": "application/json"},
        )


async def make_test_auth_get(path: str, user: User) -> httpx.Response:
    access_token = JWTService(user=user).generate_access_jwt()

    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.get(
            f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}",
            headers={"content-type": "application/json", "authorization": f"Bearer {access_token}"},   # TODO
        )


async def make_test_auth_post(path: str, data: dict, user: User) -> httpx.Response:
    access_token = JWTService(user=user).generate_access_jwt()

    path = path.strip("/")
    async with httpx.AsyncClient() as client:
        return await client.post(
            f"http://{TEST_DOMAIN}:{TEST_PORT}/{path}",
            json=data,
            headers={"content-type": "application/json", "authorization": f"Bearer {access_token}"},   # TODO
        )
