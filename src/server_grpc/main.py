from concurrent import futures

import grpc
from google.protobuf.message import Message

import graph_fga.grpc.pb2.messages_pb2 as messages_pb2
import graph_fga.grpc.pb2.services_pb2_grpc as services_pb2_grpc
from graph_fga.entities import RelationTuple, CheckRequest, ListObjectsRequest
from graph_fga.exceptions import InvalidRelationTupleException
from graph_fga.interpreter.auth_model import AuthModel
from graph_fga.logger import logger
from server_grpc.exceptions import InvalidRequestException
from server_grpc.exceptions import handle_exception
from server_grpc.repositories import model_config_repository
from server_grpc.services import StoreLogic
from server_grpc.settings import settings


def get_store_logic_from_request(request: Message) -> StoreLogic:
    store_id = getattr(request, "store_id", None)
    if not store_id:
        raise InvalidRequestException("invalid/missing store_id")

    try:
        return StoreLogic.setup(store_id=store_id)
    except ValueError as exc:
        raise InvalidRequestException("invalid store_id") from exc


class GraphFgaServicer(services_pb2_grpc.GraphFgaServiceServicer):
    @handle_exception
    def store_create(
        self, request: messages_pb2.StoreCreateRequest, context: grpc.ServicerContext
    ) -> messages_pb2.StoreCreateResponse:
        try:
            auth_model = AuthModel(config=request.model)
        except Exception as _:
            raise InvalidRequestException("invalid model")

        if not auth_model.is_valid:
            raise InvalidRequestException("invalid model")

        model_config_repository.save(auth_model=auth_model)
        model_config_repository.create_indexes(auth_model=auth_model)

        return messages_pb2.StoreCreateResponse(status="ok", store_id=auth_model.id)

    @handle_exception
    def store_write(
        self, request: messages_pb2.StoreWriteRequest, context: grpc.ServicerContext
    ) -> messages_pb2.StoreWriteResponse:
        store_logic = get_store_logic_from_request(request=request)

        writes = [
            RelationTuple(source=d.user, target=d.object, relation=d.relation)
            for d in request.writes
        ]
        deletes = [
            RelationTuple(source=d.user, target=d.object, relation=d.relation)
            for d in request.deletes
        ]
        writes = [r for r in writes if r not in deletes]

        try:
            store_logic.validate_relation_tuples(relation_tuples=[*writes, *deletes])
        except (ValueError, InvalidRelationTupleException) as exc:
            raise InvalidRequestException(str(exc))

        store_logic.persist_relation_tuples(
            writes=writes, deletes=deletes, skip_validation=True
        )

        return messages_pb2.StoreWriteResponse(status="ok")

    @handle_exception
    def store_read(
        self, request: messages_pb2.StoreReadRequest, context: grpc.ServicerContext
    ) -> messages_pb2.StoreReadResponse:
        source_id = getattr(request.source, "id", None)
        target_id = getattr(request.target, "id", None)
        source_type = getattr(request.source, "type", None)
        target_type = getattr(request.target, "type", None)

        if not source_type:
            raise InvalidRequestException("missing source type")
        if target_id and not target_type:
            raise InvalidRequestException("missing target type for target id")

        store_logic = get_store_logic_from_request(request=request)
        relation_tuples = store_logic.list_relations(
            source_id=source_id,
            target_id=target_id,
            target_type=target_type,
            source_type=source_type,
        )

        return messages_pb2.StoreReadResponse(
            objects=[
                messages_pb2.StoreRelationTuple(
                    user=t.source, object=t.target, relation=t.relation
                )
                for t in relation_tuples
            ]
        )

    @handle_exception
    def store_check(
        self, request: messages_pb2.StoreCheckRequest, context: grpc.ServicerContext
    ) -> messages_pb2.StoreCheckResponse:
        store_logic = get_store_logic_from_request(request=request)

        return messages_pb2.StoreCheckResponse(
            allowed=store_logic.is_allowed(
                check_request=CheckRequest(
                    source=request.user,
                    target=request.object,
                    permission=request.permission,
                )
            )
        )

    @handle_exception
    def store_list_objects(
        self,
        request: messages_pb2.StoreListObjectsRequest,
        context: grpc.ServicerContext,
    ) -> messages_pb2.StoreListObjectsResponse:
        store_logic = get_store_logic_from_request(request=request)

        return messages_pb2.StoreListObjectsResponse(
            objects=store_logic.list_objects(
                list_objects_request=ListObjectsRequest(
                    source=request.user,
                    target_type=request.type,
                    permission=request.permission,
                )
            )
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS))
    services_pb2_grpc.add_GraphFgaServiceServicer_to_server(
        GraphFgaServicer(), server=server
    )

    server.add_insecure_port(f"[::]:9999")
    logger.info("started")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
