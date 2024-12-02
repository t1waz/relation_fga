from typing import Dict

from overseer_backend.clients import graph_fga_client
from overseer_backend.domain.tools import Tool


class UpdateStoreTool(Tool):
    NAME = "update_store"
    DESCRIPTION = """
        Update the permission scheme in OpenFGA format for the current store. When updating the store, follow these critical rules and patterns:

        1. Mandatory Requirements:
           - Always preserve the 'type user' definition
           - Never use plural names for resource modeling
           - For resource name during permission modeling always use english names.
           - Maintain referential integrity across all relations
           - Ensure all type definitions are complete with their relations

        2. Permission Modeling Guidelines with Examples:
           a) Basic Relations:
              - Use direct assignments for primary ownership: '[user]'
              Example:
                ```
                type issue
                  relations
                    define manager: [user]
                ```

              - Define group memberships:
              Example:
                ```
                type group
                  relations
                    define comrade: [user]
                ```

              - Support multiple assignees:
              Example:
                ```
                type issue
                  relations
                    define manager: [user, group, group#comrade]
                ```

           b) Permission Inheritance:
              - Define base relations before derived permissions
              Example:
                ```
                type issue
                  relations
                    define manager: [user]
                    define can_edit: manager    # Inherits from manager
                ```

              - Create permission hierarchies with multiple sources
              Example:
                ```
                type issue
                  relations
                    define owner: [user]
                    define manager: [user]
                    define can_edit: manager or owner
                ```

              - Complex permission inheritance
              Example:
                ```
                type issue
                  relations
                    define can_edit1: manager from attached or manager
                    define can_view1: can_view2 from attached or can_edit1 or viewer
                    define manager: [user, group]
                    define viewer: [user, group]
                ```

           c) Related Object Permissions:
              - Simple related object access
              Example:
                ```
                type issue
                  relations
                    define attached: [foo]
                    define can_edit: manager from attached
                ```

              - Multi-level relations
              Example:
                ```
                type bar
                  relations
                    define bar_manager: [user]

                type foo
                  relations
                    define foo_attached: [bar]
                    define foo_manager: bar_manager from foo_attached

                type issue
                  relations
                    define attached: [foo]
                    define can_edit: foo_manager from attached
                ```

              - Nested permissions with hash notation
              Example:
                ```
                type group
                  relations
                    define comrade: [foo#owner]

                type issue
                  relations
                    define manager: [user, group#comrade]
                ```

           d) Complex Permission Patterns:
              - View/edit hierarchies with multiple paths
              Example:
                ```
                type task
                  relations
                    define can_edit2: manager or owner
                    define can_view2: can_edit2 or viewer or participant
                    define manager: [user, group]
                    define owner: [user]
                    define participant: [user]
                    define viewer: [user, group]
                ```

              - Nested relations with multiple conditions
              Example:
                ```
                type foo
                  relations
                    define owner: [user, issue]
                    define manager: [user, group]
                    define foo_can_edit: owner or manager

                type issue
                  relations
                    define attached: [foo]
                    define manager: [user, group#comrade]
                    define can_edit: manager or foo_can_edit from attached
                ```

        3. Validation Rules:
           - All referenced types must be defined before use
           - All relations must have valid targets
           - Circular dependencies should be avoided
           - Permission paths should be traceable

        4. Best Practices:
           - Group related permissions together
           - Use consistent naming conventions (e.g., can_edit, can_view)
           - Document complex permission chains
           - Consider performance implications of deeply nested relations

        5. Schema Evolution:
           - Maintain backward compatibility when possible
           - Update related permissions when modifying types
           - Preserve existing access patterns when extending the schema

        The examples above demonstrate common patterns found in real-world authorization scenarios. When implementing new patterns, ensure they follow similar principles of clarity and maintainability while preserving the security model's integrity.
        """

    def __init__(self, store_id: str) -> None:
        self._store_id = store_id

    def call(self, model_str: str) -> str:
        return graph_fga_client.store_update(
            store_id=self._store_id, model_str=model_str
        )

    @property
    def input_schema(self) -> Dict:
        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "input_schema": {
                "type": "object",
                "properties": {
                    "model_str": {
                        "type": "string",
                        "description": "permission scheme in OpenFga format to create",
                    }
                },
                "required": ["model"],
            },
        }
