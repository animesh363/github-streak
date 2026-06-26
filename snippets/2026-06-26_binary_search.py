# ═══════════════════════════════════════════════
# 📅 Date   : 2026-06-26
# 🔧 Snippet : Binary Search
# ═══════════════════════════════════════════════

def binary_search(arr: list, target) -> int:
    """Returns index of target in sorted arr, -1 if not found. O(log n)"""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9, 11], 7))   # 3
print(binary_search([1, 3, 5, 7, 9, 11], 4))   # -1

