import asyncio
import os
import signal
import socket
import subprocess
import time
import uuid
from typing import List

import pytest
from _pytest.fixtures import SubRequest

from backend.core.entites import User, Store
from backend.repositories import user_repository, store_repository


TEST_PORT = 8000  # TODO
TEST_DOMAIN = "0.0.0.0"  # TODO


@pytest.fixture(scope="session")
def event_loop(request: SubRequest):  # TODO typing
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()


def spawn_process(command: List[str]) -> subprocess.Popen:
    process = subprocess.Popen(command, preexec_fn=os.setsid)
    return process


def kill_process(process: subprocess.Popen) -> None:
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except ProcessLookupError:
        pass


def start_server(domain: str, port: int) -> subprocess.Popen:
    process = spawn_process(["python", "backend/main.py"])

    # Wait for the server to be reachable
    timeout = 5  # The maximum time we will wait for an answer
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            kill_process(process)
            raise ConnectionError("Could not reach Robyn server")
        try:
            sock = socket.create_connection((domain, port), timeout=5)
            sock.close()
            break
        except Exception as _:  # type: ignore
            pass
    return process


@pytest.fixture(scope="session", autouse=True)
def session():
    process = start_server(domain=TEST_DOMAIN, port=TEST_PORT)
    yield
    kill_process(process)


@pytest.fixture
async def f_user_1():
    user_1 = User(email="example@example.com", password="pass")
    await user_repository.save(user=user_1)

    yield user_1

    await user_repository.delete(user=user_1)


@pytest.fixture
async def f_store_1(f_user_1):
    store_1 = Store(name="store_1", owner=f_user_1)
    await store_repository.save(store=store_1)

    yield store_1

    await store_repository.delete(store=store_1)


@pytest.fixture
async def f_store_2(f_user_1):
    store_2 = Store(name="store_2", owner=f_user_1)
    await store_repository.save(store=store_2)

    yield store_2

    await store_repository.delete(store=store_2)


@pytest.fixture
async def f_store_3(f_user_1):
    store_3 = Store(name="store_3", owner=f_user_1)
    await store_repository.save(store=store_3)

    yield store_3

    await store_repository.delete(store=store_3)
