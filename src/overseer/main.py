import typing

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket
from overseer.domain.ai import OverSeerAssistant
from typing import Optional
from overseer.clients import graph_fga_client

config = """
type user

"""


class OverseerEndpoint(WebSocketEndpoint):
    encoding = "json"

    def __init__(self, *args, **kwargs) -> None:
        self._overseer_assistant: Optional[OverSeerAssistant] = None
        super().__init__(*args, **kwargs)

    async def on_connect(self, websocket: WebSocket) -> None:
        store_id = graph_fga_client.store_create(model_str=config)
        self._overseer_assistant = OverSeerAssistant(
            store_id=store_id, permission_model=config
        )
        await websocket.accept()

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        question = data["question"]
        answer = await self._overseer_assistant.get_answer(question=question)
        await websocket.send_json(
            {
                "question": question,
                "answer": answer,
                "permission_model": self._overseer_assistant.permission_model,
            }
        )


routes = [WebSocketRoute("/overseer", OverseerEndpoint)]

app = Starlette(routes=routes)
