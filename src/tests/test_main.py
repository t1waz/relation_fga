import uuid

import grpc
import pytest

from graph_fga.entities import RelationTuple
from graph_fga.grpc.pb2 import messages_pb2


class TestMainRelationRead:
    def test_graph_fga_server_get_existing_relations_only_source_type(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_read(
            request=messages_pb2.StoreReadRequest(
                store_id=f_auth_model_1.id,
                source=messages_pb2.StoreReadObj(
                    type="user",
                ),
            )
        )

        desired_relations = [
            {
                "object": o,
                "relation": r,
                "user": desired_user,
            }
            for r, o in zip(desired_relations, desired_targets)
        ]

        for response_object in response.objects:
            relation = {
                "user": response_object.user,
                "object": response_object.object,
                "relation": response_object.relation,
            }
            assert relation in desired_relations

    def test_graph_fga_server_get_existing_relations_source_type_with_id(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_read(
            request=messages_pb2.StoreReadRequest(
                store_id=f_auth_model_1.id,
                source=messages_pb2.StoreReadObj(
                    id="foo",
                    type="user",
                ),
            )
        )

        desired_relations = [
            {
                "object": o,
                "relation": r,
                "user": desired_user,
            }
            for r, o in zip(desired_relations, desired_targets)
        ]

        for response_object in response.objects:
            relation = {
                "user": response_object.user,
                "object": response_object.object,
                "relation": response_object.relation,
            }
            assert relation in desired_relations


class TestMainListObjects:
    def test_graph_fga_server_get_list_objects_existing_multiple_1(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_edit",
            )
        )

        assert set(response.objects) == {"222", "333"}

    def test_graph_fga_server_get_list_objects_existing_multiple_2(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
            )
        )

        assert set(response.objects) == {"333", "222"}

    def test_graph_fga_server_get_list_objects_existing_multiple_3(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="manager",
            )
        )

        assert set(response.objects) == {"222"}

    def test_graph_fga_server_get_list_objects_no_access(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:foo1"
        desired_targets = ["issue:1111", "issue:2222", "issue:3332"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user="user:aaa",
                permission="can_edit",
            )
        )

        assert response.objects == []

    def test_graph_fga_server_get_list_objects_existing_related(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_unit = "group:1"
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target="issue:444", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="group:1#comrade", target="issue:444", relation="manager"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_edit",
            )
        )

        assert set(response.objects) == {"222", "333", "444"}

    def test_graph_fga_server_get_list_objects_existing_related_with_permission(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_unit = "group:1"
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target="issue:444", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade", target="issue:555", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade", target="issue:444", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target="issue:555", relation="viewer"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar1", target="issue:666", relation="manager"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
            )
        )

        assert set(response.objects) == {"222", "333", "444", "555"}

    def test_graph_fga_server_get_list_objects_existing_related_with_permission_no_attached_user_to_related(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_unit = "group:1"
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="group:1#comrade", target="issue:444", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target="issue:555", relation="viewer"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
            )
        )

        assert set(response.objects) == {"222", "333", "444"}

    def test_graph_fga_server_get_list_objects_existing_related_with_permission_no_attached_user_to_related_2(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_unit = "group:1"
        desired_user = "user:foo"
        desired_targets = ["issue:111", "issue:222", "issue:333"]
        desired_relations = ["owner", "manager", "viewer"]

        for target, relation in zip(desired_targets, desired_relations):
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id,
                relation_tuple=RelationTuple(
                    source=desired_user, target=target, relation=relation
                ),
            )

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade", target="issue:444", relation="viewer"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:bar", target="issue:555", relation="viewer"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_edit",
            )
        )

        assert set(response.objects) == {"222", "333"}

    def test_graph_fga_server_get_list_objects_existing_related_with_permission_no_attached_user_to_related_3(
        self, grpc_stub, f_auth_model_2, relation_tuple_repository
    ):
        common_unit = "group:2"
        desired_user = "user:11"

        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade",
                target="bar:444",
                relation="viewer",
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source="user:22", target="issue:444", relation="owner"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_2.id,
                type="bar",
                user=desired_user,
                permission="can_view",
            )
        )

        assert set(response.objects) == {"444"}

    def test_graph_fga_server_get_list_objects_invalid_type(
        self, grpc_stub, f_auth_model_2, relation_tuple_repository
    ):
        common_unit = "group:2"
        desired_user = "user:11"

        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade",
                target="bar:444",
                relation="viewer",
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source="user:22", target="issue:444", relation="owner"
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_2.id,
                type="foo",
                user=desired_user,
                permission="can_view",
            )
        )

        assert response.objects == []

    def test_graph_fga_server_get_list_objects_contextual_single_object(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_object_id = "11112"
        common_group = "group:123-11"
        desired_user = "user:11-22"
        desired_object = f"issue:{desired_object_id}"

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_group}#comrade",
                target=desired_object,
                relation="manager",
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
            )
        )

        assert response.objects == []

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=desired_user, object=common_group, relation="comrade"
                    )
                ],
            )
        )

        assert response.objects == [desired_object_id]

    def test_graph_fga_server_get_list_objects_contextual_will_not_persist_contextual(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_object_id = "11112"
        common_group = "group:123-11"
        desired_user = "user:11-22"
        desired_object = f"issue:{desired_object_id}"

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_group}#comrade",
                target=desired_object,
                relation="manager",
            ),
        )

        grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=desired_user, object=common_group, relation="comrade"
                    )
                ],
            )
        )

        tuples = grpc_stub.store_read(
            request=messages_pb2.StoreReadRequest(
                store_id=f_auth_model_1.id,
                source=messages_pb2.StoreReadObj(
                    type="user",
                ),
            )
        )

        assert len(tuples.objects) == 0

    def test_graph_fga_server_get_list_objects_contextual_multiple_object(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_objects_ids = ["11112", "22221"]
        common_group = "group:123-11"
        desired_user = "user:11-22"

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_group}#comrade",
                target=f"issue:{desired_objects_ids[0]}",
                relation="manager",
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user,
                target=f"issue:{desired_objects_ids[1]}",
                relation="viewer",
            ),
        )

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
            )
        )

        assert response.objects == [desired_objects_ids[1]]

        response = grpc_stub.store_list_objects(
            request=messages_pb2.StoreListObjectsRequest(
                store_id=f_auth_model_1.id,
                type="issue",
                user=desired_user,
                permission="can_view",
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=desired_user, object=common_group, relation="comrade"
                    )
                ],
            )
        )

        assert set(response.objects) == set(desired_objects_ids)


class TestMainStoreCreate:
    def test_graph_fga_server_create_store_invalid_model(self, grpc_stub):
        invalid_model = "sdfd fgoo"

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_create(
                request=messages_pb2.StoreCreateRequest(
                    model=invalid_model,
                )
            )
        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "model" in exc_data

    def test_graph_fga_server_create_store_valid_request(
        self, grpc_stub, model_config_repository
    ):
        desired_model = """
        type user

        type unit
          relations
            define comrade: [user]
            define root: [unit]

        """

        response = grpc_stub.store_create(
            request=messages_pb2.StoreCreateRequest(
                model=desired_model,
            )
        )

        assert response.status == "ok"
        assert response.store_id

        auth_model = model_config_repository.get_model_config(
            store_id=response.store_id
        )
        assert auth_model.id == response.store_id
        assert auth_model.config == desired_model


class TestMainStoreUpdate:
    def test_graph_fga_server_update_not_existing_store(
        self, grpc_stub, f_auth_model_1
    ):
        desired_model = """
        type user
    
        """

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_update(
                request=messages_pb2.StoreUpdateRequest(
                    store_id=str(uuid.uuid4()),
                    model=desired_model,
                )
            )
        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "model" in exc_data

    def test_graph_fga_server_update_invalid_model(self, grpc_stub, f_auth_model_1):
        invalid_model = "sdfd fgoo"

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_update(
                request=messages_pb2.StoreUpdateRequest(
                    store_id=f_auth_model_1.id,
                    model=invalid_model,
                )
            )
        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "model" in exc_data

    def test_graph_fga_server_update_existing_store(self, grpc_stub, f_auth_model_1):
        desired_model = """
        type user

        type unit
          relations
            define comrade: [user]
            define root: [unit]

        """

        response = grpc_stub.store_update(
            request=messages_pb2.StoreUpdateRequest(
                store_id=f_auth_model_1.id,
                model=desired_model,
            )
        )

        assert response.status == "updated"
        assert response.store_id == f_auth_model_1.id

    def test_graph_fga_server_after_update_permission_changed(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_model = """
        type user

        type unit
          relations
            define comrade: [user]
            define root: [unit]

        """

        response = grpc_stub.store_update(
            request=messages_pb2.StoreUpdateRequest(
                store_id=f_auth_model_1.id,
                model=desired_model,
            )
        )

        desired_user = "user:1"
        desired_case = "issue:1"
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=desired_case, relation="manager"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_case,
                permission="can_edit",
            )
        )

        assert response.allowed is False


class TestMainCheck:
    def test_graph_fga_server_check_valid_data_not_existing_direct_access(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:1", target="issue:1", relation="manager"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user="user:2",
                object="issue:1",
                permission="can_edit",
            )
        )

        assert response.allowed is False

    def test_graph_fga_server_check_valid_data_existing_direct_access_from_another_store(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:1"
        desired_case = "issue:1"
        relation_tuple_repository.save(
            store_id=str(uuid.uuid4()),
            relation_tuple=RelationTuple(
                source=desired_user, target=desired_case, relation="manager"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_case,
                permission="can_edit",
            )
        )

        assert response.allowed is False

    def test_graph_fga_server_check_valid_data_existing_direct_access(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:1"
        desired_case = "issue:1"
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=desired_case, relation="manager"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_case,
                permission="can_edit",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_valid_data_existing_not_direct_access(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_user = "user:1"
        desired_case = "issue:1"
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=desired_user, target="group:1", relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:2", target="group:1", relation="comrade"
            ),
        )

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="user:2", target=desired_case, relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source="group:1#comrade", target=desired_case, relation="manager"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_case,
                permission="can_edit",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_existing_related_with_permission_no_attached_user_to_relate(
        self, grpc_stub, f_auth_model_2, relation_tuple_repository
    ):
        common_unit = "group:2"
        desired_user = "user:11"
        desired_object = "bar:444"

        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_unit, relation="comrade"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source=f"{common_unit}#comrade",
                target=desired_object,
                relation="viewer",
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_2.id,
            relation_tuple=RelationTuple(
                source="user:22", target="issue:444", relation="owner"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_2.id,
                user=desired_user,
                object=desired_object,
                permission="can_view",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_existing_related_with_from(
        self, grpc_stub, f_auth_model_3, relation_tuple_repository
    ):
        desired_user = "user:foo1"
        desired_object = "issue:777"

        relation_tuple_repository.save(
            store_id=f_auth_model_3.id,
            relation_tuple=RelationTuple(
                source=desired_user, target="task:1111", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_3.id,
            relation_tuple=RelationTuple(
                source="task:1111", target=desired_object, relation="attached"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_3.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_existing_related_with_from_one_nested(
        self, grpc_stub, f_auth_model_4, relation_tuple_repository
    ):
        desired_user = "user:foo1"
        desired_object = "issue:777"

        relation_tuple_repository.save(
            store_id=f_auth_model_4.id,
            relation_tuple=RelationTuple(
                source=desired_user, target="task:1111", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_4.id,
            relation_tuple=RelationTuple(
                source="task:1111", target=desired_object, relation="attached"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_4.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
            )
        )

        assert response.allowed is True

    def test_real_model_attached(
        self, grpc_stub, f_auth_model_5, relation_tuple_repository
    ):
        desired_user = "user:1111"
        common_object = "ticket:3333"
        desired_object = "issue:2222"

        relation_tuple_repository.save(
            store_id=f_auth_model_5.id,
            relation_tuple=RelationTuple(
                source=desired_user, target=common_object, relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_5.id,
            relation_tuple=RelationTuple(
                source=common_object, target=desired_object, relation="attached"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_5.id,
                user=desired_user,
                object=desired_object,
                permission="can_view",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_existing_related_with_from_two_nested(
        self, grpc_stub, f_auth_model_5, relation_tuple_repository
    ):
        desired_user = "user:foo1"
        desired_object = "issue:777"
        common_object = "task:1234"

        relation_tuple_repository.save(
            store_id=f_auth_model_5.id,
            relation_tuple=RelationTuple(
                source=desired_user, target="parcel:1111", relation="manager"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_5.id,
            relation_tuple=RelationTuple(
                source="parcel:1111", target=common_object, relation="attached"
            ),
        )
        relation_tuple_repository.save(
            store_id=f_auth_model_5.id,
            relation_tuple=RelationTuple(
                source=common_object, target=desired_object, relation="attached"
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_5.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_with_contextual_tuple(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_group = "group:123-11"
        desired_user = "user:11-22"
        desired_object = "issue:11112"

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_group}#comrade",
                target=desired_object,
                relation="manager",
            ),
        )

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
            )
        )

        assert response.allowed is False

        response = grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=desired_user, object=common_group, relation="comrade"
                    )
                ],
            )
        )

        assert response.allowed is True

    def test_graph_fga_server_check_with_contextual_tuple_does_not_persist_contextual(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        common_group = "group:123-11"
        desired_user = "user:11-22"
        desired_object = "issue:11112"

        relation_tuple_repository.save(
            store_id=f_auth_model_1.id,
            relation_tuple=RelationTuple(
                source=f"{common_group}#comrade",
                target=desired_object,
                relation="manager",
            ),
        )

        grpc_stub.store_check(
            request=messages_pb2.StoreCheckRequest(
                store_id=f_auth_model_1.id,
                user=desired_user,
                object=desired_object,
                permission="can_edit",
                contextual_tuples=[
                    messages_pb2.StoreRelationTuple(
                        user=desired_user, object=common_group, relation="comrade"
                    )
                ],
            )
        )

        tuples = grpc_stub.store_read(
            request=messages_pb2.StoreReadRequest(
                store_id=f_auth_model_1.id,
                source=messages_pb2.StoreReadObj(
                    type="user",
                ),
            )
        )

        assert len(tuples.objects) == 0


class TestMainWrite:
    def test_graph_fga_server_send_invalid_source_name_for_writes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="foo:1", relation="comrade", object="group:1"
                )
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid source type" in exc_data

    def test_graph_fga_server_send_invalid_source_no_id_for_writes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="user", relation="comrade", object="group:1"
                )
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "user" in exc_data
        assert "no id" in exc_data

    def test_graph_fga_server_send_invalid_target_name_for_writes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="comrade", object="foo:1"
                )
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid relation" in exc_data

    def test_graph_fga_server_send_invalid_target_no_id_for_writes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="comrade", object="group"
                )
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "group" in exc_data
        assert "no id" in exc_data

    def test_graph_fga_server_send_invalid_relation_for_writes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="foo", object="group:1"
                )
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid relation" in exc_data

    def test_graph_fga_server_send_invalid_store_id_writes_request(self, grpc_stub):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]
        request = messages_pb2.StoreWriteRequest(
            store_id=str(uuid.uuid4()),
            writes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
            deletes=[],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "store_id" in exc_data

    def test_graph_fga_server_send_valid_writes_request(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
            deletes=[],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

    def test_graph_fga_server_send_valid_writes_request_another_model(
        self, grpc_stub, f_auth_model_2, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="attached", target="document:1"),
            RelationTuple(source="user:2", relation="attached", target="document:1"),
        ]
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_2.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
            deletes=[],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_2.id, relation_tuple=relation_tuple
            )

    def test_graph_fga_server_send_valid_writes_request_with_relation_name_repeated_in_types(
        self, grpc_stub, f_auth_model_2, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="owner", target="issue:1"),
            RelationTuple(source="user:2", relation="owner", target="issue:2"),
        ]
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_2.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
            deletes=[],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_2.id, relation_tuple=relation_tuple
            )

    def test_graph_fga_server_send_valid_writes_request_repeated_in_deletes(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_write_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]
        desired_delete_relation_tuples = [
            desired_write_relation_tuples[0],
            RelationTuple(source="user:3", relation="comrade", target="group:1"),
        ]
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_write_relation_tuples
            ],
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_delete_relation_tuples
            ],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        assert not relation_tuple_repository.is_exists(
            store_id=f_auth_model_1.id, relation_tuple=desired_write_relation_tuples[0]
        )

        for relation_tuple in desired_write_relation_tuples[1:]:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

    def test_real_model(self, grpc_stub, f_auth_model_5):
        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_5.id,
            writes=[
                messages_pb2.StoreRelationTuple(
                    user="parcel:018cd6e8-f9d6-79b8-d8ed-8d50269fa63e",
                    relation="attached",
                    object="ticket:018cd6e8-f9e5-0b6d-48bc-38d80d19ddce",
                )
            ],
            deletes=[],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"


class TestMainDelete:
    def test_graph_fga_server_send_invalid_source_name_for_deletes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=f_auth_model_1.id,
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user="foo:1", relation="comrade", object="group:1"
                )
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid source type" in exc_data

    def test_graph_fga_server_send_invalid_source_no_id_for_deletes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=f_auth_model_1.id,
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user="user", relation="comrade", object="group:1"
                )
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "user" in exc_data
        assert "no id" in exc_data

    def test_graph_fga_server_send_invalid_target_name_for_deletes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=f_auth_model_1.id,
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="comrade", object="foo:1"
                )
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid relation" in exc_data

    def test_graph_fga_server_send_invalid_target_no_id_for_deletes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=f_auth_model_1.id,
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="comrade", object="group"
                )
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "group" in exc_data
        assert "no id" in exc_data

    def test_graph_fga_server_send_invalid_relation_for_deletes_relations(
        self, grpc_stub, f_auth_model_1
    ):
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=f_auth_model_1.id,
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user="user:1", relation="foo", object="group:1"
                )
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "invalid relation" in exc_data

    def test_graph_fga_server_send_invalid_store_id_deletes_request(self, grpc_stub):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]
        request = messages_pb2.StoreWriteRequest(
            writes=[],
            store_id=str(uuid.uuid4()),
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as exc_info:
            grpc_stub.store_write(request=request)

        exc_data = exc_info.value.details()

        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert "store_id" in exc_data

    def test_graph_fga_server_send_valid_deletes_request(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]
        for relation_tuple in desired_relation_tuples:
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

        for relation_tuple in desired_relation_tuples:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[],
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert not relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

    def test_graph_fga_server_send_valid_deletes_conditional_tuples(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(
                source="group:1#comrade", relation="viewer", target="issue:1"
            ),
            RelationTuple(
                source="group:2#comrade", relation="manager", target="issue:1"
            ),
        ]
        for relation_tuple in desired_relation_tuples:
            relation_tuple_repository.save(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

        for relation_tuple in desired_relation_tuples:
            assert relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[],
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert not relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )

    def test_graph_fga_server_send_not_existing_deletes_request(
        self, grpc_stub, f_auth_model_1, relation_tuple_repository
    ):
        desired_relation_tuples = [
            RelationTuple(source="user:1", relation="comrade", target="group:1"),
            RelationTuple(source="user:2", relation="comrade", target="group:1"),
        ]

        request = messages_pb2.StoreWriteRequest(
            store_id=f_auth_model_1.id,
            writes=[],
            deletes=[
                messages_pb2.StoreRelationTuple(
                    user=d.source, relation=d.relation, object=d.target
                )
                for d in desired_relation_tuples
            ],
        )

        response = grpc_stub.store_write(request=request)

        assert response.status == "ok"

        for relation_tuple in desired_relation_tuples:
            assert not relation_tuple_repository.is_exists(
                store_id=f_auth_model_1.id, relation_tuple=relation_tuple
            )
