# symbol_data.py

from client import client
import asyncio

from symbolClass.ohlcv import OHLCV
from symbolClass.orderBook import Orderbook
from symbolClass.orders import Orders
from symbolClass.positions import Positions
from symbolClass.trades import Trades
from decimal import Decimal, ROUND_HALF_UP

class SymbolData:
    def __init__(self, symbol:str):
        self.symbol = symbol
        self.ohlcv = OHLCV(symbol)
        self.orderbook = Orderbook(symbol)
        self.orders = Orders(symbol)
        self.position = Positions(symbol)
        self.trades = Trades(symbol)
        self.pressurize = False

    async def launch(self):
        await client.load_markets()
        market = client.market(self.symbol)
        self.tick_size = float(market['precision']['price'])
        self.min_order_size = float(market['limits']['amount']['min'])
        self.quantity_precision = float(market['precision']['amount'])
        self.min_notional = float(market['limits']['cost']['min'])

        ohlcv = asyncio.create_task(self.ohlcv.launch())
        orderbook = asyncio.create_task(self.orderbook.launch())
        orders = asyncio.create_task(self.orders.launch())
        position = asyncio.create_task(self.position.launch())
        trades = asyncio.create_task(self.trades.launch())
        await asyncio.gather(ohlcv, orderbook, orders, position, trades)

    def adjustPriceToTickSize(self, price):
        """Adjust the price to the nearest tick size with higher precision."""
        tick_size = Decimal(str(self.tick_size))
        price = Decimal(str(price))
        return float((price / tick_size).quantize(1, rounding=ROUND_HALF_UP) * tick_size)

    def adjustQuantityToPrecision(self, quantity):
        """Adjust the quantity to the correct precision."""
        quantity_prec = Decimal(str(self.quantity_precision))
        quantity = Decimal(str(quantity))
        return float((quantity / quantity_prec).quantize(1, rounding=ROUND_HALF_UP) * quantity_prec)

'''
async def main():
    symbolData = SymbolData('BTC/USDT')
    await symbolData.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''