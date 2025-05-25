# 📊 IBKR Telegram Trading Bot with Webhooks & Testing

A powerful, self-contained Python bot that integrates **Interactive Brokers (IBKR)** trading with a **Telegram bot interface**, complete with test order simulation, webhook support (e.g., TradingView), and dynamic configuration management.

---

## 📁 Project Overview

This bot allows you to:
- Configure trading parameters for stocks via Telegram.
- Receive trade alerts via webhook (e.g., from TradingView).
- Execute live **limit buy/sell orders** via IBKR.
- Simulate historical/test orders via Telegram.
- Receive real-time responses and trade simulations directly to your Telegram.

---

## 🚀 Features

- 📱 Telegram Bot Integration
- 🔁 Webhook endpoint for auto-trade signals
- ⚙️ IBKR order execution (Buy/Sell)
- 💼 Config persistence in JSON
- 🧪 Test historical orders
- 📢 Sends **demo trade signal** on launch

---

## 🔧 Requirements

- Python 3.8+
- IB Gateway or TWS running at `127.0.0.1:7497`
- Telegram Bot Token
- Your Telegram User ID

Install dependencies:

```bash
pip install flask python-telegram-bot==20.3 ib_insync
