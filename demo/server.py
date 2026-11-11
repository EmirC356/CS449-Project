"""PP1 demo relay: ESP32 <-> WebSocket <-> browser.

Every message from one client is forwarded to all other clients and appended
to events.jsonl (timestamped), which is the seed of the study event log.

    pip install websockets
    python demo/server.py            # then open demo/index.html in a browser
"""

import asyncio
import json
import socket
import time
from pathlib import Path

from websockets.asyncio.server import broadcast, serve

PORT = 8765
LOG_PATH = Path(__file__).with_name("events.jsonl")
clients = set()


def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def log(message: str) -> None:
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        data = {"raw": message}
    data["t"] = round(time.time(), 3)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
    print(data)


async def handler(ws):
    clients.add(ws)
    print(f"+ client {ws.remote_address} ({len(clients)} connected)")
    try:
        async for message in ws:
            log(message)
            broadcast(clients - {ws}, message)
    finally:
        clients.discard(ws)
        print(f"- client {ws.remote_address} ({len(clients)} connected)")


async def main() -> None:
    async with serve(handler, "0.0.0.0", PORT):
        print(f"Relay running on ws://{local_ip()}:{PORT}")
        print(f"Put {local_ip()} into SERVER_IP in the ESP32 sketch.")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
