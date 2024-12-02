import typing
from typing import Optional

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import WebSocketRoute, Route
from starlette.websockets import WebSocket

from overseer_backend.clients import graph_fga_client
from overseer_backend.domain.ai import OverSeerAssistant
from overseer_backend.logger import logger


DEFAULT_STORE_PERMISSION_MODEL = """
type user

"""


class OverseerEndpoint(WebSocketEndpoint):
    encoding = "json"

    def __init__(self, *args, **kwargs) -> None:
        self._overseer_assistant: Optional[OverSeerAssistant] = None
        super().__init__(*args, **kwargs)

    async def on_connect(self, websocket: WebSocket) -> None:
        existing_store_ids = graph_fga_client.store_list()
        if existing_store_ids:
            store_id = existing_store_ids[0]
            logger.info(f"store exist, connecting to: {store_id}")
        else:
            store_id = graph_fga_client.store_create(
                model_str=DEFAULT_STORE_PERMISSION_MODEL
            )
            logger.info("no existing stores, creating new one")

        permission_model = graph_fga_client.store_view(store_id=store_id)

        self._overseer_assistant = OverSeerAssistant(
            store_id=store_id, permission_model=permission_model
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
