# ═══════════════════════════════════════════════
# 📅 Date      : 2026-03-11
# 🧩 Problem   : Maximum Subarray
# 💡 Difficulty: Medium
# ═══════════════════════════════════════════════
# 📝 Description:
#    Find the contiguous subarray with the largest sum. (Kadane's Algorithm)
# ═══════════════════════════════════════════════

def max_sub_array(nums: list[int]) -> int:
    max_sum = current = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        max_sum = max(max_sum, current)
    return max_sum

# Tests
print(max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
print(max_sub_array([1]))                                 # 1
print(max_sub_array([5, 4, -1, 7, 8]))                   # 23

