from client import client, clientPro

class Market:
    _instance = None  # Class-level variable to store the singleton instance

    @staticmethod
    def get_instance():
        """Static access method to get the singleton instance."""
        if Market._instance is None:
            Market._instance = Market()
        return Market._instance

    def __init__(self):
        """Prevent direct instantiation of the singleton class."""
        if Market._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access the instance.")
    
    async def placeOrder(self, price, quantity, symbol, side):
        try:
            response = await client.create_order(
                symbol=symbol,
                type='limit',
                side=side,
                amount=quantity,
                price=price,
                params={'post_only': True}
            )
            print(f"Placed {side} order at price: {price} for quantity: {quantity}")
            return True
        except Exception as e:
            print(f"Error placing market-making orders: {e}")
            return False

    async def modifyOrder(self, price, quantity, symbol, side, orderId):
        try:
            response = await client.edit_order(
                id=orderId,
                symbol=symbol,
                type='limit',
                side=side,
                amount=quantity,
                price=price,
                params={'post_only': True}
            )
            print(f"Modifying {side} order: New price: {price}, New quantity: {quantity}")
            return True
        except Exception as e:
            print(f"Error modifying orders: {e}")
            return False

    async def directOrder(self, quantity, symbol, side):
        try:
            response = await client.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=quantity,
            )
            print(f"{side} quantity: {quantity}")
            return True
        except Exception as e:
            print(f"Error placing direct orders: {e}")
            return False
        
    async def cancelOrder(self, id, symbol):
        try:
            response = await client.cancel_order(
                id=id,
                symbol=symbol
            )
            print(f"order {id} canceled")
            return True
        except Exception as e:
            print(f"Error canceling order {id}: {e}")
            return False