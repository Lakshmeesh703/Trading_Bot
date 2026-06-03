import argparse
import os
import sys

from bot.client import BinanceFuturesClient
from bot.orders import OrderService, format_order_summary
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logging


def main(argv=None):
    logger = setup_logging()
    parser = argparse.ArgumentParser(description="Simple Binance Futures (Testnet) trading CLI")
    parser.add_argument("--api-key", help="Binance API key (or set BINANCE_API_KEY env var)")
    parser.add_argument("--api-secret", help="Binance API secret (or set BINANCE_API_SECRET env var)")
    parser.add_argument("symbol", help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("order_type", help="MARKET or LIMIT")
    parser.add_argument("quantity", help="Quantity to trade")
    parser.add_argument("--price", help="Price for LIMIT orders", default=None)

    args = parser.parse_args(argv)

    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        logger.error("API key and secret must be provided via flags or environment variables")
        print("Provide API credentials via --api-key/--api-secret or set BINANCE_API_KEY/BINANCE_API_SECRET")
        sys.exit(2)

    try:
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except Exception as e:
        logger.error("Validation error: %s", e)
        print(f"Invalid input: {e}")
        sys.exit(2)

    client = BinanceFuturesClient(api_key, api_secret, base_url="https://testnet.binancefuture.com")
    service = OrderService(client)

    print("Placing order...\n")
    try:
        result = service.place(args.symbol, side, order_type, quantity, price)
        summary = format_order_summary(result["request"], result["response"])
        print(summary)
        print("\nOrder placed successfully")
    except Exception as e:
        logger.error("Error placing order: %s", e)
        print("Order failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
