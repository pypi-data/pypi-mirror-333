from .msg import terachem_server_pb2 as tcpb2
from .conn import send, recv
from .input import JobInput

import trio


class TCPBClient:
    """Implementation of TeraChem CommBox client API on top of Trio socket."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.so = None

    async def connect(self):
        self.so = await trio.open_tcp_stream(self.host, self.port)
        return self

    async def aclose(self, *_):
        if self.so:
            await self.so.aclose()

    __aenter__ = connect
    __aexit__ = aclose

    async def is_available(self) -> bool:
        status = await self._request(tcpb2.STATUS)
        return not status.busy

    async def compute(self, inputf_or_msg: str | bytes) -> tcpb2.JobOutput:
        _ = await self.send_job(inputf_or_msg)
        while not await self.check_job_complete():
            await trio.sleep(1)
        return await self.recv_job()

    async def _send_job(self, msg: bytes) -> tcpb2.Status:
        status = await self._request(tcpb2.JOBINPUT, msg)
        if status.WhichOneof("job_status") != "accepted":
            raise RuntimeError("job submission failed")
        return status

    async def send_job(self, inputf_or_msg: str | bytes) -> tcpb2.Status:
        if type(inputf_or_msg) is str:
            job = JobInput.from_file(inputf_or_msg)
            msg = job.encode()
        else:
            msg = inputf_or_msg
        return await self._send_job(msg)

    async def recv_job(self) -> tcpb2.JobOutput:
        rt, r = await recv(self.so)
        assert rt == tcpb2.JOBOUTPUT, "unexpected job output msg"
        assert len(r) > 0, "empty job output msg"
        output = tcpb2.JobOutput()
        output.ParseFromString(r)
        return output

    async def check_job_complete(self) -> bool:
        status = await self._request(tcpb2.STATUS)
        match status.WhichOneof("job_status"):
            case "working":
                return False
            case "completed":
                return True
            case _:
                raise RuntimeError("invalid job status")

    async def _request(self, msgtype: int, payload: bytes = b"") -> tcpb2.Status:
        await send(self.so, msgtype, payload)
        rt, r = await recv(self.so)
        assert rt == tcpb2.STATUS, "unexpected status msg"
        status = tcpb2.Status()
        status.ParseFromString(r)
        return status
