import sys
import os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import clientPro

class Orderbook:

    def __init__(self, symbol):
        self.symbol = symbol
        self.bids = [] # example : [[64875.1, 4.923], [64872.2, 8.126], [64870.0, 0.003], [64859.9, 0.003], [64846.3, 0.007], ...
        self.asks = [] # example : [[65059.4, 0.133], [65070.0, 1.8], [65158.3, 0.005], [65288.4, 0.005], [65299.9, 56.02], ...

    async def launch(self):
        await self.getOrderbook()

    async def getOrderbook(self):
        while True:
            try:
                orderbook = await clientPro.watch_order_book(self.symbol)
                self.bids = orderbook["bids"]
                self.asks = orderbook["asks"]
            except Exception as e:
                print(e)

'''
async def main():
    orderbook = Orderbook('BTC/USDT')
    await orderbook.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''