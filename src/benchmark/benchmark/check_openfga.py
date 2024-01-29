import time

import httpx

from benchmark.benchmark.settings import *

FGA_URL = f"http://{OPENFGA_HOST}:{OPENFGA_PORT}"


if __name__ == "__main__":
    response = httpx.get(f"{FGA_URL}/stores")
    store_id = response.json()["stores"][-1]["id"]

    response = httpx.get(f"{FGA_URL}/stores/{store_id}/authorization-models")
    auth_id = response.json()["authorization_models"][0]["id"]

    for _ in range(100):
        t1 = time.time()
        response = httpx.post(
            f"{FGA_URL}/stores/{store_id}/list-objects",
            json={
                "authorization_model_id": auth_id,
                "type": "issue",
                "relation": "can_view",
                "user": "user:1",
            },
            timeout=None,
        )
        t2 = time.time()
        objs = response.json()["objects"]

        print(t2 - t1)
