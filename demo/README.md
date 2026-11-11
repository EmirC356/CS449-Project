# Full app: live local-LLM hints (`app.html`)

A working version of the study prototype: Python runs in the browser (Pyodide), tests run on every **Run**, and hints are **generated live** by a local LLM at the level the policy allows.

1. Start a local LLM server, e.g. Ollama: `ollama serve` (tested with `gpt-oss:20b`, about 3 s per hint once loaded).
2. `python demo/server.py`
3. Open **http://localhost:8765/**. Do not open the file directly: Ollama rejects `file://` pages (CORS).
4. In the start dialog, enter an anonymous ID (P01…) and pick **Study** (3 tasks, condition order from the ID) or **Free demo**. *Settings* lets you change the endpoint, model, API type (Ollama native or any OpenAI-compatible server such as LM Studio, llama.cpp, vLLM) and the hint language.

| Condition | Request does |
|---|---|
| A · Full answer | Generates the full fix (L4) |
| B · Hint only | Generates one conceptual hint (L2), no escalation |
| C · Calibrated | Next level L1→L4; the policy can also *offer* a hint (LED + vibration), Defer = quiet 2 min, Silence = no offers |

Inputs: ESP32 buttons through the relay, on-screen buttons, or Alt+1 / Alt+2 / Alt+3. Every run, hint, button press, confidence rating and questionnaire answer is logged in the browser (Settings → Export JSON/CSV) and in `demo/events.jsonl`.

**Known limitation:** live generation does not always respect the level rules (a 20B model sometimes leaks the cause at L1/L2). For the user study, review and freeze the hint ladders as planned.

# PP1 demo: ESP32 BOOT button → browser hint panel

Shows the real hardware path with **no extra parts**: the ESP32's built-in BOOT button and on-board LED.

```
BOOT button ──(Arduino C++)──► ESP32 ──Wi-Fi WebSocket──► Python relay (demo/server.py) ──► browser (demo/index.html)
on-board LED ◄──────────────── "blink" / "led_on" / "led_off" ◄───────────────────────────────┘
```

| Action | Event | What changes |
|---|---|---|
| Short press (< 1 s) | `request` | Hint panel moves to the next level (L1→L4), LED blinks |
| Long press (≥ 1 s) | `silence` | Proactive hints silenced, LED stays on (press again to undo) |
| On-screen buttons | same events | Fallback if the hardware fails |

## Run

1. **Laptop and ESP32 on the same Wi-Fi.** Use a phone hotspot in class (university Wi-Fi often blocks device-to-device traffic).
2. Start the relay:
   ```
   pip install websockets
   python demo/server.py
   ```
   It prints the laptop IP.
3. Arduino IDE: install the **esp32** board package (Espressif) and the **WebSockets** library (Markus Sattler). Open `firmware/pp1_boot_button_demo/`, set `WIFI_SSID`, `WIFI_PASS`, `SERVER_IP`, select *ESP32 Dev Module*, upload. Serial Monitor at 115200 shows `[ws] connected`.
4. Open `demo/index.html` in the browser. The status should say *Connected to relay*. If the relay runs on another machine, use `index.html?ws=ws://<ip>:8765`.
5. Press BOOT → the hint level changes in the browser. Every event is also appended to `demo/events.jsonl`.

## No hardware yet? Simulated ESP32 (backup mode)

With `server.py` running and `index.html` open, in a second terminal:
```
python demo/fake_esp32.py
```
Enter = short press (request), `s` + Enter = long press (silence), `q` + Enter = quit. It sends the same JSON as the firmware and prints the LED commands it gets back. The handbook allows a simulated signal only as a backup; the final demo must use the real ESP32.

## Troubleshooting
- On-board LED doesn't light: some boards use another pin; change `LED_PIN`.
- `[ws] disconnected` loop: wrong `SERVER_IP`, or Windows Firewall is blocking port 8765 (allow Python on private networks).
- Upload fails: hold BOOT while uploading starts, or check that the USB cable carries data.
