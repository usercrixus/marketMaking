# main.py

import asyncio
from strategy import Strategy
from symbol import SymbolData
from account import Account
from strategy import Strategy
from monitor import Monitor

async def main():
    try:
        # Instantiate the SymbolData object for the trading symbol

        account = Account.get_instance()
        btcusdt = SymbolData("BTC/USDT")
        ethusdt = SymbolData("ETH/USDT")

        accountTask = asyncio.create_task(account.launch())
        btcusdtTask = asyncio.create_task(btcusdt.launch())
        ethusdtTask = asyncio.create_task(ethusdt.launch())

        strategy:Strategy = Strategy([ethusdt, btcusdt])

        await asyncio.sleep(10)

        monitorTask = asyncio.create_task(Monitor.get_instance([strategy]).launch())

        await asyncio.gather(accountTask, btcusdtTask, ethusdtTask, monitorTask)

    except Exception as e:
        print(f"Error running tasks: {e.with_traceback(e)}")

if __name__ == '__main__':
    asyncio.run(main())
