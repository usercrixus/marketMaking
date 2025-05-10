from client import clientPro, client

class Account:
    _instance = None  # Class-level variable to store the singleton instance

    @staticmethod
    def get_instance():
        if Account._instance is None:
            Account._instance = Account()
        return Account._instance

    def __init__(self):
        if Account._instance is not None:
            raise Exception("This class is a singleton! Use `get_instance()` to access the instance.")
        self.totalWalletBalance = 0
        self.totalMarginBalance = 0
        self.totalCrossWalletBalance = 0
        self.availableBalance = 0
        self.leverage = 50 # Can't find the API call to get it
        self.maximumPosition =  3000000  # Can't find the API call to get it

    async def launch(self):
        await self.initBalance()
        await self.getBalance()

    async def initBalance(self):
        balance = await client.fetch_balance()
        self.totalWalletBalance = float(balance["info"]["totalWalletBalance"])
        self.totalMarginBalance = float(balance["info"]["totalMarginBalance"])
        self.totalCrossWalletBalance = float(balance["info"]["totalCrossWalletBalance"])
        self.availableBalance = float(balance["info"]["availableBalance"])

    async def getBalance(self):
        while True:
            try:
                balance = await clientPro.watch_balance()
                for asset in balance["info"]["a"]["B"]:
                    if(asset["a"] == "USDT"):
                        self.totalWalletBalance = float(asset["wb"])
                        self.totalCrossWalletBalance = float(asset["cw"])
                bufferTotalMarginBalance = 0.0
                for asset in balance["info"]["a"]["P"]:
                    bufferTotalMarginBalance += float(asset["up"])
                self.totalMarginBalance = self.totalWalletBalance + bufferTotalMarginBalance
                balance = await client.fetch_balance()
                self.availableBalance = float(balance["info"]["availableBalance"])
                print(f"Wallet Balance : {self.totalWalletBalance}, Margin Balance : {self.totalMarginBalance}, Available Balance : {self.availableBalance}")
            except Exception as e:
                print(e)

'''
async def main():
    btcusdt = SymbolData("BTC/USDT")
    account = Account.get_instance([btcusdt])
    await account.launch()    

if __name__ == '__main__':
    asyncio.run(main())
'''