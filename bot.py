import logging
import json
import os
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread
from ib_insync import IB, Stock, LimitOrder

# ========= CONFIG =========
TELEGRAM_TOKEN = "telegram token"
TELEGRAM_USER_ID = telegramid
CONFIG_FILE = "configurations.json"
app = Flask(__name__)
ib = IB()
bot = Bot(TELEGRAM_TOKEN)

# ========= CONFIG LOAD/SAVE =========
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(configs):
    with open(CONFIG_FILE, "w") as f:
        json.dump(configs, f, indent=2)

configs = load_config()

# ========= TELEGRAM COMMANDS =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Welcome to the IBKR Trading Bot!\n\n"
        "Use these commands to get started:\n"
        "🔧 /set TICKER AMOUNT PROFIT → Set trade config\n"
        "📊 /show → Show configurations\n"
        "🧪 /test_order TICKER BUY/SELL PRICE QTY DATE(YYYY-MM-DD)"
    )
    await update.message.reply_text(msg)

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
            f"✅ Saved: {ticker} | ${amount} | Target: {profit}%"
        )
    except:
        await update.message.reply_text("❌ Usage: /set TICKER AMOUNT PROFIT")

async def show_configs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not configs:
        await update.message.reply_text("⚠️ No configurations yet.")
        return
    msg = "📊 Configurations:\n"
    for t, c in configs.items():
        msg += f"🔹 {t}: ${c['order_size_usd']} @ {c['min_profit_percent']}%\n"
    await update.message.reply_text(msg)

async def test_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ticker = context.args[0].upper()
        side = context.args[1].upper()
        price = float(context.args[2])
        qty = int(context.args[3])
        date_str = context.args[4]
        datetime.strptime(date_str, "%Y-%m-%d")
        total = price * qty
        msg = (
            f"🧪 Test Order:\n📅 {date_str}\n📈 {ticker}\n"
            f"📥 {side}\n💵 ${price:.2f}\n🔢 Qty: {qty}\n🧾 Total: ${total:.2f}"
        )
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("❌ Usage: /test_order TICKER BUY/SELL PRICE QTY DATE")

# ========= RANDOM SIGNAL ON START =========
async def send_random_signal():
    await asyncio.sleep(5)
    await bot.send_message(chat_id=TELEGRAM_USER_ID, text="🚀 Test Signal: BUY AAPL @ $182.35 | Qty: 10")

# ========= TELEGRAM BOT RUNNER =========
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
        await send_random_signal()  # 🚀 auto test signal

    loop.run_until_complete(run())
    loop.run_forever()

# ========= IBKR TRADING FUNCTIONS =========
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
            print(f"⚠️ Price unavailable: {ticker}")
            return
        qty = round(usd_amount / price)
        order = LimitOrder('BUY', qty, price, outsideRth=True, tif='GTC')
        ib.placeOrder(stock, order)
        print(f"✅ BUY {ticker} | Qty: {qty} @ ${price}")
    except Exception as e:
        print(f"❌ Buy failed for {ticker}: {e}")

def place_limit_sell(ticker, target_profit):
    try:
        connect_ib()
        stock = Stock(ticker, 'SMART', 'USD')
        ib.qualifyContracts(stock)
        market_price = ib.reqMktData(stock).last
        positions = ib.positions()
        qty = sum(p.position for p in positions if p.contract.symbol == ticker)
        if qty == 0:
            print(f"ℹ️ No holdings in {ticker}")
            return
        cost = ib.reqPnLSingle(ib.accountValues()[0].account, stock.conId).averageCost
        if cost == 0:
            print(f"⚠️ Missing cost info for {ticker}")
            return
        return_pct = ((market_price - cost) / cost) * 100
        if return_pct >= target_profit:
            order = LimitOrder('SELL', qty, market_price, outsideRth=True, tif='GTC')
            ib.placeOrder(stock, order)
            print(f"✅ SELL {ticker} | Qty: {qty} @ ${market_price}")
        else:
            print(f"📉 {ticker} Return: {return_pct:.2f}% < Target {target_profit}%")
    except Exception as e:
        print(f"❌ Sell failed for {ticker}: {e}")

# ========= WEBHOOK =========
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    ticker = data.get("ticker", "").upper()
    action = data.get("action", "").lower()

    if ticker not in configs:
        return jsonify({"error": "Not configured"}), 400

    conf = configs[ticker]

    if action == "buy":
        place_limit_buy(ticker, conf["order_size_usd"])
        return jsonify({"status": f"Buy triggered: {ticker}"})
    elif action == "sell":
        place_limit_sell(ticker, conf["min_profit_percent"])
        return jsonify({"status": f"Sell evaluated: {ticker}"})
    else:
        return jsonify({"error": "Invalid action"}), 400

# ========= MAIN =========
if __name__ == "__main__":
    Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=5000)
