from collections import deque

import sys
import os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import clientPro

class Trades:

    def __init__(self, symbol):
        self.symbol = symbol
        self.trades = deque(maxlen=100)
        '''
        Example :
        [
            {
                "info":{
                    "e":"trade",
                    "E":1727464529850,
                    "T":1727464529850,
                    "s":"BTCUSDT",
                    "t":289965272,
                    "p":"65207.20",
                    "q":"0.012",
                    "X":"MARKET",
                    "m":false
                },
                "timestamp":1727464529850,
                "datetime":"2024-09-27T19:15:29.850Z",
                "symbol":"BTC/USDT:USDT",
                "id":"289965272",
                "order":"None",
                "type":"None",
                "side":"buy",
                "takerOrMaker":"None",
                "price":65207.2,
                "amount":0.012,
                "cost":782.4864,
                "fee":{
                    "cost":"None",
                    "currency":"None"
                },
                "fees":[
                    
                ]
            },
            {
                "info":{
                    "e":"trade",
                    "E":1727464529850,
                    "T":1727464529850,
                    "s":"BTCUSDT",
                    "t":289965273,
                    "p":"65207.20",
                    "q":"0.012",
                    "X":"MARKET",
                    "m":false
                },
                "timestamp":1727464529850,
                "datetime":"2024-09-27T19:15:29.850Z",
                "symbol":"BTC/USDT:USDT",
                "id":"289965273",
                "order":"None",
                "type":"None",
                "side":"buy",
                "takerOrMaker":"None",
                "price":65207.2,
                "amount":0.012,
                "cost":782.4864,
                "fee":{
                    "cost":"None",
                    "currency":"None"
                },
                "fees":[
                    
                ]
            }
        ]
        '''

    async def launch(self):
        await self.getTrades()

    async def getTrades(self):
        while True:
            try:
                trades = await clientPro.watch_trades(self.symbol)
                for trade in trades:
                    self.trades.append(trade)
            except Exception as e:
                print(e)

'''
async def main():
    trades = Trades('BTC/USDT')
    await trades.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''