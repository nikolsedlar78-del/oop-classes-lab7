"""Спільні функції перевірки вхідних даних (кидають ValueError)."""
import math


def require_str(value, field):
    """Повертає непорожній рядок без крайніх пробілів або кидає ValueError."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def require_number(value, field, *, minimum=None, positive=False):
    """Перевіряє, що value — скінченне число (не bool), з опційними межами."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number")
    if not math.isfinite(value):
        raise ValueError(f"{field} must be finite")
    if positive and value <= 0:
        raise ValueError(f"{field} must be positive")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return value


def require_int(value, field, *, minimum=None, maximum=None):
    """Перевіряє, що value — ціле (не bool) у межах [minimum, maximum]."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field} must be <= {maximum}")
    return value
