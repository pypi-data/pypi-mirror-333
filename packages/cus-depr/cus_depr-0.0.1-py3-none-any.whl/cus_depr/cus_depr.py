# cus_depr.py
import warnings
from functools import wraps

__all__ = ["deprecated", "uinstead"]

def deprecated(func):
    """Декоратор для пометки функций как устаревших."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"Function '{func.__name__}' is deprecated",
            category=DeprecationWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper


def uinstead(new_func: str):
    """Декоратор для пометки функции с предложением использования новой функции вместо старой."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"Function '{func.__name__}' is deprecated. Use '{new_func}' instead.",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
