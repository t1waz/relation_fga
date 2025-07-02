import time

from benchmark.benchmark import settings as benchhmark_settings
from graph_fga.grpc.clients import GraphFgaGrpcClient


STORE_ID = "19f133bc-f19b-4fd5-b616-280449441d50"


if __name__ == "__main__":
    client = GraphFgaGrpcClient(
        host=benchhmark_settings.GRAPH_FGA_HOST, port=benchhmark_settings.GRAPH_FGA_PORT
    )

    for _ in range(100):
        t1 = time.time()
        objects = client.store_list_objects(
            store_id=STORE_ID, user="user:1", permission="can_view", type="issue"
        )
        t2 = time.time()
        print(t2 - t1)
