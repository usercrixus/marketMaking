from collections import deque

import sys
import os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import clientPro

class OHLCV:

    def __init__(self, symbol):
        self.symbol = symbol
        self.ohlcv = deque(maxlen=100) # example : [[1727463660000, 65139.4, 65339.9, 65072.2, 65072.2, 0.21000000000000002, 10], [1727463720000, 65339.9, 65339.9, 65339.9, 65339.9, 0.1, 1]]

    async def launch(self):
        await self.getOHLCV()

    async def getOHLCV(self):
        while True:
            try:
                trades = await clientPro.watch_trades(self.symbol)
                ohlcv = clientPro.build_ohlcvc(trades, '1m')
                self.ohlcv.append(ohlcv[0])
            except Exception as e:
                print(e)

'''
async def main():
    ohlcv = OHLCV('BTC/USDT')
    await ohlcv.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''