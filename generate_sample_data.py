#!/usr/bin/env python3
"""
Generate sample Dogecoin futures data for demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Generate realistic sample DOGEUSDT futures data"""

    # Generate timestamps for hourly data (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    timestamps = pd.date_range(start=start_date, end=end_date, freq='1H')

    # Generate realistic price data starting around $0.08
    base_price = 0.08
    num_points = len(timestamps)

    # Random walk with trend
    np.random.seed(42)
    price_changes = np.random.normal(0, 0.002, num_points)
    closes = base_price + np.cumsum(price_changes)
    closes = np.maximum(closes, 0.05)  # Minimum price

    # Generate OHLC from close prices
    opens = closes + np.random.normal(0, 0.0005, num_points)
    highs = np.maximum(opens, closes) + np.abs(np.random.normal(0, 0.001, num_points))
    lows = np.minimum(opens, closes) - np.abs(np.random.normal(0, 0.001, num_points))

    # Generate volume data
    volumes = np.random.uniform(5000000, 20000000, num_points)
    quote_volumes = volumes * closes

    # Generate trade data
    trades = np.random.randint(1000, 5000, num_points)
    taker_buy_base_volumes = volumes * np.random.uniform(0.4, 0.6, num_points)
    taker_buy_quote_volumes = taker_buy_base_volumes * closes

    # Create DataFrame
    df = pd.DataFrame({
        'open_time': timestamps,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes,
        'close_time': timestamps + timedelta(hours=1),
        'quote_volume': quote_volumes,
        'trades': trades,
        'taker_buy_base_volume': taker_buy_base_volumes,
        'taker_buy_quote_volume': taker_buy_quote_volumes
    })

    return df

if __name__ == "__main__":
    print("Generating sample DOGEUSDT futures data...")
    df = generate_sample_data()

    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Save to CSV
    filename = 'data/DOGEUSDT_1h_sample.csv'
    df.to_csv(filename, index=False)

    print(f"\nSample data saved to: {filename}")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['open_time'].min()} to {df['open_time'].max()}")
    print("\nFirst 5 records:")
    print(df.head())
    print("\nLast 5 records:")
    print(df.tail())
    print("\nPrice statistics:")
    print(df[['open', 'high', 'low', 'close', 'volume']].describe())
