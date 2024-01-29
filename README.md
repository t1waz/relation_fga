RELATION FGA
============



DEV GUIDE
---------
PROTOS:

run commands from graph_fga/grpc folder:

    $ python -m grpc_tools.protoc -I./protos --python_out=./pb2 --pyi_out=./pb2 --grpc_python_out=./pb2 protos/messages.proto
    $ python -m grpc_tools.protoc -I./protos --python_out=./pb2 --pyi_out=./pb2 --grpc_python_out=./pb2 protos/services.proto
    

edit file services_pb2_grpc first line to:

    from . import messages_pb2 as messages__pb2


TESTS:

GRPC tests:

    $ docker compose run server_grpc pytest
