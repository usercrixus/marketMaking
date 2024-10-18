from typing import List
from account import Account
from symbol import SymbolData

class Strategy():
    def __init__(self, symbolsData: List[SymbolData]):
        self.symbolsData = symbolsData

    def getPosition(self, symbolData:SymbolData):
        best_bid = symbolData.orderbook.bids[0][0]
        best_ask = symbolData.orderbook.asks[0][0]
        mid_price = (best_bid + best_ask) / 2
        quantity = self.calculateOptimalQuantity(mid_price)
        
        if symbolData.position.getPositionSide() == "long":
            sell_quantity = symbolData.position.getPositionValue()
            bid_quantity = quantity
        elif symbolData.position.getPositionSide() == "short":
            bid_quantity = symbolData.position.getPositionValue()
            sell_quantity = quantity
        else:
            bid_quantity = quantity
            sell_quantity = quantity

        if(sell_quantity < symbolData.min_order_size):
            sell_quantity = symbolData.min_order_size
        if(bid_quantity < symbolData.min_order_size):
            bid_quantity = symbolData.min_order_size

        return symbolData.adjustQuantityToPrecision(sell_quantity), symbolData.adjustQuantityToPrecision(bid_quantity)

    def getPrices(self, symbolData:SymbolData):
        bid_price = symbolData.orderbook.bids[0][0]
        ask_price = symbolData.orderbook.asks[0][0]
        midPrice = (bid_price + ask_price) / 2
        if(symbolData.position.position and not symbolData.position.isPositionClose()):
            if symbolData.position.getPositionSide() == "long":
                if(symbolData.position.position["entryPrice"] < bid_price):
                    bid_price = symbolData.position.position["entryPrice"]
                if(symbolData.position.getPositionValue() * midPrice < 33/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    percentPosition =  1 - (symbolData.position.getPositionValue() * midPrice / (Account.get_instance().maximumPosition / len(self.symbolsData)))
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - percentPosition))/100)) >= ask_price):
                        ask_price = symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - percentPosition))/100)
                elif(symbolData.position.getPositionValue() * midPrice > 66/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    if(symbolData.position.position["entryPrice"] * (1 - (0.5 / 100)) < bid_price):
                        bid_price = symbolData.position.position["entryPrice"] * (1 - (0.5 / 100))
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - 0.33))/100)) >= ask_price):
                        ask_price = symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - 0.33))/100)
                    else:
                        ask_price = symbolData.orderbook.asks[1][0] - symbolData.tick_size
                else:
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - 0.33))/100)) >= ask_price):
                        ask_price = symbolData.position.position["entryPrice"] * (1 + (0.15 * (1 - 0.33))/100)
                    else:
                        ask_price = symbolData.orderbook.asks[1][0] - symbolData.tick_size
            else:
                if(symbolData.position.position["entryPrice"] > ask_price):
                    ask_price = symbolData.position.position["entryPrice"]
                if(symbolData.position.getPositionValue() * midPrice < 33/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    percentPosition =  1 - (symbolData.position.getPositionValue() * midPrice / (Account.get_instance().maximumPosition / len(self.symbolsData)))
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - percentPosition))/100)) <= bid_price):
                        bid_price = symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - percentPosition))/100)
                elif(symbolData.position.getPositionValue() * midPrice > 66/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    if(symbolData.position.position["entryPrice"] * (1 + (0.5 / 100)) > ask_price):
                        ask_price = symbolData.position.position["entryPrice"] * (1 + (0.5 / 100))
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - 0.33))/100)) <= bid_price):
                        bid_price = symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - 0.33))/100)
                    else:
                        bid_price = symbolData.orderbook.bids[1][0] + symbolData.tick_size
                else:
                    if(symbolData.adjustPriceToTickSize(symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - 0.33))/100)) <= bid_price):
                        bid_price = symbolData.position.position["entryPrice"] * (1 - (0.15 * (1 - 0.33))/100)
                    else:
                        bid_price = symbolData.orderbook.bids[1][0] + symbolData.tick_size
                    
        return symbolData.adjustPriceToTickSize(ask_price), symbolData.adjustPriceToTickSize(bid_price)

    def shouldAdjustOrders(self, symbolData:SymbolData):
        ask_price, bid_price = self.getPrices(symbolData)
        sell_quantity, bid_quantity = self.getPosition(symbolData)
        ajustAsk = True
        ajustBid = True
        
        for order in symbolData.orders.orders:
            if(order["side"] == "buy"):
                if(order["price"] == bid_price and order["amount"] == bid_quantity):
                    ajustAsk = False
            elif(order["side"] == "sell"):
                if(order["price"] == ask_price and order["amount"] == sell_quantity):
                    ajustBid = False

        return ajustAsk, ajustBid
    
    def shouldReducePosition(self, symbolData:SymbolData):
        bid_price = symbolData.orderbook.bids[0][0]
        ask_price = symbolData.orderbook.asks[0][0]
        midPrice = (bid_price + ask_price) / 2
        if(symbolData.position.position and not symbolData.position.isPositionClose()):
            if symbolData.position.getPositionSide() == "long":
                if(symbolData.position.getPositionValue() * midPrice > 90/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    return True
            else:
                if(symbolData.position.getPositionValue() * midPrice > 90/100 * Account.get_instance().maximumPosition / len(self.symbolsData)):
                    return True
        return False

    def calculateOptimalQuantity(self, mid_price):
        total_portfolio_value_usdt = Account.get_instance().totalMarginBalance
        bet_size_usdt = 0.50 * total_portfolio_value_usdt
        quantity_to_bet = bet_size_usdt / mid_price
        return quantity_to_bet