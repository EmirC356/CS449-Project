"""Relay + static server: ESP32 <-> WebSocket <-> browser.

    pip install websockets
    python demo/server.py

    http://localhost:8765/       full app (app.html, live local-LLM hints)
    http://localhost:8765/demo   PP1 hint-panel demo (index.html)
    ws://<laptop-ip>:8765        WebSocket relay for the ESP32 and the pages

Every WebSocket message is appended to events.jsonl with a timestamp.
Messages are forwarded to all other clients, except {"type": "log"} records,
which are only written to the log file.

The pages must be opened through this server (http://localhost), not as
file:// - Ollama rejects requests from file:// pages (CORS).
"""

import asyncio
import json
import socket
import time
from pathlib import Path

from websockets.asyncio.server import broadcast, serve
from websockets.datastructures import Headers
from websockets.http11 import Response

PORT = 8765
HERE = Path(__file__).parent
LOG_PATH = HERE / "events.jsonl"
ROUTES = {"/": "app.html", "/app": "app.html", "/demo": "index.html"}
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


def log(data: dict) -> None:
    data["t"] = round(time.time(), 3)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def process_request(connection, request):
    """Serve the HTML pages over plain HTTP; let WebSocket upgrades through."""
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return None
    path = request.path.split("?", 1)[0]
    name = ROUTES.get(path)
    if name is None:
        return connection.respond(404, "Not found\n")
    body = (HERE / name).read_bytes()
    headers = Headers([
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-store"),
    ])
    return Response(200, "OK", headers, body)


async def handler(ws):
    clients.add(ws)
    print(f"+ client {ws.remote_address} ({len(clients)} connected)")
    try:
        async for message in ws:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                data = {"raw": message}
            log(dict(data))
            if data.get("type") == "log":
                continue  # study log record: file only, never sent to the ESP32
            print(data)
            broadcast(clients - {ws}, message)
    finally:
        clients.discard(ws)
        print(f"- client {ws.remote_address} ({len(clients)} connected)")


async def main() -> None:
    async with serve(handler, "0.0.0.0", PORT, process_request=process_request):
        ip = local_ip()
        print(f"App:   http://localhost:{PORT}/")
        print(f"Demo:  http://localhost:{PORT}/demo")
        print(f"Relay: ws://{ip}:{PORT}   (put {ip} into SERVER_IP in the ESP32 sketch)")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
