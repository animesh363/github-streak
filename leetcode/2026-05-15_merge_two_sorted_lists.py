# ═══════════════════════════════════════════════
# 📅 Date      : 2026-05-15
# 🧩 Problem   : Merge Two Sorted Lists
# 💡 Difficulty: Easy
# ═══════════════════════════════════════════════
# 📝 Merge two sorted linked lists and return the sorted merged list.
# ═══════════════════════════════════════════════

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(l1, l2):
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

