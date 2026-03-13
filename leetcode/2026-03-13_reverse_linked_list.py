# ═══════════════════════════════════════════════
# 📅 Date      : 2026-03-13
# 🧩 Problem   : Reverse Linked List
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Description:
#    Reverse a singly linked list iteratively.
# ═══════════════════════════════════════════════

class ListNode:
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

