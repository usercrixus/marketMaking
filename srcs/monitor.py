import asyncio
from typing import List
from account import Account
from strategy import Strategy
from market import Market
from symbol import SymbolData

class Monitor:
    _instance = None  # Class-level variable to store the singleton instance

    @staticmethod
    def get_instance(strategy : List[Strategy]):
        """Static access method to get the singleton instance."""
        if Monitor._instance is None:
            Monitor._instance = Monitor(strategy)
        return Monitor._instance

    def __init__(self, strategy : List[Strategy]):
        """Prevent direct instantiation of the singleton class."""
        if Monitor._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
        self.strategy = strategy
    
    async def launch(self):
        while True:
            await self.manageOrders()
            await asyncio.sleep(4)

    async def manageOrders(self):
        for strategy in self.strategy:
            for symbolData in strategy.symbolsData:
                if(strategy.shouldReducePosition(symbolData) and not symbolData.pressurize):
                    asyncio.create_task(self.reducePosition(strategy, symbolData))
                    symbolData.pressurize = True
                await self.passOrder(strategy, symbolData)


    async def passOrder(self, strategy:Strategy, symbolData:SymbolData):
        ajustAsk, ajustBid = strategy.shouldAdjustOrders(symbolData)
        ask_price, bid_price = strategy.getPrices(symbolData)
        sell_quantity, bid_quantity = strategy.getPosition(symbolData)
        isSellValidated = True
        isBuyValidated = True
        if(ajustBid and (symbolData.pressurize == False or symbolData.position.getPositionSide() == "long")):
            createOrder = True
            for order in symbolData.orders.orders:
                if(order["side"] == "sell"):
                    isSellValidated = await Market.get_instance().modifyOrder(ask_price, sell_quantity, symbolData.symbol, "sell", order["id"])
                    createOrder = False
                    break
            if(createOrder):
                isSellValidated = await Market.get_instance().placeOrder(ask_price, sell_quantity, symbolData.symbol, "sell")
        if(ajustAsk and (symbolData.pressurize == False or symbolData.position.getPositionSide() == "short")):
            createOrder = True
            for order in symbolData.orders.orders:
                if(order["side"] == "buy"):
                    isBuyValidated = await Market.get_instance().modifyOrder(bid_price, bid_quantity, symbolData.symbol, "buy", order["id"])
                    createOrder = False
                    break
            if(createOrder):
                isBuyValidated = await Market.get_instance().placeOrder(bid_price, bid_quantity, symbolData.symbol, "buy")

        if(not isBuyValidated or not isSellValidated):
            await asyncio.sleep(1)
            await self.passOrder(strategy, symbolData)

    async def reducePosition(self, strategy:Strategy, symbolData:SymbolData):
        bid_price = symbolData.orderbook.bids[0][0]
        ask_price = symbolData.orderbook.asks[0][0]
        midPrice = (bid_price + ask_price) / 2
        sell_quantity, bid_quantity = strategy.getPosition(symbolData)
        while(symbolData.position.getPositionValue() * midPrice > 33/100 * Account.get_instance().maximumPosition / 2):
            if(symbolData.position.position and not symbolData.position.isPositionClose()):
                if symbolData.position.getPositionSide() == "long":
                    for order in symbolData.orders.orders:
                        if(order["side"] == "buy"):
                            await Market.get_instance().cancelOrder(order["id"], symbolData.symbol)
                    await Market.get_instance().directOrder(sell_quantity / 10, symbolData.symbol, "sell")
                else:
                    for order in symbolData.orders.orders:
                        if(order["side"] == "sell"):
                            await Market.get_instance().cancelOrder(order["id"], symbolData.symbol)
                    await Market.get_instance().directOrder(bid_quantity / 10, symbolData.symbol, "buy")
            await asyncio.sleep(4)
        symbolData.pressurize = False