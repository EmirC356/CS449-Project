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

## Troubleshooting
- On-board LED doesn't light: some boards use another pin; change `LED_PIN`.
- `[ws] disconnected` loop: wrong `SERVER_IP`, or Windows Firewall is blocking port 8765 (allow Python on private networks).
- Upload fails: hold BOOT while uploading starts, or check that the USB cable carries data.
