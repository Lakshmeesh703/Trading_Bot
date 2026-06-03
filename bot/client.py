import hashlib
import hmac
import time
from typing import Any, Dict, Optional

import requests

from .logging_config import setup_logging

logger = setup_logging()


class BinanceFuturesClient:
    """Minimal Binance Futures (USDT-M) REST client for testnet.

    Uses HMAC SHA256 signatures for private endpoints.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com", dry_run: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.dry_run = dry_run

    def _sign(self, data: str) -> str:
        return hmac.new(self.api_secret, data.encode(), hashlib.sha256).hexdigest()

    def _post(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        params["timestamp"] = int(time.time() * 1000)
        query = "&".join(f"{k}={params[k]}" for k in sorted(params))
        signature = self._sign(query)
        qs = f"{query}&signature={signature}"
        logger.info("POST %s?%s", url, query)
        if self.dry_run:
            # Simulate a successful response
            import random

            fake = {
                "orderId": random.randint(10000000, 99999999),
                "symbol": params.get("symbol"),
                "status": "NEW",
                "executedQty": str(params.get("quantity", 0)) if params.get("type") == "MARKET" else "0",
                "avgPrice": str(params.get("price")) if params.get("price") else "0",
            }
            logger.info("Dry-run response %s", fake)
            return fake
        try:
            r = self.session.post(url, params=qs, timeout=10)
            logger.info("Response [%s] %s", r.status_code, r.text)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logger.exception("Network/API error while POSTing to %s", url)
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, stop_price: Optional[float] = None) -> Dict[str, Any]:
        path = "/fapi/v1/order"
        params: Dict[str, Any] = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            # map internal types to Binance API types
            "type": ("STOP" if order_type.upper() == "STOP_LIMIT" else order_type.upper()),
            "quantity": quantity,
        }
        t = order_type.upper()
        if t == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        elif t == "STOP_LIMIT":
            # For simplicity map STOP_LIMIT -> type=STOP with stopPrice + price
            params["stopPrice"] = stop_price
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._post(path, params)
