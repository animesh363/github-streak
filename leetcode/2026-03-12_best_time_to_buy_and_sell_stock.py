# ═══════════════════════════════════════════════
# 📅 Date      : 2026-03-12
# 🧩 Problem   : Best Time to Buy and Sell Stock
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Given prices array, find the maximum profit from one buy and one sell.
# ═══════════════════════════════════════════════

def max_profit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

print(max_profit([7, 1, 5, 3, 6, 4]))  # 5
print(max_profit([7, 6, 4, 3, 1]))     # 0

