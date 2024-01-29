# import asyncio
#
# import pytest
# from httpx import AsyncClient
# from _pytest.fixtures import SubRequest
# from main import app
#
#
# @pytest.fixture(scope="session")
# def event_loop(request: SubRequest):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#
#     yield loop
#
#     loop.close()
#
#
# @pytest.fixture(scope="function")
# def test_client() -> AsyncClient:
#     yield AsyncClient(app=app, base_url='http://testserver')
#
