class AppException(Exception):
    def __init__(self, msg: str) -> None:
        self._msg = msg

    @property
    def msg(self) -> str:
        return self._msg
