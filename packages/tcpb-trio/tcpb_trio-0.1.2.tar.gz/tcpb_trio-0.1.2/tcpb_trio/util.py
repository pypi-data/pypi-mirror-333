import trio
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def aretry(times: int):
    def _wrapper(afn):
        @wraps(afn)
        async def _wrapped(*args, **kwargs):
            err = None
            for t in range(times):
                try:
                    return await afn(*args, **kwargs)
                except Exception as e:
                    logger.warn(f"{afn} raises {e}, retrying")
                    err = e
                await trio.sleep(0.1 * 2**t)
            raise err

        return _wrapped

    return _wrapper
