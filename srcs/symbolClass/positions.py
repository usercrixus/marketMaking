import asyncio

import sys
import os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import clientPro, client

class Positions:

    def __init__(self, symbol):
        self.symbol = symbol
        self.position = {}
        '''
        example :
        {
            "info":{
                "symbol":"BTCUSDT",
                "positionSide":"BOTH",
                "positionAmt":"0.016",
                "entryPrice":"65212.5625",
                "breakEvenPrice":"65238.64752501",
                "markPrice":"65809.37534989",
                "unRealizedProfit":"9.54900559",
                "liquidationPrice":"0",
                "isolatedMargin":"0",
                "notional":"1052.95000559",
                "marginAsset":"USDT",
                "isolatedWallet":"0",
                "initialMargin":"42.11800022",
                "maintMargin":"4.21180002",
                "positionInitialMargin":"42.11800022",
                "openOrderInitialMargin":"0",
                "adl":"0",
                "bidNotional":"0",
                "askNotional":"0",
                "updateTime":"1727469603200"
            },
            "id":"None",
            "symbol":"BTC/USDT:USDT",
            "contracts":0.016, <--- note, if this value is 0, the position is close
            "contractSize":1.0,
            "unrealizedPnl":9.54900559,
            "leverage":"None",
            "liquidationPrice":"None",
            "collateral":1043.401,
            "notional":1052.95000559,
            "markPrice":65809.37534989,
            "entryPrice":65212.5625,
            "timestamp":1727469603200,
            "initialMargin":42.11800022,
            "initialMarginPercentage":0.03999999,
            "maintenanceMargin":4.21180002236,
            "maintenanceMarginPercentage":0.004,
            "marginRatio":0.004,
            "datetime":"2024-09-27T20:40:03.200Z",
            "marginMode":"cross",
            "marginType":"cross",
            "side":"long",
            "hedged":false,
            "percentage":22.67,
            "stopLossPrice":"None",
            "takeProfitPrice":"None"
        }
        '''

    async def launch(self):
        await self.getPositions()

    async def getPositions(self):
        while True:
            try:
                positions = await clientPro.watch_positions(symbols=[self.symbol])
                for position in positions:
                    if(position["symbol"].split(":")[0] == self.symbol):
                        self.position = position
            except Exception as e:
                print(e)

    def isPositionClose(self):
        try:
            if(self.position["contracts"] == 0):
                return True
            else:
                return False
        except:
            return False

    def getPositionValue(self):
        '''Value in symbol size (not in USDT)'''
        try:
            return self.position["contracts"]
        except:
            return False
        
    def getPositionSide(self):
        '''Long or short'''
        try:
            return self.position["side"]
        except:
            return False        

'''
async def main():
    positions = Positions("BTC/USDT")
    await positions.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''