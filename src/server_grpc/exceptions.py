import functools
from typing import Any

import grpc
from google.protobuf.message import Message
import traceback


class ServiceException(Exception):
    pass


class InvalidRequestException(ServiceException):
    pass


def handle_invalid_request_exception(
    exc: InvalidRequestException,
    request: Message,
    context: grpc.ServicerContext,
) -> Any:
    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
    context.set_details(str(exc))

    return Message


EXCEPTION_CODE_MAPPING = {
    InvalidRequestException: handle_invalid_request_exception,
}


def handle_exception(func):
    @functools.wraps(func)
    def wrapper(self, request: Message, context: grpc.ServicerContext, *args, **kwargs):
        try:
            return func(self, request, context, *args, **kwargs)
        except Exception as exc:
            exception_handler = EXCEPTION_CODE_MAPPING.get(type(exc))
            if not exception_handler:
                error_traceback = traceback.format_exc()
                print(
                    f"no exception handler for: {exc}, type: {type(exc)} {error_traceback}"
                )  # noqa
                context.set_code(grpc.StatusCode.UNKNOWN)
                context.set_details(
                    f"no exception handler for: {exc}, type: {type(exc)} {error_traceback}"
                )
                return Message()

            return exception_handler(exc=exc, request=request, context=context)()

    return wrapper
