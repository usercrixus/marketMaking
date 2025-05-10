from typing import List
import math
from account import Account
from symbol import SymbolData

class Strategy:
    def __init__(self, symbolsData: List[SymbolData], max_adjust_offset_pct: float = 0.5, log_k: float = 9.0):
        self.symbolsData = symbolsData
        self.max_adjust_offset_pct = max_adjust_offset_pct
        self.log_k = log_k
    def getPosition(self, symbolData: SymbolData):
        best_bid = symbolData.orderbook.bids[0][0]
        best_ask = symbolData.orderbook.asks[0][0]
        mid_price = (best_bid + best_ask) / 2
        quantity = self.calculateOptimalQuantity(mid_price)

        side = symbolData.position.getPositionSide()
        if side == "long":
            sell_quantity = symbolData.position.getPositionValue()
            bid_quantity = quantity
        elif side == "short":
            bid_quantity = symbolData.position.getPositionValue()
            sell_quantity = quantity
        else:
            bid_quantity = quantity
            sell_quantity = quantity
        bid_quantity = max(bid_quantity, symbolData.min_order_size)
        sell_quantity = max(sell_quantity, symbolData.min_order_size)

        return (
            symbolData.adjustQuantityToPrecision(sell_quantity),
            symbolData.adjustQuantityToPrecision(bid_quantity)
        )

    def getPrices(self, symbolData: SymbolData):
        bid_price = symbolData.orderbook.bids[0][0]
        ask_price = symbolData.orderbook.asks[0][0]
        mid_price = (bid_price + ask_price) / 2
        if not (symbolData.position.position and not symbolData.position.isPositionClose()):
            return (
                symbolData.adjustPriceToTickSize(ask_price),
                symbolData.adjustPriceToTickSize(bid_price)
            )
        side = symbolData.position.getPositionSide()
        entry_price = symbolData.position.position["entryPrice"]
        pos_value = symbolData.position.getPositionValue()
        total_limit = Account.get_instance().maximumPosition / len(self.symbolsData)
        utilization = min(max((pos_value * mid_price) / total_limit, 0.0), 1.0)
        remaining = 1.0 - utilization
        weight = math.log1p(self.log_k * remaining) / math.log1p(self.log_k)
        offset_pct = self.max_adjust_offset_pct * weight
        if side == "long":
            bid_candidate = entry_price * (1 - offset_pct / 100)
            bid_price = min(bid_price, bid_candidate)
            ask_candidate = entry_price * (1 + offset_pct / 100)
            ask_price = max(ask_price, ask_candidate)
        else:
            ask_candidate = entry_price * (1 + offset_pct / 100)
            ask_price = max(ask_price, ask_candidate)
            bid_candidate = entry_price * (1 - offset_pct / 100)
            bid_price = min(bid_price, bid_candidate)

        return (
            symbolData.adjustPriceToTickSize(ask_price),
            symbolData.adjustPriceToTickSize(bid_price)
        )

    def shouldAdjustOrders(self, symbolData: SymbolData):
        ask_price, bid_price = self.getPrices(symbolData)
        sell_qty, bid_qty = self.getPosition(symbolData)
        adjust_ask, adjust_bid = True, True
        for order in symbolData.orders.orders:
            if order["side"] == "buy" and order["price"] == bid_price and order["amount"] == bid_qty:
                adjust_ask = False
            if order["side"] == "sell" and order["price"] == ask_price and order["amount"] == sell_qty:
                adjust_bid = False
        return adjust_ask, adjust_bid

    def shouldReducePosition(self, symbolData: SymbolData):
        mid_price = sum(o[0] for o in symbolData.orderbook.bids[:1] + symbolData.orderbook.asks[:1]) / 2
        pos = symbolData.position
        if pos.position and not pos.isPositionClose():
            utilization = (pos.getPositionValue() * mid_price) / (Account.get_instance().maximumPosition / len(self.symbolsData))
            return utilization > 0.9
        return False

    def calculateOptimalQuantity(self, mid_price: float) -> float:
        total_value = Account.get_instance().totalMarginBalance
        bet_size = 0.5 * total_value
        return bet_size / mid_price
