import argparse
from datetime import datetime
from typing import Dict, Union
import asyncio

from futu import *

from siglab_py.exchanges.futubull import Futubull
from siglab_py.util.market_data_util import fetch_candles
from siglab_py.util.analytic_util import compute_candles_stats

end_date : datetime = datetime.today()
start_date : datetime = end_date - timedelta(days=365)

param : Dict = {
    'symbol' : None,
    'trdmarket' : TrdMarket.HK,
    'security_firm' : SecurityFirm.FUTUSECURITIES,
    'market' : Market.HK, 
    'security_type' : SecurityType.STOCK,
    'daemon' : {
        'host' : '127.0.0.1',
        'port' : 11111
    }
}

'''
If debugging from VSCode, launch.json:

    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python Debugger: Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "args" : [
                        "--symbol", "HK.00700",
                        "--market", "HK",
                        "--trdmarket", "HK",
                        "--security_firm", "FUTUSECURITIES",
                        "--security_type", "STOCK"
                    ],
                "env": {
                    "PYTHONPATH": "${workspaceFolder}"
                }
            }
        ]
    }
'''
def parse_args():
    parser = argparse.ArgumentParser() # type: ignore
    parser.add_argument("--symbol", help="symbol, example HK.00700", default=None)

    '''
    Enums here: 
    https://openapi.futunn.com/futu-api-doc/en/quote/quote.html#66
    https://openapi.futunn.com/futu-api-doc/en/trade/trade.html#9434
    '''
    parser.add_argument("--market", help="market: HK SH SZ US AU CA FX", default=Market.HK)
    parser.add_argument("--trdmarket", help="trdmarket: HK, HKCC, HKFUND, FUTURES, CN, CA, AU, JP, MY, SG, US, USFUND", default=TrdMarket.HK)
    parser.add_argument("--security_firm", help="security_firm: FUTUSECURITIES (HK), FUTUINC (US), FUTUSG (SG), FUTUAU (AU)", default=SecurityFirm.FUTUSECURITIES)
    parser.add_argument("--security_type", help="STOCK, BOND, ETF, FUTURE, WARRANT, IDX ... ", default=SecurityType.STOCK)

    args = parser.parse_args()
    param['symbol'] = args.symbol
    param['market'] = args.market
    param['trdmarket'] = args.trdmarket
    param['security_firm'] = args.security_firm

async def main():
    parse_args()

    exchange = Futubull(param)

    pd_candles: Union[pd.DataFrame, None] = fetch_candles(
            start_ts=int(start_date.timestamp()),
            end_ts=int(end_date.timestamp()),
            exchange=exchange,
            normalized_symbols=[ param['symbol'] ],
            candle_size='1d'
        )[param['symbol']]

    assert pd_candles is not None

    if pd_candles is not None:
        assert len(pd_candles) > 0, "No candles returned."
        expected_columns = {'exchange', 'symbol', 'timestamp_ms', 'open', 'high', 'low', 'close', 'volume', 'datetime_utc', 'datetime', 'year', 'month', 'day', 'hour', 'minute'}
        assert set(pd_candles.columns) >= expected_columns, "Missing expected columns."
        assert pd_candles['timestamp_ms'].notna().all(), "timestamp_ms column contains NaN values."
        assert pd_candles['timestamp_ms'].is_monotonic_increasing, "Timestamps are not in ascending order."

asyncio.run(main())
