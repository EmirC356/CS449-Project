// PP1 demo: ESP32 built-in BOOT button -> WebSocket -> browser hint panel.
// No extra parts needed. Uses GPIO0 (BOOT button) and GPIO2 (on-board LED on most DevKit boards).
//
//   short press (< 1 s)  -> {"event":"request"}  (ask for the next hint level)
//   long press  (>= 1 s) -> {"event":"silence"}  (toggle proactive hints off/on)
//
// The server can send back: "led_on", "led_off", "blink".
//
// Library: "WebSockets" by Markus Sattler (Arduino Library Manager).
// Board:   "ESP32 Dev Module" (esp32 board package by Espressif).

#include <WiFi.h>
#include <WebSocketsClient.h>

// ---- edit these ----
const char* WIFI_SSID   = "YOUR_WIFI_OR_HOTSPOT";
const char* WIFI_PASS   = "YOUR_PASSWORD";
const char* SERVER_IP   = "192.168.1.10";  // laptop IP, printed by demo/server.py
const uint16_t SERVER_PORT = 8765;
// --------------------

const int BUTTON_PIN = 0;   // BOOT button, active LOW
const int LED_PIN    = 2;   // on-board LED (change if your board differs)

const unsigned long DEBOUNCE_MS   = 30;
const unsigned long LONG_PRESS_MS = 1000;

WebSocketsClient ws;
bool wsConnected = false;

int  stableState = HIGH;
int  lastReading = HIGH;
unsigned long lastChangeMs = 0;
unsigned long pressStartMs = 0;

bool ledSteady = false;          // LED on = hints silenced
unsigned long blinkUntilMs = 0;

void sendEvent(const char* name) {
  String msg = String("{\"source\":\"esp32\",\"event\":\"") + name + "\"}";
  Serial.println(msg);           // serial fallback: same JSON over USB
  if (wsConnected) ws.sendTXT(msg);
}

void onWsEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_CONNECTED:
      wsConnected = true;
      Serial.println("[ws] connected");
      sendEvent("hello");
      break;
    case WStype_DISCONNECTED:
      wsConnected = false;
      Serial.println("[ws] disconnected, retrying...");
      break;
    case WStype_TEXT: {
      const char* text = (const char*)payload;
      if (strstr(text, "led_on"))  ledSteady = true;
      if (strstr(text, "led_off")) ledSteady = false;
      if (strstr(text, "blink"))   blinkUntilMs = millis() + 600;
      break;
    }
    default:
      break;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("[wifi] connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.print("\n[wifi] ip: ");
  Serial.println(WiFi.localIP());

  ws.begin(SERVER_IP, SERVER_PORT, "/");
  ws.onEvent(onWsEvent);
  ws.setReconnectInterval(2000);
}

void loop() {
  ws.loop();
  unsigned long now = millis();

  // Debounced button handling
  int reading = digitalRead(BUTTON_PIN);
  if (reading != lastReading) {
    lastChangeMs = now;
    lastReading = reading;
  }
  if ((now - lastChangeMs) > DEBOUNCE_MS && reading != stableState) {
    stableState = reading;
    if (stableState == LOW) {
      pressStartMs = now;                       // pressed
    } else {
      unsigned long held = now - pressStartMs;  // released
      sendEvent(held >= LONG_PRESS_MS ? "silence" : "request");
    }
  }

  // LED: fast blink after a hint, steady when silenced
  if (now < blinkUntilMs) {
    digitalWrite(LED_PIN, (now / 100) % 2);
  } else {
    digitalWrite(LED_PIN, ledSteady ? HIGH : LOW);
  }
}
