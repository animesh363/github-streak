# ═══════════════════════════════════════════════
# 📅 Date   : 2026-03-14
# 🔧 Snippet : Retry Decorator
# ═══════════════════════════════════════════════

import time
import functools

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Decorator that retries a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unstable_function(x):
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return f"Success: {x}"

print(unstable_function(42))

