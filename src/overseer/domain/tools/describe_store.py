from typing import Dict

from overseer.clients import graph_fga_client
from overseer.domain.tools import Tool


class DescribeStoreTool(Tool):
    NAME = "describe_store"
    DESCRIPTION = """
    Get the permission scheme in OpenFGA format for the current store. The scheme follows these key principles:

    1. Type Definitions:
       - Every type must be explicitly defined (e.g., 'type user', 'type issue')
       - The 'user' type is fundamental and must always be present

    2. Relations Structure:
       - Relations are defined under each type using 'relations define' blocks
       - Direct relations use square brackets to specify allowed types: [user], [group]
       - Multiple allowed types are comma-separated: [user, group]

    3. Permission Patterns:
       - Direct assignments: 'define manager: [user]'
       - Permission inheritance: 'define can_edit: manager'
       - Composite permissions using 'or': 'define can_edit: manager or owner'
       - Related object permissions: 'define can_edit: manager from attached'

    4. Relation References:
       - Hash notation (#) for nested relations: 'group#comrade'
       - Multi-level relations: 'foo_manager: bar_manager from foo_attached'

    5. Common Patterns:
       - Owner/manager hierarchies
       - View/edit permission inheritance
       - Group-based access control
       - Object relationship-based permissions

    The store should maintain consistent permission patterns and follow OpenFGA's graph-based authorization model.
    """

    def __init__(self, store_id: str) -> None:
        self._store_id = store_id

    def call(self, *args, **kwargs) -> str:
        return graph_fga_client.store_view(store_id=self._store_id)

    @property
    def input_schema(self) -> Dict:
        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
