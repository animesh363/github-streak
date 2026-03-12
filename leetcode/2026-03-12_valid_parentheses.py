# ═══════════════════════════════════════════════
# 📅 Date      : 2026-03-12
# 🧩 Problem   : Valid Parentheses
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Given a string with brackets, determine if it is valid.
# ═══════════════════════════════════════════════

def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack

print(is_valid("()[]{}"))   # True
print(is_valid("(]"))       # False

