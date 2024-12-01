from typing import Dict, List, Optional

from graph_fga.entities import CheckRequest
from overseer.clients import graph_fga_client
from overseer.domain.tools import Tool


class CheckStoreRelationTool(Tool):
    NAME = "check_relation"
    DESCRIPTION = """
    Check if a specific relation exists between entities in the OpenFGA store. This tool verifies
    authorization relationships and permissions based on the defined model.

    The check evaluates:
    1. Direct Relations:
       - Simple user-to-object permissions (e.g., user:123 can_edit document:456)
       - Group membership checks (e.g., user:123 member group:admin)

    2. Inherited Relations:
       - Permission inheritance (e.g., editor inherits viewer permissions)
       - Nested group permissions (group#role)

    3. Contextual Relations:
       - Temporary or conditional permissions through contextual tuples
       - Additional relationship context for the check

    Examples of checks:
    - Can user:123 edit document:456?
    - Is user:123 a member of group:admin?
    - Does user:123 have viewer access to project:789 through their group membership?

    The tool returns a boolean indicating whether the relation is allowed or not.
    """

    def __init__(self, store_id: str) -> None:
        self._store_id = store_id

    def call(
        self,
        source: str,
        target: str,
        permission: str,
        contextual_tuples: Optional[List[Dict]] = None,
    ) -> bool:
        context_relations = None
        if contextual_tuples:
            context_relations = [
                {
                    "user": tuple["source"],
                    "object": tuple["target"],
                    "relation": tuple["relation"],
                }
                for tuple in contextual_tuples
            ]

        check_request = CheckRequest(
            source=source,
            target=target,
            permission=permission,
            contextual_tuples=context_relations,
        )

        return graph_fga_client.store_check(
            store_id=self._store_id,
            user=check_request.source,
            object=check_request.target,
            permission=check_request.permission,
            contextual_tuples=context_relations,
        )

    @property
    def input_schema(self) -> Dict:
        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "input_schema": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "The source entity (e.g., user:123, group:admin) that wants to access the target",
                    },
                    "target": {
                        "type": "string",
                        "description": "The target entity (e.g., document:456) being accessed",
                    },
                    "permission": {
                        "type": "string",
                        "description": "The permission or relation to check (e.g., can_edit, can_view, member)",
                    },
                    "contextual_tuples": {
                        "type": "array",
                        "description": "Optional list of additional relation tuples to consider during the check",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "description": "The source entity in the contextual relation",
                                },
                                "target": {
                                    "type": "string",
                                    "description": "The target entity in the contextual relation",
                                },
                                "relation": {
                                    "type": "string",
                                    "description": "The type of contextual relation",
                                },
                            },
                            "required": ["source", "target", "relation"],
                        },
                    },
                },
                "required": ["source", "target", "permission"],
            },
        }
