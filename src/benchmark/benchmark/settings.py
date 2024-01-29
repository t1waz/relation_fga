OPENFGA_HOST = "127.0.0.1"
OPENFGA_PORT = "7777"

GRAPH_FGA_HOST = "127.0.0.1"
GRAPH_FGA_PORT = "9999"

GRAPH_DB_HOST = "127.0.0.1"
GRAPH_DB_PORT = "7687"


SCHEMA = open("auth-model.dsl").read()
JSON_SCHEMA = {
    "schema_version": "1.1",
    "type_definitions": [
        {"type": "user", "relations": {}, "metadata": None},
        {
            "type": "unit",
            "relations": {"member": {"this": {}}, "parent": {"this": {}}},
            "metadata": {
                "relations": {
                    "member": {"directly_related_user_types": [{"type": "user"}]},
                    "parent": {"directly_related_user_types": [{"type": "unit"}]},
                }
            },
        },
        {
            "type": "issue",
            "relations": {
                "editor": {"this": {}},
                "owner": {"this": {}},
                "participant": {"this": {}},
                "viewer": {"this": {}},
                "can_edit": {
                    "union": {
                        "child": [
                            {"computedUserset": {"relation": "editor"}},
                            {"computedUserset": {"relation": "owner"}},
                        ]
                    }
                },
                "can_view": {
                    "union": {
                        "child": [
                            {"computedUserset": {"relation": "can_edit"}},
                            {"computedUserset": {"relation": "viewer"}},
                            {"computedUserset": {"relation": "participant"}},
                        ]
                    }
                },
            },
            "metadata": {
                "relations": {
                    "editor": {
                        "directly_related_user_types": [
                            {"type": "user"},
                            {"type": "unit"},
                            {"type": "unit", "relation": "member"},
                        ]
                    },
                    "owner": {"directly_related_user_types": [{"type": "user"}]},
                    "participant": {"directly_related_user_types": [{"type": "user"}]},
                    "viewer": {
                        "directly_related_user_types": [
                            {"type": "user"},
                            {"type": "unit"},
                            {"type": "unit", "relation": "member"},
                        ]
                    },
                    "can_edit": {"directly_related_user_types": []},
                    "can_view": {"directly_related_user_types": []},
                }
            },
        },
    ],
}
