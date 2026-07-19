# ═══════════════════════════════════════════════
# 📅 Date      : 2026-07-19
# 🧩 Problem   : Climbing Stairs
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 You can climb 1 or 2 steps. How many ways to reach top of n stairs?
# ═══════════════════════════════════════════════

def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

for i in range(1, 8):
    print(f"n={i}: {climb_stairs(i)} ways")

