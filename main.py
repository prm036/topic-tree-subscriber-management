"""
Topic-Tree Subscriber Management
--------------------------------

This module implements a hierarchical topic tree (trie) for managing subscribers.

Features:
1. TreeNode structure
2. Add subscriber for a topic
3. Get subscribers (exact match, '*' wildcard, '**' multi-level wildcard)
4. Return subscribers for a topic and all subtopics
5. Remove/unsubscribe subscriber
6. Support multi-topic subscription

Author: Your Name
Date: YYYY-MM-DD
"""

# -----------------------------
# 1. TreeNode Structure
# -----------------------------
class TreeNode:
    def __init__(self):
        self.children: dict[str, "TreeNode"] = {}
        self.subscribers: set = set()


# -----------------------------
# 2. Add Subscriber Function
# -----------------------------
def add_subscriber(root: TreeNode, subscriber_id: str, topic_list: list[str]):
    """
    Add a subscriber to a given topic path.
    """
    node = root
    for topic in topic_list:
        if topic not in node.children:
            node.children[topic] = TreeNode()
        node = node.children[topic]
    node.subscribers.add(subscriber_id)


# -----------------------------
# 3. Remove / Unsubscribe Function
# -----------------------------
def remove_subscriber(root: TreeNode, subscriber_id: str, topic_list: list[str]):
    """
    Remove a subscriber from a specific topic path.
    """
    node = root
    for topic in topic_list:
        if topic in node.children:
            node = node.children[topic]
        else:
            return  # topic path doesn't exist
    node.subscribers.discard(subscriber_id)


# -----------------------------
# 4. Get Subscribers with Wildcards ('*' and '**')
# -----------------------------
def get_subscribers(root: TreeNode, topic_list: list[str]) -> set:
    """
    Return subscribers for a topic_list that may contain '*' or '**' wildcards.
    '*'  → matches exactly one level
    '**' → matches zero or more levels
    """
    if not topic_list:
        return root.subscribers

    head, tail = topic_list[0], topic_list[1:]
    subscribers = set()

    if head == "*":
        for child in root.children.values():
            subscribers |= get_subscribers(child, tail)
        return subscribers

    if head == "**":
        # Option A: match zero levels
        subscribers |= get_subscribers(root, tail)
        # Option B: match one or more levels
        for child in root.children.values():
            subscribers |= get_subscribers(child, topic_list)
        return subscribers

    # Exact match
    if head in root.children:
        return get_subscribers(root.children[head], tail)

    return set()


# -----------------------------
# 5. Get Subscribers for Topic AND All Subtopics
# -----------------------------
def get_subscribers_recursive(root: TreeNode) -> set:
    """
    Returns all subscribers under this node, including all descendants.
    """
    subscribers = set(root.subscribers)
    for child in root.children.values():
        subscribers |= get_subscribers_recursive(child)
    return subscribers


# -----------------------------
# 6. Multi-Topic Subscription Helper
# -----------------------------
def add_subscriber_multi(root: TreeNode, subscriber_id: str, topics: list[list[str]]):
    """
    Add a subscriber to multiple topics at once.
    """
    for topic_list in topics:
        add_subscriber(root, subscriber_id, topic_list)


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    root = TreeNode()

    # Add subscribers
    add_subscriber(root, "sub1", ["nytimes", "us", "editorial"])
    add_subscriber(root, "sub2", ["washington", "us", "sports"])
    add_subscriber(root, "sub3", ["nytimes", "india", "politics"])
    add_subscriber_multi(root, "sub4", [["nytimes", "us", "sports"], ["washington", "us", "politics"]])

    # Get exact subscribers
    print("Exact subscribers:")
    print(get_subscribers(root, ["nytimes", "us", "editorial"]))  # sub1

    # Get wildcard subscribers
    print("Wildcard '*' subscribers:")
    print(get_subscribers(root, ["*", "us", "editorial"]))        # sub1
    print("Wildcard '**' subscribers:")
    print(get_subscribers(root, ["nytimes", "**"]))               # sub1, sub3, sub4

    # Get subscribers for all subtopics
    print("All subtopic subscribers under 'nytimes':")
    ny_root = root.children.get("nytimes")
    if ny_root:
        print(get_subscribers_recursive(ny_root))                 # sub1, sub3, sub4

    # Remove subscriber
    remove_subscriber(root, "sub1", ["nytimes", "us", "editorial"])
    print("After removing sub1:")
    print(get_subscribers(root, ["nytimes", "us", "editorial"]))  # should be empty set
