# Binance Price Alert

Real-time crypto price monitor with alerts for Binance spot pairs.
Live candlestick charts, dark/light theme, email & Telegram notifications.

![Version](https://img.shields.io/badge/version-1.0.2-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- Live price table for any Binance USDT pair (WebSocket)
- Candlestick chart with volume bars (5m / 15m / 1h / 4h / 1d)
- Price change alerts with configurable threshold and time window
- Email (SMTP) and Telegram notifications
- Dark / light theme
- Single-file executable — no Python required

---

## Download

Pre-built binaries for every release:

| Platform | File |
|----------|------|
| Windows  | `trade-alert-windows.exe` |
| macOS    | `trade-alert-macos` |
| Linux    | `trade-alert-linux` |

→ [Latest release](https://github.com/oottoo/binance-price-alert/releases/latest)

Just download, place in a folder, and run. A `config.yaml` is created automatically next to the executable on first launch.

> **Windows note:** if SmartScreen warns about an unknown publisher, click *More info → Run anyway*. The binary is unsigned but clean — built without UPX compression specifically to avoid Defender false positives.

---

## Run from source

```bash
git clone https://github.com/oottoo/binance-price-alert.git
cd binance-price-alert
pip install -r requirements.txt
python main.py
```

Open **http://localhost:8000** in your browser.

---

## Configuration

Edit `config.yaml` (created automatically next to the executable):

```yaml
symbols:
  - BTC
  - ETH
  - BNB

alert_threshold: 1        # % change to trigger an alert
alert_window_min: 5       # lookback window in minutes
poll_interval: 10         # seconds between price checks
reset_hour: 0             # hour (UTC) to reset daily stats

email:
  enabled: false
  smtp_host: smtp.gmail.com
  smtp_port: 587
  user: you@gmail.com
  password: your_app_password
  to: recipient@gmail.com

telegram:
  enabled: false
  bot_token: 123456:ABC-xxx
  chat_id: "987654321"
```

Settings can also be changed live from the **⚙ Settings** panel in the UI.

---

## Build from source

Requires [PyInstaller](https://pyinstaller.org):

```bash
pip install pyinstaller
python -m PyInstaller trade_alert.spec
# → dist/trade-alert.exe  (Windows)
# → dist/trade-alert      (macOS / Linux)
```

CI builds for all three platforms run automatically on every `v*` tag via GitHub Actions.

---

Made with ♥ by [420.vet](https://420.vet)
