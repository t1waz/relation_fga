# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import messages_pb2 as messages__pb2


class GraphFgaServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.store_view = channel.unary_unary(
            "/GraphFgaService/store_view",
            request_serializer=messages__pb2.StoreViewRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreViewResponse.FromString,
        )
        self.store_create = channel.unary_unary(
            "/GraphFgaService/store_create",
            request_serializer=messages__pb2.StoreCreateRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreCreateResponse.FromString,
        )
        self.store_update = channel.unary_unary(
            "/GraphFgaService/store_update",
            request_serializer=messages__pb2.StoreUpdateRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreUpdateResponse.FromString,
        )
        self.store_list = channel.unary_unary(
            "/GraphFgaService/store_list",
            request_serializer=messages__pb2.StoreListRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreListResponse.FromString,
        )
        self.store_read = channel.unary_unary(
            "/GraphFgaService/store_read",
            request_serializer=messages__pb2.StoreReadRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreReadResponse.FromString,
        )
        self.store_write = channel.unary_unary(
            "/GraphFgaService/store_write",
            request_serializer=messages__pb2.StoreWriteRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreWriteResponse.FromString,
        )
        self.store_check = channel.unary_unary(
            "/GraphFgaService/store_check",
            request_serializer=messages__pb2.StoreCheckRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreCheckResponse.FromString,
        )
        self.store_list_objects = channel.unary_unary(
            "/GraphFgaService/store_list_objects",
            request_serializer=messages__pb2.StoreListObjectsRequest.SerializeToString,
            response_deserializer=messages__pb2.StoreListObjectsResponse.FromString,
        )


class GraphFgaServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def store_view(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_check(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def store_list_objects(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_GraphFgaServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "store_view": grpc.unary_unary_rpc_method_handler(
            servicer.store_view,
            request_deserializer=messages__pb2.StoreViewRequest.FromString,
            response_serializer=messages__pb2.StoreViewResponse.SerializeToString,
        ),
        "store_create": grpc.unary_unary_rpc_method_handler(
            servicer.store_create,
            request_deserializer=messages__pb2.StoreCreateRequest.FromString,
            response_serializer=messages__pb2.StoreCreateResponse.SerializeToString,
        ),
        "store_update": grpc.unary_unary_rpc_method_handler(
            servicer.store_update,
            request_deserializer=messages__pb2.StoreUpdateRequest.FromString,
            response_serializer=messages__pb2.StoreUpdateResponse.SerializeToString,
        ),
        "store_list": grpc.unary_unary_rpc_method_handler(
            servicer.store_list,
            request_deserializer=messages__pb2.StoreListRequest.FromString,
            response_serializer=messages__pb2.StoreListResponse.SerializeToString,
        ),
        "store_read": grpc.unary_unary_rpc_method_handler(
            servicer.store_read,
            request_deserializer=messages__pb2.StoreReadRequest.FromString,
            response_serializer=messages__pb2.StoreReadResponse.SerializeToString,
        ),
        "store_write": grpc.unary_unary_rpc_method_handler(
            servicer.store_write,
            request_deserializer=messages__pb2.StoreWriteRequest.FromString,
            response_serializer=messages__pb2.StoreWriteResponse.SerializeToString,
        ),
        "store_check": grpc.unary_unary_rpc_method_handler(
            servicer.store_check,
            request_deserializer=messages__pb2.StoreCheckRequest.FromString,
            response_serializer=messages__pb2.StoreCheckResponse.SerializeToString,
        ),
        "store_list_objects": grpc.unary_unary_rpc_method_handler(
            servicer.store_list_objects,
            request_deserializer=messages__pb2.StoreListObjectsRequest.FromString,
            response_serializer=messages__pb2.StoreListObjectsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "GraphFgaService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class GraphFgaService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def store_view(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_view",
            messages__pb2.StoreViewRequest.SerializeToString,
            messages__pb2.StoreViewResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_create(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_create",
            messages__pb2.StoreCreateRequest.SerializeToString,
            messages__pb2.StoreCreateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_update(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_update",
            messages__pb2.StoreUpdateRequest.SerializeToString,
            messages__pb2.StoreUpdateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_list(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_list",
            messages__pb2.StoreListRequest.SerializeToString,
            messages__pb2.StoreListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_read(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_read",
            messages__pb2.StoreReadRequest.SerializeToString,
            messages__pb2.StoreReadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_write(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_write",
            messages__pb2.StoreWriteRequest.SerializeToString,
            messages__pb2.StoreWriteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_check(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_check",
            messages__pb2.StoreCheckRequest.SerializeToString,
            messages__pb2.StoreCheckResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def store_list_objects(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GraphFgaService/store_list_objects",
            messages__pb2.StoreListObjectsRequest.SerializeToString,
            messages__pb2.StoreListObjectsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
