from typing import List, Union, Optional, Dict

import grpc

from graph_fga.entities import RelationTuple
from graph_fga.grpc.pb2 import messages_pb2
from graph_fga.grpc.pb2 import services_pb2_grpc


class GraphFgaGrpcClient:
    def __init__(self, host: str, port: Union[str, int]) -> None:
        self._stub = services_pb2_grpc.GraphFgaServiceStub(
            channel=grpc.insecure_channel(f"{host}:{port}")
        )

    def store_create(self, model_str: str) -> str:
        response = self._stub.store_create(
            messages_pb2.StoreCreateRequest(model=model_str)
        )

        return response.store_id

    def store_read(
        self,
        store_id,
        source_type: str,
        source_id: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> List[RelationTuple]:
        response = self._stub.store_read(
            messages_pb2.StoreReadRequest(
                store_id=store_id,
                relation=relation,
                source=messages_pb2.StoreReadObj(
                    id=source_id,
                    type=source_type,
                ),
                target=messages_pb2.StoreReadObj(
                    id=target_id,
                    type=target_type,
                ),
            )
        )

        return [
            RelationTuple(source=d.user, relation=d.relation, target=d.object)
            for d in response.objects
        ]

    def store_write(
        self, store_id: str, writes: List[RelationTuple], deletes: List[RelationTuple]
    ) -> str:
        response = self._stub.store_write(
            messages_pb2.StoreWriteRequest(
                store_id=store_id,
                writes=[
                    messages_pb2.StoreRelationTuple(
                        user=w.source, relation=w.relation, object=w.target
                    )
                    for w in writes
                ],
                deletes=[
                    messages_pb2.StoreRelationTuple(
                        user=w.source, relation=w.relation, object=w.target
                    )
                    for w in deletes
                ],
            )
        )

        return response.status

    def store_check(
        self,
        store_id: str,
        user: str,
        object: str,
        permission: str,
        contextual_tuples: Optional[List[Dict]] = None,
    ) -> bool:
        response = self._stub.store_check(
            messages_pb2.StoreCheckRequest(
                user=user,
                object=object,
                store_id=store_id,
                permission=permission,
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=d["user"], relation=d["relation"], object=d["object"]
                    )
                    for d in contextual_tuples or []
                ],
            )
        )

        return response.allowed

    def store_list_objects(
        self,
        store_id,
        user: str,
        permission: str,
        type: str,
        contextual_tuples: Optional[List[Dict]] = None,
    ) -> List[str]:
        response = self._stub.store_list_objects(
            messages_pb2.StoreListObjectsRequest(
                user=user,
                type=type,
                store_id=store_id,
                permission=permission,
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=d["user"], relation=d["relation"], object=d["object"]
                    )
                    for d in contextual_tuples or []
                ],
            )
        )

        return response.objects
