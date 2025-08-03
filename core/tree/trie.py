"""
Trie operations
"""
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def trie_insert(root, word):
    print(f"[Trie] Inserting '{word}'...")
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True
    return root

def trie_search(root, word):
    print(f"[Trie] Searching for '{word}'...")
    node = root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_end

def trie_prefix_match(root, prefix):
    print(f"[Trie] Prefix matching for '{prefix}'...")
    node = root
    for char in prefix:
        if char not in node.children:
            return []
        node = node.children[char]
    results = []
    def dfs(n, path):
        if n.is_end:
            results.append(prefix + path)
        for c, child in n.children.items():
            dfs(child, path + c)
    dfs(node, "")
    return results
