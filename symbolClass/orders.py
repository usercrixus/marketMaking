import sys
import os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import clientPro, client

class Orders:

    orders = []

    def __init__(self, symbol):
        self.symbol = symbol
        self.orders = []
        '''
        example :
        [
            {
                "info":{
                    "s":"BTCUSDT",
                    "c":"web_SCWrX3v4eeDzhfLToV8S",
                    "S":"BUY",
                    "o":"LIMIT",
                    "f":"GTC",
                    "q":"0.002",
                    "p":"61000",
                    "ap":"0",
                    "sp":"0",
                    "x":"NEW",
                    "X":"NEW",
                    "i":4060033429,
                    "l":"0",
                    "z":"0",
                    "L":"0",
                    "n":"0",
                    "N":"USDT",
                    "T":1727471153739,
                    "t":0,
                    "b":"122",
                    "a":"276.00040",
                    "m":false,
                    "R":false,
                    "wt":"CONTRACT_PRICE",
                    "ot":"LIMIT",
                    "ps":"BOTH",
                    "cp":false,
                    "rp":"0",
                    "pP":false,
                    "si":0,
                    "ss":0,
                    "V":"NONE",
                    "pm":"NONE",
                    "gtd":0
                },
                "symbol":"BTC/USDT:USDT",
                "id":"4060033429",
                "clientOrderId":"web_SCWrX3v4eeDzhfLToV8S",
                "timestamp":1727471153739,
                "datetime":"2024-09-27T21:05:53.739Z",
                "lastTradeTimestamp":"None",
                "lastUpdateTimestamp":1727471153739,
                "type":"limit",
                "timeInForce":"GTC",
                "postOnly":false,
                "reduceOnly":false,
                "side":"buy",
                "price":61000.0,
                "stopPrice":0.0,
                "triggerPrice":0.0,
                "amount":0.002,
                "cost":0.0,
                "average":"None",
                "filled":0.0,
                "remaining":0.002,
                "status":"open",
                "fee":"None",
                "trades":[
                    
                ],
                "fees":[
                    
                ],
                "takeProfitPrice":"None",
                "stopLossPrice":"None"
            }
        ]
        '''

    async def launch(self):
        await self.initOrders()
        await self.getOrders()

    async def initOrders(self):
        orders = await client.fetch_orders(self.symbol)
        for order in orders:
            if(order["status"] == "open"):
                self.orders.append(order)

    async def getOrders(self):
        while True:
            try:
                orders = await clientPro.watch_orders(symbol=None, since=None, limit=None, params={})
                for order in orders:
                    if(order["status"] == "open" and order["symbol"].split(":")[0] == self.symbol):
                        isPush = True
                        for selfOrder in self.orders:
                            if(selfOrder["id"] == order["id"]):
                                self.orders.remove(selfOrder)
                                self.orders.append(order)
                                isPush = False
                                break
                        if(isPush):
                            self.orders.append(order)
                    else:
                        for selfOrder in self.orders:
                            if(selfOrder["id"] == order["id"]):
                                self.orders.remove(selfOrder)
            except Exception as e:
                print(e)

'''
async def main():
    orders = Orders("BTC/USDT")
    await orders.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''