"""
Configuration for Binance Dogecoin Futures Data Collection
"""

# Binance API Configuration
BINANCE_API_KEY = ""  # Optional: Not required for public market data
BINANCE_API_SECRET = ""  # Optional: Not required for public market data

# Trading Pair
SYMBOL = "DOGEUSDT"

# Data Collection Settings
INTERVAL = "1h"  # Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
START_DATE = "2021-01-01"  # Start date for historical data collection

# Output Settings
DATA_DIR = "data"
OUTPUT_FORMAT = "csv"  # csv or json
