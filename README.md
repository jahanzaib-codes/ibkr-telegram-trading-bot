# IBKR Auto-Trading Bot

This bot automates trade execution using Interactive Brokers, configurable via Telegram and triggered via TradingView alerts.

---

## 💡 Features

- Configure trade presets via Telegram
- Receive webhook alerts (Buy/Sell) from TradingView
- Auto-place GTC Limit Orders using IBKR API
- Dollar-Cost Averaging (DCA)
- Profit-based Sell conditions

---

## ⚙️ Telegram Commands

- `/start` – Show welcome message
- `/set TICKER ORDER_USD PROFIT_PERCENT`
  - Example: `/set AAPL 1000 3.5`
- `/show` – View all active configurations

---

## 🔗 Webhook Format (TradingView)

Webhook URL: `http://your-server-ip:5000/webhook`

Send JSON:
```json
{
  "action": "buy",
  "ticker": "AAPL"
}
