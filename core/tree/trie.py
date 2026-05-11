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

def trie_delete(root, word):
    """
    Deletes a word from the trie.
    Returns True if the word was found and deleted.
    """
    def _delete(node, word, depth):
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0
        
        char = word[depth]
        if char not in node.children:
            return False
        
        should_delete_child = _delete(node.children[char], word, depth + 1)
        
        if should_delete_child:
            del node.children[char]
            return not node.is_end and len(node.children) == 0
        
        return False

    _delete(root, word, 0)
    return root
