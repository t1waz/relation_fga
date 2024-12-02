import typing
from typing import Optional

from overseer_backend.clients import graph_fga_client
from overseer_backend.domain.ai import OverSeerAssistant
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import WebSocketRoute, Route
from starlette.websockets import WebSocket


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
        await websocket.send_json(
            {
                "permission_model": self._overseer_assistant.permission_model,
            }
        )

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


async def healthcheck(requet: Request, *args, **kwargs) -> Response:
    return Response(status_code=200)


routes = [
    Route("/healthcheck", healthcheck),
    WebSocketRoute("/overseer", OverseerEndpoint),
]

app = Starlette(routes=routes)
