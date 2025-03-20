import requests
import pandas as pd
from crypto_candle_fetcher.data_processing import DataProcessor

TIMEFRAMES = {
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "8h": "8h",
    "12h": "12h",
    "1d": "1d",
    "3d": "3d",
    "1w": "1w"
}

def fetch_candles(fetcher, pair: str, interval: str, period: int):
    """ Fetch candlestick data from Binance """
    
    processor = DataProcessor(time_unit="ms", debug=fetcher.Debug)
    base_url = "https://api.binance.com/api/v3/klines"
    
    # Retrieve time range from DataProcessor
    start_time, end_time = processor.get_time_range(period)
    
    params = {
        "symbol": pair,
        "interval": interval,
        "startTime": start_time * 1000,  # Convert seconds to milliseconds
        "endTime": end_time * 1000,  # Convert seconds to milliseconds
        "limit": 1000
    }
    
    candles = []
    
    while True:
        processor.log_message(f"🔄 Requesting data from {params['startTime']} to {params['endTime']}")

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            processor.log_message(f"❌ Error fetching data from Binance: {response.json()}")
            break
        
        data = response.json()
        if not data:
            processor.log_message("⚠️ Data retrieval complete. No more data available.")
            break
        
        processor.log_message(f"✅ Retrieved {len(data)} new candles")
        
        # Append new data
        candles.extend(data)
        
        # Update `startTime` to fetch more data
        params["startTime"] = data[-1][0] + 1  
        
        # If fewer than 1000 records were received, we have reached the end of the data
        if len(data) < 1000:
            processor.log_message("✅ All data has been retrieved.")
            break
    
    if not candles:
        processor.log_message("⚠️ No data received!")
        return None

    # Convert data to DataFrame
    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume",
                                        "close_time", "quote_asset_volume", "trades",
                                        "taker_buy_base", "taker_buy_quote", "ignore"])
    
    # Keep only essential columns
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    
    # Process data using `normalize_candle_df` function
    df = processor.normalize_candle_df(df)
    
    # Sort data by timestamp
    df = df.sort_values(by="timestamp")
    
    # Save data using `save_dataframe` function
    return processor.save_dataframe(df, "binance", pair, interval, fetcher.csv_save, fetcher.json_save)
