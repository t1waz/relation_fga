import os
import signal
import socket
import subprocess
import time
from typing import List
from backend.core.entites import User
from backend.repositories import user_repository

import pytest

TEST_PORT = 8000  # TODO
TEST_DOMAIN = "0.0.0.0"   # TODO


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
        except Exception as _: # type: ignore
            print(_, 'eaaaa', domain, port)
    return process


@pytest.fixture(scope="session", autouse=True)
def session():
    process = start_server(domain=TEST_DOMAIN, port=TEST_PORT)
    yield
    kill_process(process)


@pytest.fixture
async def f_user_1():
    user = User(email="example@example.com", password="pass")
    await user_repository.save(user=user)

    yield user
