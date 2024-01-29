from graph_fga.interpreter.auth_model import AuthModel
from graph_fga.interpreter.services import AuthModelService


def test_simple_path():
    model_str = """
        type user

        type issue
          relations
            define manager: [user]
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="manager")

    assert paths == ["(user)-[:manager]->(issue)"]


def test_path_with_permission():
    model_str = """
        type user

        type issue
          relations
            define manager: [user]
            define can_edit: manager
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert paths == ["(user)-[:manager]->(issue)"]


def test_path_with_permission_no_access():
    model_str = """
        type user

        type parcel
          relations
            define foo: [user]

        type issue
          relations
            define manager: [parcel]
            define can_edit: manager
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert paths == []


def test_path_with_permission_multiple():
    model_str = """
        type user

        type parcel
          relations
            define foo: [user]

        type issue
          relations
            define owner: [user]
            define manager: [parcel]
            define can_edit: manager or owner
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert paths == ["(user)-[:owner]->(issue)"]


def test_path_with_single_related_relation():
    model_str = """
        type user
        
        type foo
          relations
            define manager: [user]

        type group

        type issue
          relations
            define attached: [foo]
            define manager: [group]
            define can_edit: manager from attached
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert set(paths) == {"(user)-[:manager]->(foo)-[:attached]->(issue)"}


def test_path_with_single_related_permission():
    model_str = """
        type user

        type foo
          relations
            define manager: [user]
            define can_edit: manager

        type group

        type issue
          relations
            define attached: [foo]
            define manager: [group]
            define can_edit: can_edit from attached
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert set(paths) == {"(user)-[:manager]->(foo)-[:attached]->(issue)"}


def test_path_with_double_related_relation():
    model_str = """
        type user
        
        type bar
          relations
            define bar_manager: [user]
        
        type foo
          relations
            define foo_attached: [bar]
            define foo_manager: bar_manager from foo_attached

        type group

        type issue
          relations
            define attached: [foo]
            define manager: [group]
            define can_edit: foo_manager from attached
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert set(paths) == {
        "(user)-[:bar_manager]->(bar)-[:foo_attached]->(foo)-[:attached]->(issue)"
    }


def test_path_with_double_related_relation_and_hash():
    model_str = """
        type user

        type group
          relations
            define comrade: [user]

        type bar
          relations
            define bar_manager: [group#comrade]

        type foo
          relations
            define foo_attached: [bar]
            define foo_manager: bar_manager from foo_attached

        type issue
          relations
            define attached: [foo]
            define manager: [group]
            define can_edit: foo_manager from attached
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert set(paths) == {
        "(user)-[:comrade]->(group)-[:bar_manager111comrade]->(bar)-[:foo_attached]->(foo)-[:attached]->(issue)"
    }


def test_path_with_hash():
    model_str = """
        type user

        type group
          relations
            define comrade: [user, group]

        type issue
          relations
            define manager: [user, group#comrade]
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="manager")

    assert set(paths) == {
        "(user)-[:comrade]->(group)-[:manager111comrade]->(issue)",
        "(user)-[:manager]->(issue)",
    }


def test_path_with_nested_hash():
    model_str = """
        type user

        type foo
          relations
            define owner: [user, issue]

        type group
          relations
            define comrade: [foo#owner]

        type issue
          relations
            define manager: [user, group#comrade]
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="manager")

    assert set(paths) == {
        "(user)-[:manager]->(issue)",
        "(user)-[:owner]->(foo)-[:comrade111owner]->(group)-[:manager111comrade]->(issue)",
    }


def test_path_with_nested_hash_and_multiple_or():
    model_str = """
        type user

        type foo
          relations
            define owner: [user, issue]
            define manager: [user, group]
            define foo_can_edit: owner or manager

        type group
          relations
            define comrade: [foo#owner]

        type issue
          relations
            define attached: [foo]
            define manager: [user, group#comrade]
            define can_edit: manager or foo_can_edit from attached
    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_edit")

    assert set(paths) == {
        "(user)-[:manager]->(issue)",
        "(user)-[:manager]->(foo)-[:attached]->(issue)",
        "(user)-[:owner]->(foo)-[:attached]->(issue)",
        "(user)-[:owner]->(foo)-[:comrade111owner]->(group)-[:manager111comrade]->(issue)",
    }


def test_path_with_nested_hash_and_multiple_or_2():
    model_str = """
        type user

        type group
          relations
            define comrade: [user]

        type issue
          relations
            define attached: [task]
            define can_edit1: manager from attached or manager
            define can_view1: can_view2 from attached or can_edit1 or viewer
            define manager: [user, group, group#comrade]
            define viewer: [user, group, group#comrade]

        type task
          relations
            define can_edit2: manager or owner
            define can_view2: can_edit2 or viewer or participant
            define manager: [user, group, group#comrade]
            define owner: [user]
            define participant: [user]
            define viewer: [user, group, group#comrade]

    """
    auth_model = AuthModel(config=model_str)
    service = AuthModelService(auth_model=auth_model)
    paths = service.get_paths_cmds(start="user", end="issue", relation="can_view1")

    assert set(paths) == {
        "(user)-[:comrade]->(group)-[:viewer111comrade]->(issue)",
        "(user)-[:comrade]->(group)-[:viewer111comrade]->(task)-[:attached]->(issue)",
        "(user)-[:viewer]->(issue)",
        "(user)-[:viewer]->(task)-[:attached]->(issue)",
        "(user)-[:manager]->(issue)",
        "(user)-[:participant]->(task)-[:attached]->(issue)",
        "(user)-[:manager]->(task)-[:attached]->(issue)",
        "(user)-[:comrade]->(group)-[:manager111comrade]->(issue)",
        "(user)-[:owner]->(task)-[:attached]->(issue)",
        "(user)-[:comrade]->(group)-[:manager111comrade]->(task)-[:attached]->(issue)",
    }
