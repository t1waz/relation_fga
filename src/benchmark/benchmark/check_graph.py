import time

from benchmark.benchmark.settings import *
from graph_fga.grpc.clients import GraphFgaGrpcClient


STORE_ID = "6136ac0b-3379-4c97-8c0b-c6cc31aaa2c7"


if __name__ == "__main__":
    client = GraphFgaGrpcClient(host=GRAPH_FGA_HOST, port=GRAPH_FGA_PORT)

    t1 = time.time()
    objects = client.store_list_objects(
        store_id=STORE_ID, user="user:1", permission="can_view", type="issue"
    )
    t2 = time.time()
    print(len(objects), t2 - t1)
