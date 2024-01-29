from typing import Dict

from robyn import SubRouter
from robyn.robyn import Request

stores_router = SubRouter(__name__, prefix="/stores")


@stores_router.post(f"/write")
async def store_write_endpoint(request: Request) -> Dict:
    return {}
