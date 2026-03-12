# ═══════════════════════════════════════════════
# 📅 Date   : 2026-03-12
# 🔧 Snippet : Memoization Decorator
# ═══════════════════════════════════════════════

from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """Fibonacci with memoization — O(n) time."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

