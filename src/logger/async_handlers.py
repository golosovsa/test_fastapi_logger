import asyncio
from types import GenericAlias
from logging import Handler, getLevelName
from aioconsole import get_standard_streams

ASYNC_QUEUE_MAX_SIZE = 100


async def async_queue_to_stdout_worker(loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
    _, writer = await get_standard_streams(loop=loop)
    while True:
        msg = await queue.get()
        await writer.write(msg)
        await writer.drain()
        queue.task_done()


class AsyncQueueStdoutHandler(Handler):

    def __init__(self):
        try:
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        except RuntimeError:
            # First must run asynchronous loop
            raise

        Handler.__init__(self)

        self.loop = loop
        self.queue = asyncio.Queue(ASYNC_QUEUE_MAX_SIZE)
        self.task = self.loop.create_task(async_queue_to_stdout_worker(self.loop, self.queue))

    def emit(self, record):
        msg = f"☕: {self.format(record)}\n"
        self.queue.put_nowait(msg)

    async def shutdown(self):
        self.task.cancel()
        await asyncio.sleep(0)
        if not self.task.cancelled():
            await self.task

    def __repr__(self):
        level = getLevelName(self.level)
        name = self.queue.__class__.__name__
        capacity = self.queue.maxsize
        return '<%s %s(%s, %s)>' % (self.__class__.__name__, name, capacity, level)

    __class_getitem__ = classmethod(GenericAlias)
