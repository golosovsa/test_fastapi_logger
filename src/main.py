import logging
from contextlib import asynccontextmanager

from .logger.settings import startup_logger, shutdown_logger

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_logger()
    logger = logging.getLogger()
    logger.debug("Hello world")
    yield
    logger.debug("Goodbye world")
    await shutdown_logger()


application = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@application.get('/')
def ping():
    return "pong"


if __name__ == '__main__':
    uvicorn.run(
        'src.main:application',
        host='0.0.0.0',
        port=8000,
    )

