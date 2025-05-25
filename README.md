
# IBKR Telegram Trading Bot (Single File)

This is a fully self-contained trading bot that connects to **Interactive Brokers (IBKR)** and is controlled via **Telegram commands** and **webhook alerts**.

✅ **Single File Project** — Everything is in `bot.py`.  
📡 **Telegram Commands** — Configure tickers, simulate orders, view saved configs.  
📨 **Webhook Integration** — Trigger orders from TradingView or any webhook source.

---

## 👨‍💻 Requirements

- Python 3.10+
- IB Gateway or Trader Workstation (TWS)
- Telegram Bot Token
- IBKR Paper Trading Account

### Python Libraries

```bash
pip install flask python-telegram-bot==20.7 ib_insync
```

---

## 🚀 Run the Bot

```bash
python bot.py
```

---

## 📲 Telegram Commands

| Command | Example | Description |
|--------|---------|-------------|
| `/start` | — | Shows bot instructions |
| `/set` | `/set AAPL 500 2.5` | Set ticker with amount (USD) and profit target (%) |
| `/show` | — | Displays current configurations |
| `/test_order` | `/test_order AAPL BUY 190 5 2025-06-01` | Simulates a test trade with given parameters |

---

## 🔁 Webhook Usage

### Endpoint:

```
POST http://<your-ip>:5000/webhook
```

### Example Payload:

```json
{
  "ticker": "AAPL",
  "action": "buy"
}
```

- `"buy"` → Places a limit buy order on IBKR
- `"sell"` → Sells if profit target is met

---

## 📥 Telegram Output Example

```
🧪 Test Order Simulation:
📅 Date: 2025-06-01
📈 Ticker: AAPL
📥 Type: BUY
💵 Price: $190.00
🔢 Quantity: 5
🧾 Total: $950.00
```

---

## 🧾 Example Configuration (Auto-saved)

```json
{
  "AAPL": {
    "order_size_usd": 500,
    "min_profit_percent": 2.5
  }
}
```

---

## ⚙️ Internal Logic

- Uses `Flask` for the webhook endpoint
- Uses `ib_insync` to connect to IBKR TWS
- Telegram commands:
  - Save configuration
  - Simulate test order
- Webhook `/webhook`:
  - `buy` → Places order using saved config
  - `sell` → Checks live position, sells if profit target met

---

## 🔐 Security Tips

- Store Telegram token securely (use env variables in production)
- If exposing server to internet, secure with HTTPS or use `ngrok`

---

## 📁 File Structure

```
📁 Project Folder
 └── bot.py          # All logic in a single file
```

No other files needed. Everything is handled within `bot.py`.

---

## 🤖 Telegram Bot Setup

1. Create bot via BotFather, get the token
2. Paste token in `bot.py` under `TELEGRAM_TOKEN`
3. Run with `python bot.py`
4. On Telegram, type `/start`

---

## 🧪 IB Gateway / TWS Setup

- Paper Trading account must be enabled
- TWS/Gateway must run on port `7497`
- Enable API access from localhost

---

## ✨ Author

Built by **Jahanzaib**  
GitHub: [github.com/jahanzaib-codes](https://github.com/jahanzaib-codes)

---

## 📄 License

MIT License — Free to use, share, and modify.
