# IBKR Telegram Trading Bot (Single File)

Yeh project ek **Interactive Brokers (IBKR)** ke sath connected automated trading bot hai jo **Telegram commands aur webhook alerts** se control hota hai.

✅ **Single File Project** — Sab kuch `bot.py` mein hai.  
📡 **Telegram Commands** — Ticker set karo, test order bhejo, aur configurations check karo.  
📨 **Webhook** — TradingView alerts ya kisi external source se webhook trigger karo.

---

## 👨‍💻 Requirements

- Python 3.10+
- IB Gateway ya Trader Workstation (TWS)
- Telegram Bot Token
- IBKR Paper Trading Account

### Python Libraries

```bash
pip install flask python-telegram-bot==20.7 ib_insync
````

---

## 🚀 Run Bot

```bash
python bot.py
```

---

## 📲 Telegram Commands

| Command       | Example                                 | Description                                        |
| ------------- | --------------------------------------- | -------------------------------------------------- |
| `/start`      | —                                       | Bot instructions show karta hai                    |
| `/set`        | `/set AAPL 500 2.5`                     | Ticker set karo with dollar amount & target profit |
| `/show`       | —                                       | Saved configurations dikhata hai                   |
| `/test_order` | `/test_order AAPL BUY 190 5 2025-06-01` | Test order simulate karta hai                      |

---

## 🔁 Webhook Usage

### Endpoint:

```
POST http://<your-ip>:5000/webhook
```

### Payload Example:

```json
{
  "ticker": "AAPL",
  "action": "buy"
}
```

* `"buy"` → IBKR pe buy order place karega
* `"sell"` → Agar profit target achieve ho gaya ho to sell karega

---

## 💡 Example Output (Telegram)

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

## 🧾 Example Configuration (Auto saved in same folder)

```json
{
  "AAPL": {
    "order_size_usd": 500,
    "min_profit_percent": 2.5
  }
}
```

---

## 🧠 What This Bot Does Internally

* `Flask` ka use karke webhook endpoint create karta hai
* `ib_insync` ke through IBKR TWS ke sath connect hota hai
* Telegram commands se:

  * Configurations save hoti hain
  * Test order simulate hota hai
* Jab webhook `/webhook` call hota hai:

  * `buy` → Limit Buy order place hoti hai
  * `sell` → Agar profit percentage `target` se upar hai to Sell hoti hai

---

## 🔐 Security Tip

Make sure:

* `bot.py` 
* Server secure ho (use HTTPS/ngrok if exposing publicly)

---

## 📁 File Structure (Single File)

```
📁 Project Folder
 └── bot.py          # All logic is here
```


## 🤖 Telegram Setup Guide

1. BotFather se new bot banao aur token le lo
2. `bot.py` ke `TELEGRAM_TOKEN` variable mein paste karo
3. Run karo `python bot.py`
4. Telegram pe `/start` type karo

---

## 🧪 IB Gateway / TWS Settings

* Paper Trading enabled hona chahiye
* TWS/Gateway port: `7497`
* API Settings: Allow connections from localhost

---

## ✨ Author

Developed by **Jahanzaib**
GitHub: [github.com/jahanzaib-codes](https://github.com/jahanzaib-codes)
