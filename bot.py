import logging
import json
import os
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread
from ib_insync import IB, Stock, LimitOrder

# ========== Configuration ==========
TELEGRAM_TOKEN = "8175293763:AAEECMe9YOJErWjz3AnM9KbhZINchU-_aZg"
CONFIG_FILE = "configurations.json"
app = Flask(__name__)
ib = IB()

# ========== Load/Save Configs ==========
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(configs):
    with open(CONFIG_FILE, "w") as f:
        json.dump(configs, f, indent=2)

configs = load_config()

# ========== Telegram Bot Handlers ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 Welcome to the IBKR Trading Bot!\n\n"
        "Use these commands to get started:\n"
        "🔧 /set TICKER AMOUNT PROFIT% → Set trade config\n"
        "📊 /show → View all configured tickers\n"
        "🧪 /test_order TICKER BUY/SELL PRICE QTY DATE(YYYY-MM-DD) → Simulate test trade"
    )
    await update.message.reply_text(message)

async def set_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ticker = context.args[0].upper()
        amount = float(context.args[1])
        profit = float(context.args[2])
        configs[ticker] = {
            "order_size_usd": amount,
            "min_profit_percent": profit
        }
        save_config(configs)
        await update.message.reply_text(
            f"✅ Config saved:\n📈 {ticker}\n💰 ${amount}\n🎯 Profit Target: {profit}%"
        )
    except:
        await update.message.reply_text("❌ Usage: /set TICKER AMOUNT PROFIT")

async def show_configs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not configs:
        await update.message.reply_text("⚠️ No tickers configured yet.")
        return
    msg = "📊 Current Configurations:\n"
    for ticker, conf in configs.items():
        msg += f"🔹 {ticker}: ${conf['order_size_usd']} @ {conf['min_profit_percent']}% profit\n"
    await update.message.reply_text(msg)

async def test_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ticker = context.args[0].upper()
        side = context.args[1].upper()
        price = float(context.args[2])
        qty = int(context.args[3])
        date_str = context.args[4]
        datetime.strptime(date_str, "%Y-%m-%d")  # Validate date

        msg = (
            f"🧪 Test Order Simulation:\n"
            f"📅 Date: {date_str}\n"
            f"📈 Ticker: {ticker}\n"
            f"📥 Type: {side}\n"
            f"💵 Price: ${price:.2f}\n"
            f"🔢 Quantity: {qty}\n"
            f"🧾 Total: ${price * qty:.2f}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text("❌ Usage: /test_order TICKER BUY/SELL PRICE QTY DATE")

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("set", set_config))
    app_telegram.add_handler(CommandHandler("show", show_configs))
    app_telegram.add_handler(CommandHandler("test_order", test_order))

    async def run():
        await app_telegram.initialize()
        await app_telegram.start()
        await app_telegram.updater.start_polling()

    loop.run_until_complete(run())
    loop.run_forever()

# ========== IBKR Logic ==========
def connect_ib():
    if not ib.isConnected():
        ib.connect("127.0.0.1", 7497, clientId=1)

def place_limit_buy(ticker, usd_amount):
    try:
        connect_ib()
        stock = Stock(ticker, 'SMART', 'USD')
        ib.qualifyContracts(stock)
        price = ib.reqMktData(stock).last
        if not price or price <= 0:
            print(f"⚠️ Market price not available for {ticker}")
            return
        qty = round(usd_amount / price)
        order = LimitOrder('BUY', qty, price, outsideRth=True, tif='GTC')
        ib.placeOrder(stock, order)
        print(f"✅ BUY {ticker} | Qty: {qty} @ {price}")
    except Exception as e:
        print(f"❌ Buy error for {ticker}: {e}")

def place_limit_sell(ticker, profit_target):
    try:
        connect_ib()
        stock = Stock(ticker, 'SMART', 'USD')
        ib.qualifyContracts(stock)
        market_price = ib.reqMktData(stock).last
        positions = ib.positions()
        total_qty = sum(p.position for p in positions if p.contract.symbol == ticker)
        if total_qty == 0:
            print(f"ℹ️ No position in {ticker}")
            return
        avg_cost = ib.reqPnLSingle(ib.accountValues()[0].account, stock.conId).averageCost
        if avg_cost == 0:
            print(f"⚠️ No cost info for {ticker}")
            return
        return_pct = ((market_price - avg_cost) / avg_cost) * 100
        if return_pct >= profit_target:
            order = LimitOrder('SELL', total_qty, market_price, outsideRth=True, tif='GTC')
            ib.placeOrder(stock, order)
            print(f"✅ SELL {ticker} | Qty: {total_qty} @ {market_price}")
        else:
            print(f"📉 Profit {return_pct:.2f}% < Target {profit_target}%")
    except Exception as e:
        print(f"❌ Sell error for {ticker}: {e}")

# ========== Webhook (TradingView) ==========
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    ticker = data.get("ticker", "").upper()
    action = data.get("action", "").lower()

    if ticker not in configs:
        return jsonify({"error": "Ticker not configured"}), 400

    conf = configs[ticker]

    if action == "buy":
        place_limit_buy(ticker, conf["order_size_usd"])
        return jsonify({"status": f"Buy triggered for {ticker}"})
    elif action == "sell":
        place_limit_sell(ticker, conf["min_profit_percent"])
        return jsonify({"status": f"Sell evaluated for {ticker}"})
    else:
        return jsonify({"error": "Invalid action"}), 400

# ========== Run ==========
if __name__ == "__main__":
    Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=5000)
