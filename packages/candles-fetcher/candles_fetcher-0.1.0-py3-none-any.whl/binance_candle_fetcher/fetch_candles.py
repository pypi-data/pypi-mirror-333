import asyncio
import ccxt.async_support as ccxt
import pandas as pd
from datetime import datetime, timezone

async def fetch_binance_candles(symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch OHLCV candlestick data from Binance.

    Parameters:
    - symbol (str): Trading pair (e.g., 'BTC/USDT').
    - timeframe (str): Timeframe (e.g., '1m', '5m', '15m', '1h', '4h', '1d').
    - limit (int): Number of candles to fetch (default: 100).

    Returns:
    - pd.DataFrame: DataFrame containing timestamp, open, high, low, close, volume.
    """
    exchange = ccxt.binance({
        'enableRateLimit': True
    })
    
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        if not ohlcv:
            return pd.DataFrame(columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        
        df = pd.DataFrame(ohlcv, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit='ms', utc=True)
        
        return df
    finally:
        await exchange.close()

def get_binance_candles(symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
    """
    Wrapper function to fetch Binance candles synchronously.

    Parameters:
    - symbol (str): Trading pair (e.g., 'BTC/USDT').
    - timeframe (str): Timeframe (e.g., '1m', '5m', '15m', '1h', '4h', '1d').
    - limit (int): Number of candles to fetch (default: 100).

    Returns:
    - pd.DataFrame: DataFrame containing timestamp, open, high, low, close, volume.
    """
    return asyncio.run(fetch_binance_candles(symbol, timeframe, limit))
