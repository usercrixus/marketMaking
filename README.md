# Binance Futures Market Making Bot

This is a handcrafted prototype of a **market making algorithm** designed to operate on the Binance Futures Testnet.

It was built **without access to simulation engines, replay systems, or proprietary infra** — only raw testnet interactions. The bot dynamically places bid/ask orders based on live orderbook data, inventory exposure, and portfolio sizing.

---

## 🧠 Strategy Overview

- **Spread-based quoting** around the midprice.
- **Inventory-aware adaptation**: prices shift dynamically depending on position size and direction.
- **Defensive pricing logic** when exposure grows: asymmetric quote control to avoid liquidation risk.
- **Size control** relative to account margin and midprice.
- **Execution tested in live testnet environment**.

This strategy is **not passive**. It reacts to the market and to itself — a simple, interactive agent in a real game.

---

## ⚠️ Limitations

- No live capital: testnet-only for now.
- Prototype-level architecture: not optimized for latency or production-grade robustness.
- Requires a realistic environment to progress further — a simulated live market engine, not a classic backtest, to explore **market influence and agent interaction**.

---

## 🚀 Why this matters

This was built from scratch — alone — as a learning and research tool.  
If you're a **fund, a desk, or a team building market infrastructure**, and this kind of exploratory thinking speaks to you: feel free to reach out.

I’m currently seeking a team where this type of work can be taken further — with the right tools, data, and mentorship.

---

## Setup

Update your API keys in `config.py`, then:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
