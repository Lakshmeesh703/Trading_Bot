import os
from typing import Optional

import typer
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderService, format_order_summary
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.logging_config import setup_logging


load_dotenv()
app = typer.Typer()


@app.command()
def order(
    symbol: Optional[str] = typer.Option(None, prompt=True),
    side: Optional[str] = typer.Option(None, prompt=True),
    order_type: Optional[str] = typer.Option(None, prompt=True),
    quantity: Optional[str] = typer.Option(None, prompt=True),
    price: Optional[str] = typer.Option(None, prompt=False),
    stop_price: Optional[str] = typer.Option(None, prompt=False),
    api_key: Optional[str] = typer.Option(None, help="API key or set BINANCE_API_KEY"),
    api_secret: Optional[str] = typer.Option(None, help="API secret or set BINANCE_API_SECRET"),
    dry_run: bool = typer.Option(True, help="Don't send requests to testnet; simulate responses"),
):
    """Place an order on Binance Futures Testnet. Prompts for missing values."""
    logger = setup_logging()
    api_key = api_key or os.getenv("BINANCE_API_KEY")
    api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        logger.warning("No API credentials provided; running in dry-run mode")
        dry_run = True

    try:
        s = validate_side(side)
        t = validate_order_type(order_type)
        q = validate_quantity(quantity)
        p = validate_price(price, t)
        sp = validate_stop_price(stop_price, t)
    except Exception as e:
        typer.secho(f"Invalid input: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    client = BinanceFuturesClient(api_key or "", api_secret or "", dry_run=dry_run)
    service = OrderService(client)

    typer.echo("Submitting order...")
    try:
        resp = service.place(symbol, s, t, q, p, sp)
        summary = format_order_summary(resp["request"], resp["response"])
        typer.echo(summary)
        typer.secho("Order completed (dry-run=%s)" % dry_run, fg=typer.colors.GREEN)
    except Exception as e:
        logger.exception("Order failed")
        typer.secho(f"Order failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
