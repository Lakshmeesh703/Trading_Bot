from typing import Any, Dict, Optional

from .client import BinanceFuturesClient
from .logging_config import setup_logging

logger = setup_logging()


def format_order_summary(request: Dict[str, Any], response: Dict[str, Any]) -> str:
    lines = []
    lines.append("Order request:")
    for k, v in request.items():
        lines.append(f"  {k}: {v}")

    lines.append("Order response:")
    keys = ["orderId", "status", "executedQty", "avgPrice", "stopPrice"]
    for k in keys:
        if k in response:
            lines.append(f"  {k}: {response.get(k)}")

    return "\n".join(lines)


class OrderService:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, stop_price: Optional[float] = None) -> Dict[str, Any]:
        req = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
        }
        try:
            resp = self.client.place_order(symbol, side, order_type, quantity, price, stop_price)
            logger.info("Order placed: %s", resp)
            return {"request": req, "response": resp}
        except Exception as e:
            logger.exception("Failed to place order: %s", e)
            raise
