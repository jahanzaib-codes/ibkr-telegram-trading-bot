```markdown
# 🤖 IBKR Telegram Trading Bot (Beginner's Guide)

## 📌 What This Bot Does
1. Connects to your IBKR account
2. Lets you trade via Telegram messages
3. Works with TradingView webhooks

## 🛠️ Setup (3 Steps)

### 1. Install Requirements
```bash
pip install ib_insync python-telegram-bot flask
```

### 2. Edit These Lines in bot.py
```python
TELEGRAM_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # Get from @BotFather
TELEGRAM_CHAT_ID = "1798492490"  # Your Telegram ID (get from @userinfobot)
IBKR_HOST = "127.0.0.1"         # Keep this if running on same computer
IBKR_PORT = 7497                # Default IBKR port
```

### 3. Run the Bot
```bash
python bot.py
```

## 📱 Basic Telegram Commands

### Set Up a Trade
```bash
/set AAPL 500 3
```
(Means: Trade $500 of AAPL with 3% profit target)

### Check Settings
```bash
/show
```

### Test a Trade (No real money)
```bash
/test_order TSLA BUY 250 2 2024-05-01
```

### Real Trade
```bash
/trade NVDA BUY 900 1
```

## 🌐 Webhook Setup (For TradingView)

1. Use this URL:
```bash
http://your-server-ip:5000/webhook
```

2. Send this JSON:
```json
{
  "ticker": "AAPL",
  "action": "buy",
  "price": 182.50
}
```

## 📁 All Files Explained

### 1. bot.py (Main File)
```python
# This is your main bot file
# It contains all the code to:
# - Read Telegram messages
# - Connect to IBKR
# - Save your settings
```

### 2. configurations.json (Auto-Created)
```json
{
  "AAPL": {
    "order_size_usd": 500,
    "min_profit_percent": 3.0
  }
}
```
(The bot creates this automatically)

### 3. .gitignore (Optional)
```bash
configurations.json
```
(Prevents saving your settings online)

## ▶️ How to Start Trading
1. Open IBKR Trader Workstation
2. Keep it running in background
3. Run the bot:
```bash
python bot.py
```
4. Send commands from Telegram

## ❓ Common Issues
1. Bot not responding?
   - Check your Telegram token
2. IBKR connection failed?
   - Make sure Trader Workstation is open
3. Webhook not working?
   - Check your firewall settings

```
