# ═══════════════════════════════════════════════
# 📅 Date      : 2026-03-13
# 🧩 Problem   : Two Sum
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Given an array of integers and a target, return indices of the two numbers that add up to target.
# ═══════════════════════════════════════════════

def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]

