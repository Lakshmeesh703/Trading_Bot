from typing import Optional


def validate_side(side: str) -> str:
    s = side.upper()
    if s not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.upper()
    if t not in ("MARKET", "LIMIT", "STOP_LIMIT"):
        raise ValueError("order type must be MARKET, LIMIT, or STOP_LIMIT")
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except Exception:
        raise ValueError("quantity must be a number")
    if q <= 0:
        raise ValueError("quantity must be > 0")
    return q


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("price is required for LIMIT orders")
        try:
            p = float(price)
        except Exception:
            raise ValueError("price must be a number")
        if p <= 0:
            raise ValueError("price must be > 0")
        return p
    return None


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "STOP_LIMIT":
        if stop_price is None:
            raise ValueError("stop_price is required for STOP_LIMIT orders")
        try:
            sp = float(stop_price)
        except Exception:
            raise ValueError("stop_price must be a number")
        if sp <= 0:
            raise ValueError("stop_price must be > 0")
        return sp
    return None
