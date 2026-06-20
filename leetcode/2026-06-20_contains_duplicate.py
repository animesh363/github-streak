# ═══════════════════════════════════════════════
# 📅 Date      : 2026-06-20
# 🧩 Problem   : Contains Duplicate
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Return True if any value appears at least twice in the array.
# ═══════════════════════════════════════════════

def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

print(contains_duplicate([1, 2, 3, 1]))   # True
print(contains_duplicate([1, 2, 3, 4]))   # False

