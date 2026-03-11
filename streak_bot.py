import os
import random
import subprocess
import datetime
import json
from pathlib import Path

# ══════════════════════════════════════════════════════════
#  CONFIG  — these are auto-set by setup.bat
#  You can also edit manually if needed
# ══════════════════════════════════════════════════════════
REPO_PATH   = r"D:\CrazyProjects\GitStreakBot\github-streak"
GITHUB_REPO = "https://github.com/animesh363/github-streak.git"  # replaced by setup.bat
USE_AI      = True    # set True + add API key to .env to use Claude AI
API_KEY     = ""       # leave blank — loaded from .env automatically
# ══════════════════════════════════════════════════════════


# ── Load .env file if it exists ───────────────────────────
def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

def get_api_key():
    return API_KEY or os.environ.get("ANTHROPIC_API_KEY", "")


# ── Built-in LeetCode problems (used when AI is off) ─────
LEETCODE_TEMPLATES = [
    {
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an array of integers and a target, return indices of the two numbers that add up to target.",
        "solution": '''def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Tests
print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]
'''
    },
    {
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "description": "Given a string with '(', ')', '{', '}', '[', ']' — determine if it is valid.",
        "solution": '''def is_valid(s: str) -> bool:
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

# Tests
print(is_valid("()[]{}"))   # True
print(is_valid("(]"))       # False
print(is_valid("([)]"))     # False
print(is_valid("{[]}"))     # True
'''
    },
    {
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "description": "Find the contiguous subarray with the largest sum. (Kadane's Algorithm)",
        "solution": '''def max_sub_array(nums: list[int]) -> int:
    max_sum = current = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        max_sum = max(max_sum, current)
    return max_sum

# Tests
print(max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
print(max_sub_array([1]))                                 # 1
print(max_sub_array([5, 4, -1, 7, 8]))                   # 23
'''
    },
    {
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "description": "You can climb 1 or 2 steps at a time. How many ways to reach the top of n stairs?",
        "solution": '''def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# Tests
for i in range(1, 8):
    print(f"n={i}: {climb_stairs(i)} ways")
'''
    },
    {
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "description": "Reverse a singly linked list iteratively.",
        "solution": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Helper functions
def build(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

print(to_list(reverse_list(build([1, 2, 3, 4, 5]))))  # [5, 4, 3, 2, 1]
print(to_list(reverse_list(build([1, 2]))))            # [2, 1]
'''
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "description": "Given prices array, find the maximum profit from one buy and one sell.",
        "solution": '''def max_profit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

# Tests
print(max_profit([7, 1, 5, 3, 6, 4]))  # 5
print(max_profit([7, 6, 4, 3, 1]))     # 0
print(max_profit([1, 2]))              # 1
'''
    },
    {
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "description": "Given an integer array, return True if any value appears at least twice.",
        "solution": '''def contains_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))

# Alternative O(n) with early exit
def contains_duplicate_v2(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Tests
print(contains_duplicate([1, 2, 3, 1]))       # True
print(contains_duplicate([1, 2, 3, 4]))       # False
print(contains_duplicate([1, 1, 1, 3, 3, 4])) # True
'''
    },
    {
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "description": "Merge two sorted linked lists and return the sorted merged list.",
        "solution": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next

def build(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

l1 = build([1, 2, 4])
l2 = build([1, 3, 4])
print(to_list(merge_two_lists(l1, l2)))  # [1, 1, 2, 3, 4, 4]
'''
    },
]

# ── Built-in Snippets (used when AI is off) ───────────────
SNIPPET_TEMPLATES = [
    {
        "title": "Binary Search",
        "code": '''def binary_search(arr: list, target) -> int:
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
'''
    },
    {
        "title": "Memoization Decorator",
        "code": '''from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """Fibonacci with memoization — O(n) time, O(n) space."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
'''
    },
    {
        "title": "Flatten Nested List",
        "code": '''def flatten(lst: list) -> list:
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
'''
    },
    {
        "title": "Rate Limiter",
        "code": '''import time
from collections import deque

class RateLimiter:
    """Sliding window rate limiter — allows max_calls per window_seconds."""
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
'''
    },
    {
        "title": "LRU Cache from Scratch",
        "code": '''from collections import OrderedDict

class LRUCache:
    """Least Recently Used cache with O(1) get and put."""
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)

cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # 1
cache.put(3, 3)       # evicts key 2
print(cache.get(2))   # -1
'''
    },
    {
        "title": "Retry Decorator",
        "code": '''import time
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
    return f"Success with {x}"

print(unstable_function(42))
'''
    },
]


def generate_with_ai(content_type: str) -> dict:
    """Call Claude API to generate fresh unique content."""
    try:
        import urllib.request
        key = get_api_key()
        if not key:
            return None

        today = datetime.date.today().strftime("%B %d, %Y")

        if content_type == "leetcode":
            prompt = f"""Generate a unique LeetCode-style coding problem for {today}.
Return ONLY valid JSON (no markdown, no backticks) in this exact format:
{{
  "title": "Problem Name",
  "difficulty": "Easy|Medium|Hard",
  "description": "Problem description in 1-2 sentences.",
  "solution": "complete working Python solution with comments and test cases"
}}"""
        else:
            prompt = f"""Generate a useful Python utility snippet for {today}.
Return ONLY valid JSON (no markdown, no backticks) in this exact format:
{{
  "title": "Snippet Title",
  "code": "complete working Python code with comments and examples"
}}"""

        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            text = data["content"][0]["text"].strip()
            return json.loads(text)

    except Exception as e:
        print(f"[AI] Error: {e} — falling back to templates.")
        return None


def build_leetcode_file(problem: dict, date_str: str) -> tuple:
    safe_title = problem["title"].replace(" ", "_").lower()
    filename = f"leetcode/{date_str}_{safe_title}.py"
    content = f'''# ═══════════════════════════════════════════════
# 📅 Date      : {date_str}
# 🧩 Problem   : {problem["title"]}
# 💡 Difficulty: {problem["difficulty"]}
# ═══════════════════════════════════════════════
# 📝 Description:
#    {problem["description"]}
# ═══════════════════════════════════════════════

{problem["solution"]}
'''
    return filename, content


def build_snippet_file(snippet: dict, date_str: str) -> tuple:
    safe_title = snippet["title"].replace(" ", "_").lower()
    filename = f"snippets/{date_str}_{safe_title}.py"
    content = f'''# ═══════════════════════════════════════════════
# 📅 Date   : {date_str}
# 🔧 Snippet : {snippet["title"]}
# ═══════════════════════════════════════════════

{snippet["code"]}
'''
    return filename, content


def write_file(repo: Path, rel_path: str, content: str):
    full = repo / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    print(f"[FILE] Written → {rel_path}")



def git(repo: Path, *args):
    result = subprocess.run(
        ["git"] + list(args),
        cwd=str(repo),
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout.strip()


def run():
    repo = Path(REPO_PATH)

    if not repo.exists():
        print(f"[ERROR] Repo not found: {repo}")
        print("Make sure you ran setup.bat first!")
        return

    date_str     = datetime.date.today().strftime("%Y-%m-%d")
    content_type = random.choice(["leetcode", "snippet"])

    if content_type == "leetcode":
        problem = (generate_with_ai("leetcode") if USE_AI else None) or random.choice(LEETCODE_TEMPLATES)
        fname, fcontent = build_leetcode_file(problem, date_str)
        write_file(repo, fname, fcontent)
        commit_msg = f"feat: LeetCode — {problem['title']} [{problem.get('difficulty','?')}] {date_str}"
    else:
        snippet = (generate_with_ai("snippet") if USE_AI else None) or random.choice(SNIPPET_TEMPLATES)
        fname, fcontent = build_snippet_file(snippet, date_str)
        write_file(repo, fname, fcontent)
        commit_msg = f"feat: snippet — {snippet['title']} {date_str}"

    try:
        print("[GIT] Staging …")
        git(repo, "add", ".")
        print(f"[GIT] Committing: {commit_msg}")
        git(repo, "commit", "-m", commit_msg)
        print("[GIT] Pushing to GitHub …")
        git(repo, "push", "origin", "main")
        print(f"\n✅  Streak saved! → {fname}")
    except RuntimeError as e:
        print(f"\n[GIT ERROR] {e}")


if __name__ == "__main__":
    run()
