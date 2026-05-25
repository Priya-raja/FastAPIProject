"""Simple decorator examples."""

from collections.abc import Callable
from typing import Any


def fence(func: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap a callable with simple entry and exit logging."""

    def wrapper(*args, **kwargs):
        """Run the wrapped callable while printing fence messages."""
        print("Entering the fence...")
        result = func(*args, **kwargs)
        print("Exiting the fence...")
        return result

    return wrapper


@fence
def log(a: int, b: list[int]) -> None:
    """Print a sample log message for the provided values."""
    print("Logging... Value:", a, "List:", b)


if __name__ == "__main__":
    log(1, [2, 3, 4])
