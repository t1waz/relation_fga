import time

from benchmark.benchmark.settings import *
from graph_fga.grpc.clients import GraphFgaGrpcClient


STORE_ID = "e3fd79be-bf48-46ea-977e-e4b3e93086cb"


if __name__ == "__main__":
    client = GraphFgaGrpcClient(host=GRAPH_FGA_HOST, port=GRAPH_FGA_PORT)

    for _ in range(100):
        t1 = time.time()
        objects = client.store_list_objects(
            store_id=STORE_ID, user="user:1", permission="can_view", type="issue"
        )
        t2 = time.time()
        print(t2 - t1)
