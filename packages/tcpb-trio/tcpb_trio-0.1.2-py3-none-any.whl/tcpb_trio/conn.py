import trio
import struct
import io

HEADER_FMT = "!LL"  # network endian, 2 unsigned long
HEADER_SZ = struct.calcsize(HEADER_FMT)


async def send(s: trio.abc.SendStream, msgtype: int, msg: bytes):
    header = struct.pack(HEADER_FMT, msgtype, len(msg))
    await s.send_all(header + msg)


async def recv(s: trio.abc.ReceiveStream) -> (int, bytes):
    bh = await receive_exactly(s, HEADER_SZ)
    msgtype, msgsz = struct.unpack(HEADER_FMT, bh)
    return msgtype, await receive_exactly(s, msgsz)


async def receive_exactly(s: trio.abc.ReceiveStream, n: int) -> bytes:
    buf = io.BytesIO()
    while n > 0:
        data = await s.receive_some(n)
        if data == b"":
            raise EOFError("end of receive stream")
        buf.write(data)
        n -= len(data)
    return buf.getvalue()
