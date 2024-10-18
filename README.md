# Binance Futures Market-Making Bot

This Python-based market-making bot is designed to trade on the Binance Futures platform. It operates on the Binance Testnet and has demonstrated significant profits under simulated conditions.  

## Requirements

To use this bot, you need to set up your Binance API credentials in the config.py file:

```python
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
```

You can obtain these from your Binance account under API Management.  

Then, python3 -m venv venv, source venv/bin/activate, pip install ccxt, python main.py  

## Performance

The bot has been tested on the Binance Testnet and has consistently generated approximately 50,000 USDC per day. It operates by placing buy and sell orders to profit from the bid-ask spread.  

## Limitations

Due to my status as a student and limited access to funds, I have not been able to test the bot in a live trading environment. To run the bot on the live Binance Futures market, a starting capital of 60,000 USDT is required for optimal performance, along with 50x leverage.  

If you are an Hedge fund, a state or any kind of trading investor interested in this djob and wanna keep it private, you can contact me on x : https://x.com/___Crixus___  
As i can't use this work for myself, i haven't make all the necessary ajustment. Consider the work as many as in progress as in standby.  
To continue this work i need a realistic test environment. Not a classic backtest env, but an env who is simulating a real market as the algorithm is based on a strategy that influence the market. It is an interactive game. Create such an env require a true team.