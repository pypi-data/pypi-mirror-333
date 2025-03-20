from .msg import terachem_server_pb2 as tcpb2
from .client import TCPBClient

import trio
from concurrent.futures import Future
from queue import SimpleQueue
from functools import partial


class TCPBSyncClient:
    def __init__(self, host: str, port: int):
        self._aclient = TCPBClient(host, port)

    def __enter__(self):
        self.connect()
        return self


def trio_guest(afn_name):
    def fn(self, *args, **kwargs):
        fu, main_thread_portal = Future(), SimpleQueue()

        def run_sync_soon_threadsafe(fn):
            main_thread_portal.put_nowait(fn)

        def done_callback(val_or_exp):
            fu.set_result(val_or_exp)

        afn = getattr(self._aclient, afn_name)
        trio.lowlevel.start_guest_run(
            partial(afn, *args, **kwargs),
            run_sync_soon_threadsafe=run_sync_soon_threadsafe,
            done_callback=done_callback,
        )
        while True:
            t = main_thread_portal.get()
            t()
            if fu.done():
                return fu.result().unwrap()

    return fn


for fn_, afn_ in (
    ("connect", "connect"),
    ("close", "aclose"),
    ("__exit__", "__aexit__"),
    ("is_available", "is_available"),
    ("compute", "compute"),
):
    setattr(TCPBSyncClient, fn_, trio_guest(afn_))
