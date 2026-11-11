"""Simulated ESP32 for testing without hardware (backup mode only).

Sends exactly the same JSON events as the real firmware and prints the LED
commands the browser sends back.

    python demo/fake_esp32.py                 # relay on this laptop
    python demo/fake_esp32.py 192.168.1.10    # relay on another machine

Keys: Enter = request, d + Enter = defer, s + Enter = silence,
      1-5 + Enter = confidence dial (planned potentiometer), q + Enter = quit
"""

import asyncio
import json
import sys

from websockets.asyncio.client import connect

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
URL = f"ws://{HOST}:8765"


async def listen(ws):
    async for message in ws:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            continue
        cmd = data.get("cmd")
        if data.get("vibrate"):
            print(f"  [VIBRATE] {data['vibrate']} ms")
        if cmd == "blink":
            print(f"  [LED] blink {data.get('led', '')}".rstrip())
        elif cmd == "led_on":
            print("  [LED] on (silenced)")
        elif cmd == "led_off":
            print("  [LED] off")


async def main():
    async with connect(URL) as ws:
        print(f"Fake ESP32 connected to {URL}")
        print("Enter = request | d = defer | s = silence | 1-5 = confidence dial | q = quit  (then Enter)")
        await ws.send(json.dumps({"source": "esp32", "event": "hello"}))
        listener = asyncio.create_task(listen(ws))
        while True:
            key = (await asyncio.to_thread(input)).strip().lower()
            if key == "q":
                break
            if key in ("1", "2", "3", "4", "5"):
                await ws.send(json.dumps({"source": "esp32", "event": "confidence", "value": int(key)}))
                print(f"-> sent confidence {key}")
                continue
            event = {"s": "silence", "d": "defer"}.get(key, "request")
            await ws.send(json.dumps({"source": "esp32", "event": event}))
            print(f"-> sent {event}")
        listener.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, ConnectionRefusedError, OSError) as e:
        if not isinstance(e, KeyboardInterrupt):
            print(f"Could not reach the relay at {URL}. Is 'python server.py' running?")
