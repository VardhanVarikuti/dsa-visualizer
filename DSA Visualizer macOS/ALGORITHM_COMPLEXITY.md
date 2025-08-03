# DSA Visualizer - Algorithm Complexity Guide

This document provides detailed time and space complexity analysis for all algorithms implemented in the DSA Visualizer project.

---

## 📊 Graph Algorithms

### Pathfinding Algorithms

#### **Breadth-First Search (BFS)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Unweighted shortest path, level-by-level traversal
- **Notes**: 
  - Guarantees shortest path in unweighted graphs
  - Uses queue data structure
  - Visits all nodes at current level before moving to next

#### **Depth-First Search (DFS)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V) (worst case: O(V) for recursion stack)
- **Use Case**: Graph exploration, cycle detection, topological sort
- **Notes**:
  - Uses stack (recursion or explicit)
  - Explores as far as possible along each branch
  - Can be used for cycle detection

#### **Dijkstra's Algorithm**
- **Time Complexity**: O((V + E) log V) with binary heap
- **Space Complexity**: O(V)
- **Use Case**: Single-source shortest paths in weighted graphs
- **Notes**:
  - Requires non-negative edge weights
  - Uses priority queue (min-heap)
  - Optimal for dense graphs with binary heap

#### **A* Search**
- **Time Complexity**: O(E) in worst case, but typically much better
- **Space Complexity**: O(V)
- **Use Case**: Heuristic-based shortest path finding
- **Notes**:
  - Requires admissible heuristic function
  - Performance depends heavily on heuristic quality
  - Optimal when heuristic is perfect

#### **Bellman-Ford Algorithm**
- **Time Complexity**: O(VE)
- **Space Complexity**: O(V)
- **Use Case**: Single-source shortest paths with negative weights
- **Notes**:
  - Can detect negative cycles
  - Works with negative edge weights
  - Less efficient than Dijkstra for positive weights

#### **Floyd-Warshall Algorithm**
- **Time Complexity**: O(V³)
- **Space Complexity**: O(V²)
- **Use Case**: All-pairs shortest paths
- **Notes**:
  - Works with negative weights (no negative cycles)
  - Simple implementation
  - Good for dense graphs

#### **Johnson's Algorithm**
- **Time Complexity**: O(V² log V + VE)
- **Space Complexity**: O(V²)
- **Use Case**: All-pairs shortest paths in sparse graphs
- **Notes**:
  - Uses Bellman-Ford + Dijkstra
  - Better than Floyd-Warshall for sparse graphs
  - Handles negative weights

#### **SPFA (Shortest Path Faster Algorithm)**
- **Time Complexity**: O(VE) worst case, O(E) average case
- **Space Complexity**: O(V)
- **Use Case**: Single-source shortest paths with negative weights
- **Notes**:
  - Queue-based implementation
  - Can be faster than Bellman-Ford in practice
  - Detects negative cycles

### Minimum Spanning Tree Algorithms

#### **Prim's Algorithm**
- **Time Complexity**: O(E log V) with binary heap
- **Space Complexity**: O(V)
- **Use Case**: Minimum spanning tree in weighted graphs
- **Notes**:
  - Greedy algorithm
  - Works on connected graphs
  - Uses priority queue

#### **Kruskal's Algorithm**
- **Time Complexity**: O(E log E) = O(E log V)
- **Space Complexity**: O(V)
- **Use Case**: Minimum spanning tree in weighted graphs
- **Notes**:
  - Uses Union-Find data structure
  - Sorts edges by weight
  - Works on disconnected graphs

### Graph Analysis Algorithms

#### **Topological Sort (Kahn's Algorithm)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Dependency resolution, task scheduling
- **Notes**:
  - Only works on DAGs (Directed Acyclic Graphs)
  - Uses in-degree counting
  - Queue-based implementation

#### **Topological Sort + Relaxation**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Shortest paths in DAGs
- **Notes**:
  - Combines topological sort with edge relaxation
  - Optimal for DAG shortest paths
  - Linear time complexity

#### **Strongly Connected Components (SCC) - Tarjan's**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Finding connected subgraphs in directed graphs
- **Notes**:
  - Uses DFS with low-link values
  - Single DFS pass
  - Identifies all SCCs

#### **Cycle Detection (Directed)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Detecting cycles in directed graphs
- **Notes**:
  - Uses DFS with color coding
  - Three colors: white (unvisited), gray (visiting), black (visited)
  - Detects back edges

#### **Cycle Detection (Undirected)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Detecting cycles in undirected graphs
- **Notes**:
  - Uses DFS with parent tracking
  - Avoids revisiting parent
  - Detects back edges to non-parent

#### **Connected Components (Undirected)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Finding all connected groups
- **Notes**:
  - Uses DFS or BFS
  - Assigns component IDs
  - Counts number of components

#### **Articulation Points**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Finding critical nodes in undirected graphs
- **Notes**:
  - Uses DFS with discovery and low values
  - Identifies nodes whose removal disconnects graph
  - Important for network reliability

#### **Bridges**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Finding critical edges in undirected graphs
- **Notes**:
  - Uses DFS with discovery and low values
  - Identifies edges whose removal disconnects graph
  - Similar to articulation points

#### **Bipartite Check**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Checking if graph is bipartite
- **Notes**:
  - Uses BFS with color assignment
  - Two-coloring problem
  - Detects odd-length cycles

#### **Transitive Closure**
- **Time Complexity**: O(V³) with Floyd-Warshall approach
- **Space Complexity**: O(V²)
- **Use Case**: Finding all reachable pairs
- **Notes**:
  - Can use matrix multiplication
  - Warshall's algorithm
  - Boolean matrix operations

---

## 🌳 Tree Algorithms

### Binary Search Tree (BST)

#### **Insert Operation**
- **Time Complexity**: O(h) where h is height
  - **Best Case**: O(log n) for balanced tree
  - **Worst Case**: O(n) for skewed tree
- **Space Complexity**: O(h) for recursion stack
- **Notes**: Traverses from root to insertion point

#### **Delete Operation**
- **Time Complexity**: O(h) where h is height
  - **Best Case**: O(log n) for balanced tree
  - **Worst Case**: O(n) for skewed tree
- **Space Complexity**: O(h) for recursion stack
- **Notes**: Three cases: leaf, one child, two children

#### **Search Operation**
- **Time Complexity**: O(h) where h is height
  - **Best Case**: O(log n) for balanced tree
  - **Worst Case**: O(n) for skewed tree
- **Space Complexity**: O(h) for recursion stack
- **Notes**: Binary search in tree structure

#### **Traversals**
- **Inorder**: O(n) - visits all nodes
- **Preorder**: O(n) - visits all nodes
- **Postorder**: O(n) - visits all nodes
- **Space Complexity**: O(h) for recursion stack
- **Notes**: All traversals visit each node exactly once

#### **LCA (Lowest Common Ancestor)**
- **Time Complexity**: O(h) where h is height
- **Space Complexity**: O(h) for recursion stack
- **Notes**: Uses BST property for efficient search

### AVL Tree

#### **Insert Operation**
- **Time Complexity**: O(log n)
- **Space Complexity**: O(log n) for recursion stack
- **Notes**: 
  - Always maintains balance
  - May require rotations after insertion
  - Height is always O(log n)

#### **Delete Operation**
- **Time Complexity**: O(log n)
- **Space Complexity**: O(log n) for recursion stack
- **Notes**:
  - May require multiple rotations
  - Maintains balance property
  - Height remains O(log n)

#### **Search Operation**
- **Time Complexity**: O(log n)
- **Space Complexity**: O(log n) for recursion stack
- **Notes**: Same as BST but guaranteed O(log n)

#### **Rotation Operations**
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)
- **Notes**: Constant time operations for rebalancing

### Trie

#### **Insert Operation**
- **Time Complexity**: O(m) where m is word length
- **Space Complexity**: O(m)
- **Notes**: 
  - One character per level
  - Space depends on word length
  - No collisions like hash tables

#### **Search Operation**
- **Time Complexity**: O(m) where m is word length
- **Space Complexity**: O(1)
- **Notes**: Traverses exactly m levels

#### **Prefix Search**
- **Time Complexity**: O(m + k) where m is prefix length, k is number of matches
- **Space Complexity**: O(k) for storing results
- **Notes**: 
  - Finds all words with given prefix
  - DFS from prefix end

#### **Delete Operation**
- **Time Complexity**: O(m) where m is word length
- **Space Complexity**: O(m) for recursion stack
- **Notes**: May need to clean up unused nodes

### N-ary Tree

#### **BFS Traversal**
- **Time Complexity**: O(n) where n is number of nodes
- **Space Complexity**: O(w) where w is maximum width
- **Notes**: 
  - Uses queue
  - Space depends on tree width, not height

#### **DFS Traversal**
- **Time Complexity**: O(n) where n is number of nodes
- **Space Complexity**: O(h) where h is height
- **Notes**: 
  - Uses stack (recursion)
  - Space depends on tree height

---

## 🎯 Grid/Maze Algorithms

### **BFS (Grid)**
- **Time Complexity**: O(R × C) where R is rows, C is columns
- **Space Complexity**: O(R × C)
- **Notes**: 
  - Guarantees shortest path
  - Uses queue
  - Visits all reachable cells

### **DFS (Grid)**
- **Time Complexity**: O(R × C) where R is rows, C is columns
- **Space Complexity**: O(R × C) for visited array
- **Notes**: 
  - May not find shortest path
  - Uses stack (recursion)
  - Explores deep paths first

### **A* (Grid)**
- **Time Complexity**: O(R × C × log(R × C)) with binary heap
- **Space Complexity**: O(R × C)
- **Notes**: 
  - Uses heuristic function
  - Performance depends on heuristic quality
  - Priority queue implementation

### **Dijkstra (Grid)**
- **Time Complexity**: O(R × C × log(R × C)) with binary heap
- **Space Complexity**: O(R × C)
- **Notes**: 
  - For weighted grids
  - Similar to A* without heuristic
  - Priority queue implementation

### **Bidirectional BFS (Grid)**
- **Time Complexity**: O(R × C)
- **Space Complexity**: O(R × C)
- **Notes**: 
  - Searches from both start and end
  - Can be faster than unidirectional BFS
  - Meets in the middle

---

## 📈 Complexity Comparison Summary

### **Shortest Path Algorithms**
| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| BFS | O(V + E) | O(V) | Unweighted graphs |
| Dijkstra | O((V + E) log V) | O(V) | Positive weights |
| Bellman-Ford | O(VE) | O(V) | Negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All pairs |
| A* | O(E) | O(V) | Heuristic search |

### **Tree Operations**
| Operation | BST (avg) | BST (worst) | AVL | Trie |
|-----------|-----------|-------------|-----|------|
| Insert | O(log n) | O(n) | O(log n) | O(m) |
| Search | O(log n) | O(n) | O(log n) | O(m) |
| Delete | O(log n) | O(n) | O(log n) | O(m) |

### **Graph Analysis**
| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Topological Sort | O(V + E) | O(V) |
| SCC (Tarjan's) | O(V + E) | O(V) |
| Cycle Detection | O(V + E) | O(V) |
| Connected Components | O(V + E) | O(V) |

---

## 🎓 Learning Notes

### **When to Use Each Algorithm**

#### **Shortest Path**
- **BFS**: Unweighted graphs, guaranteed shortest path
- **Dijkstra**: Weighted graphs with positive weights
- **Bellman-Ford**: Weighted graphs with negative weights
- **A***: When you have a good heuristic function
- **Floyd-Warshall**: All-pairs shortest paths

#### **Graph Analysis**
- **Topological Sort**: Dependency resolution, task scheduling
- **SCC**: Finding strongly connected subgraphs
- **Cycle Detection**: Validating graph properties
- **Articulation Points**: Network reliability analysis

#### **Trees**
- **BST**: When you need ordered data with good average performance
- **AVL**: When you need guaranteed O(log n) operations
- **Trie**: String operations, prefix matching
- **N-ary**: General tree structures

### **Performance Tips**
1. **Choose the right data structure**: Match algorithm to problem requirements
2. **Consider input size**: Large graphs may need different approaches
3. **Heuristics matter**: A* performance depends heavily on heuristic quality
4. **Memory constraints**: Some algorithms use more space than others
5. **Implementation details**: Priority queue choice affects performance

---

**Note**: All complexity analyses assume standard implementations. Actual performance may vary based on specific optimizations and hardware characteristics. 