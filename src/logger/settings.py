import logging
from typing import cast

from src.logger.async_handlers import AsyncQueueStdoutHandler


async def startup_logger():
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    base_logger = logging.getLogger()

    uvicorn_error_logger.setLevel(logging.DEBUG)
    uvicorn_access_logger.setLevel(logging.DEBUG)
    base_logger.setLevel(logging.DEBUG)

    uvicorn_error_logger.handlers.clear()
    uvicorn_error_logger.addHandler(AsyncQueueStdoutHandler())

    uvicorn_access_logger.handlers.clear()
    uvicorn_access_logger.addHandler(AsyncQueueStdoutHandler())

    base_logger.handlers.clear()
    base_logger.addHandler(AsyncQueueStdoutHandler())


async def _shutdown_async_handlers(handlers: list):
    for handler in handlers:
        if isinstance(handler, AsyncQueueStdoutHandler):
            handler = cast(AsyncQueueStdoutHandler, handler)
            await handler.shutdown()


async def shutdown_logger():
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    base_logger = logging.getLogger()

    await _shutdown_async_handlers(uvicorn_error_logger.handlers)
    await _shutdown_async_handlers(uvicorn_access_logger.handlers)
    await _shutdown_async_handlers(base_logger.handlers)
