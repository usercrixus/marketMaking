# client.py

import ccxt.async_support
from config import API_KEY, API_SECRET
import ccxt
import ccxt.pro

# Initialize the Binance client for the testnet
client = ccxt.async_support.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {
        'defaultType': 'future',  # Specify 'future' for Binance Futures trading
    },
})
# Enable testnet mode
client.set_sandbox_mode(True)

# Initialize WebSocket client
clientPro = ccxt.pro.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {
        'defaultType': 'future',  # Specify 'future' for Binance Futures trading
    },
})
# Enable testnet mode
clientPro.set_sandbox_mode(True)
