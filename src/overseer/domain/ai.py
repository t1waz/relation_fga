from typing import List, Dict, Optional

from anthropic import AsyncAnthropic
from anthropic.types import Message

from overseer import settings
from overseer.domain.models import AIMessage
from overseer.domain.tools.check_store_relation import CheckStoreRelationTool
from overseer.domain.tools.describe_store import DescribeStoreTool
from overseer.domain.tools.update_store import UpdateStoreTool
from overseer.domain.tools.write_store_relation import WriteStoreRelationTool


class OverSeerAssistant:
    MODEL = "claude-3-5-sonnet-latest"
    TOOLS = [
        UpdateStoreTool,
        DescribeStoreTool,
        WriteStoreRelationTool,
        CheckStoreRelationTool,
    ]
    SYSTEM_PROMPT = """
    CURRENT PERMISSION SCHEME:
    {permission_model}

    Authorization System Guidelines:
    ------------------------------
    You are an authorization system assistant. Your role is to help manage and verify permissions
    while following these strict rules:

    1. Current State Only
       - ONLY use the CURRENT permission scheme shown above
       - NEVER reference or assume permissions from chat history
       - Permissions may have changed between interactions

    2. Verification Required
       - ALWAYS use check_relation tool before making access statements
       - FIRST use describe_store to get latest schema for permission questions
       - Never assume permissions based on previous interactions

    3. Explicit State Checking
       - Treat each interaction as independent
       - Clearly state when you are checking current permissions
       - Always verify current state before making statements

    4. Tool Usage
       - Use describe_store for understanding current schema
       - Use check_relation to verify specific permissions
       - Use write_relation to modify relations
       - Use update_store to modify schema

    Remember: The permission state can change at any time. Never rely on historical interactions
    to make statements about current permissions.
    """

    def __init__(self, store_id: str, permission_model: str) -> None:
        self._store_id = store_id
        self._messages: List[AIMessage] = []
        self._permission_model = permission_model
        self._tools = [t(store_id=store_id) for t in self.TOOLS]
        self._client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def _call_ai(self) -> Message:
        message = await self._client.messages.create(
            model=self.MODEL,
            max_tokens=1024,
            tools=[t.input_schema for t in self._tools],
            messages=[m.as_api_data for m in self._messages],
            system=self.SYSTEM_PROMPT.format(permission_model=self._permission_model),
        )

        return message

    def _call_tool(self, tool_block) -> Dict:
        tool = next(filter(lambda x: x.NAME == tool_block.name, self._tools))
        tool_result = tool.call(**tool_block.input)

        if any((isinstance(tool, c) for c in (UpdateStoreTool,))):
            self._permission_model = tool_block.input["model_str"]

        return {
            "type": "tool_result",
            "content": str(tool_result),
            "tool_use_id": tool_block.id,
        }

    async def get_answer(self, question: str) -> str:
        self._messages.append(AIMessage(role="user", content=question))
        message = await self._call_ai()
        self._messages.append(AIMessage(role="assistant", content=message.content))

        while message.stop_reason == "tool_use":
            tool_results = []
            for tool_block in [b for b in message.content if b.type == "tool_use"]:
                result = self._call_tool(tool_block=tool_block)
                tool_results.append(result)
                self._messages.append(AIMessage(role="user", content=tool_results))

            message = await self._call_ai()
            self._messages.append(AIMessage(role="assistant", content=message.content))

        return message.content[0].text

    @property
    def permission_model(self) -> str:
        return self._permission_model
