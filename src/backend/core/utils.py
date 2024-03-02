import datetime
import json
from typing import Union, Dict, List

from robyn import Response, Headers


def build_response(status_code: int, data: Union[Dict, List]) -> Response:
    return Response(
        status_code=status_code, headers=Headers({}), description=json.dumps(data)
    )


def get_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
