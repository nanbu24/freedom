#!/usr/bin/env python3
"""
Binance Dogecoin Futures Data Collection Script

This script collects historical kline/candlestick data for DOGEUSDT perpetual futures
from Binance and saves it to CSV format.
"""

import os
import time
from datetime import datetime, timedelta
import pandas as pd
import requests
from typing import List, Dict, Any
import config


class BinanceFuturesCollector:
    """Collector for Binance Futures historical data"""

    BASE_URL = "https://fapi.binance.com"

    def __init__(self, symbol: str = config.SYMBOL):
        self.symbol = symbol
        self.session = requests.Session()
        # Set headers to avoid 403 errors
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })

    def _get_klines(self, interval: str, start_time: int, end_time: int = None, limit: int = 1500) -> List[List]:
        """
        Fetch klines/candlestick data from Binance Futures API

        Args:
            interval: Kline interval (1m, 5m, 1h, 1d, etc.)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds (optional)
            limit: Number of klines to fetch (max 1500)

        Returns:
            List of kline data
        """
        endpoint = f"{self.BASE_URL}/fapi/v1/klines"

        params = {
            "symbol": self.symbol,
            "interval": interval,
            "startTime": start_time,
            "limit": limit
        }

        if end_time:
            params["endTime"] = end_time

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching klines: {e}")
            return []

    def collect_historical_data(self, interval: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """
        Collect all historical kline data from start_date to end_date

        Args:
            interval: Kline interval
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD' (defaults to today)

        Returns:
            DataFrame with historical kline data
        """
        # Convert dates to milliseconds
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        start_time = int(start_dt.timestamp() * 1000)

        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_time = int(end_dt.timestamp() * 1000)
        else:
            end_time = int(datetime.now().timestamp() * 1000)

        all_klines = []
        current_time = start_time

        print(f"Collecting {self.symbol} {interval} data from {start_date} to {end_date or 'now'}...")

        while current_time < end_time:
            # Fetch klines (don't pass end_time to avoid API issues)
            klines = self._get_klines(interval, current_time)

            if not klines:
                break

            all_klines.extend(klines)

            # Update current_time to the last kline's close time + 1ms
            current_time = klines[-1][6] + 1

            print(f"Fetched {len(klines)} klines. Total: {len(all_klines)}. Last timestamp: {datetime.fromtimestamp(klines[-1][0]/1000)}")

            # Rate limiting - be nice to Binance API
            time.sleep(0.5)

            # If we got less than the limit, we've reached the end
            if len(klines) < 1500:
                break

        # Convert to DataFrame
        df = self._klines_to_dataframe(all_klines)

        print(f"Collection complete! Total records: {len(df)}")

        return df

    def _klines_to_dataframe(self, klines: List[List]) -> pd.DataFrame:
        """
        Convert klines data to pandas DataFrame

        Args:
            klines: List of kline data from Binance API

        Returns:
            DataFrame with proper column names and types
        """
        df = pd.DataFrame(klines, columns=[
            'open_time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_volume',
            'trades',
            'taker_buy_base_volume',
            'taker_buy_quote_volume',
            'ignore'
        ])

        # Convert timestamps to datetime
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

        # Convert numeric columns
        numeric_columns = ['open', 'high', 'low', 'close', 'volume',
                          'quote_volume', 'taker_buy_base_volume', 'taker_buy_quote_volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['trades'] = df['trades'].astype(int)

        # Drop the 'ignore' column
        df = df.drop('ignore', axis=1)

        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save DataFrame to CSV file

        Args:
            df: DataFrame to save
            filename: Output filename (optional)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.symbol}_{config.INTERVAL}_{timestamp}.csv"

        # Create data directory if it doesn't exist
        os.makedirs(config.DATA_DIR, exist_ok=True)

        filepath = os.path.join(config.DATA_DIR, filename)
        df.to_csv(filepath, index=False)

        print(f"Data saved to: {filepath}")

        return filepath


def main():
    """Main execution function"""
    print("=" * 60)
    print("Binance Dogecoin Futures Data Collection")
    print("=" * 60)
    print(f"Symbol: {config.SYMBOL}")
    print(f"Interval: {config.INTERVAL}")
    print(f"Start Date: {config.START_DATE}")
    print("=" * 60)

    # Create collector
    collector = BinanceFuturesCollector(symbol=config.SYMBOL)

    # Collect historical data
    df = collector.collect_historical_data(
        interval=config.INTERVAL,
        start_date=config.START_DATE
    )

    # Save to CSV
    filepath = collector.save_to_csv(df)

    # Display summary statistics
    print("\n" + "=" * 60)
    print("Data Summary")
    print("=" * 60)
    print(f"Total Records: {len(df)}")
    print(f"Date Range: {df['open_time'].min()} to {df['open_time'].max()}")
    print(f"\nFirst 5 records:")
    print(df.head())
    print(f"\nLast 5 records:")
    print(df.tail())
    print(f"\nPrice Statistics:")
    print(df[['open', 'high', 'low', 'close', 'volume']].describe())


if __name__ == "__main__":
    main()
