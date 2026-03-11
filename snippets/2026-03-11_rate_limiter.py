# ═══════════════════════════════════════════════
# 📅 Date   : 2026-03-11
# 🔧 Snippet : Rate Limiter
# ═══════════════════════════════════════════════

import time
from collections import deque

class RateLimiter:
    """Sliding window rate limiter."""
    def __init__(self, max_calls: int, window_seconds: float):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = deque()

    def is_allowed(self) -> bool:
        now = time.time()
        while self.calls and now - self.calls[0] >= self.window:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

limiter = RateLimiter(max_calls=3, window_seconds=1)
for _ in range(5):
    print("Allowed:", limiter.is_allowed())
    time.sleep(0.1)

