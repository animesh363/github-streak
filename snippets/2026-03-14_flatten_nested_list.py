# ═══════════════════════════════════════════════
# 📅 Date   : 2026-03-14
# 🔧 Snippet : Flatten Nested List
# ═══════════════════════════════════════════════

def flatten(lst: list) -> list:
    """Recursively flattens arbitrarily nested lists."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, [4]], 5]]))    # [1, 2, 3, 4, 5]
print(flatten([[1, 2], [3, [4, 5]]]))    # [1, 2, 3, 4, 5]

