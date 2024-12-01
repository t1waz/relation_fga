from typing import Dict, List

from graph_fga.entities import RelationTuple
from overseer.clients import graph_fga_client
from overseer.domain.tools import Tool


class WriteStoreRelationTool(Tool):
    NAME = "write_relation"
    DESCRIPTION = """
    Write or delete relation tuples in the OpenFGA store. This tool allows you to manage relationships
    between entities in the authorization model.

    The relation tuples represent relationships like:
    - User assignments to roles
    - Object ownership
    - Group memberships
    - Permission grants

    Each relation tuple consists of:
    - source: The entity granting the permission (e.g. "user:123", "group:admin")
    - target: The entity the permission is for (e.g. "document:456", "project:789") 
    - relation: The type of relationship (e.g. "owner", "viewer", "member")

    Relations can include conditions using hash notation:
    - Simple: "user:123#owner"
    - Nested: "group:admin#manager"
    """

    def __init__(self, store_id: str) -> None:
        self._store_id = store_id

    def call(self, writes: List[Dict], deletes: List[Dict] = None) -> Dict:
        write_tuples = []
        if writes:
            write_tuples = [
                RelationTuple(
                    source=write["source"],
                    target=write["target"],
                    relation=write["relation"],
                )
                for write in writes
            ]

        delete_tuples = []
        if deletes:
            delete_tuples = [
                RelationTuple(
                    source=delete["source"],
                    target=delete["target"],
                    relation=delete["relation"],
                )
                for delete in deletes
            ]

        status = graph_fga_client.store_write(
            store_id=self._store_id, writes=write_tuples, deletes=delete_tuples
        )

        return {"status": status}

    @property
    def input_schema(self) -> Dict:
        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "input_schema": {
                "type": "object",
                "properties": {
                    "writes": {
                        "type": "array",
                        "description": "List of relation tuples to write",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "description": "The source entity (e.g. user:123, group:admin)",
                                },
                                "target": {
                                    "type": "string",
                                    "description": "The target entity (e.g. document:456)",
                                },
                                "relation": {
                                    "type": "string",
                                    "description": "The relation type (e.g. owner, viewer)",
                                },
                            },
                            "required": ["source", "target", "relation"],
                        },
                    },
                    "deletes": {
                        "type": "array",
                        "description": "Optional list of relation tuples to delete",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "description": "The source entity (e.g. user:123, group:admin)",
                                },
                                "target": {
                                    "type": "string",
                                    "description": "The target entity (e.g. document:456)",
                                },
                                "relation": {
                                    "type": "string",
                                    "description": "The relation type (e.g. owner, viewer)",
                                },
                            },
                            "required": ["source", "target", "relation"],
                        },
                    },
                },
                "required": ["writes"],
            },
        }
