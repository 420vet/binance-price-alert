# Binance Price Alert

Real-time crypto price monitor with alerts for Binance spot pairs.
Live candlestick charts, dark/light theme, email & Telegram notifications.

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

---

## Run

```bash
git clone https://github.com/oottoo/binance-price-alert.git
cd binance-price-alert
pip install -r requirements.txt
python main.py
```

Open **http://localhost:8000** in your browser.

---

## Configuration

Edit `config.yaml`:

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

Made with ♥ by [420.vet](https://420.vet)
