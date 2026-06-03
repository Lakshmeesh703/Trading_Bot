# Trading Bot (Binance Futures Testnet)

This is a small Python application that can place MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

Setup

1. Register at Binance Futures Testnet and create API credentials: https://testnet.binancefuture.com
2. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

3. Provide credentials via environment variables or flags:

```bash
export BINANCE_API_KEY=your_key
export BINANCE_API_SECRET=your_secret
```

Usage examples

Place a MARKET buy order for BTCUSDT (example):

```bash
python3 cli.py BTCUSDT BUY MARKET 0.001 --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET
```

Place a LIMIT sell order:

```bash
python3 cli.py BTCUSDT SELL LIMIT 0.001 --price 30000 --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET
```

Notes / assumptions

- This project uses direct REST calls to the Binance Futures Testnet and implements HMAC SHA256 signing for private endpoints.
- The CLI validates basic inputs but does not query exchange symbol metadata (e.g., lot size/price precision). Use conservative quantities and prices.
- Logging is written to `trading_bot/logs/trading_bot.log`.

Files

- `bot/client.py`: Binance Futures client with signing and request logging
- `bot/orders.py`: OrderService wrapper and formatting
- `bot/validators.py`: Input validation helpers
- `cli.py`: CLI entrypoint
