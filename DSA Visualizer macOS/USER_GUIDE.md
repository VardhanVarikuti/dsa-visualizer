# DSA Visualizer - User Guide

Welcome to the DSA Visualizer! This interactive tool helps you understand Data Structures and Algorithms through visual representations and step-by-step animations.

## 🚀 Quick Start

### Installation
1. **Install Python** (version 3.8 or higher)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

### First Steps
1. Launch the application
2. Choose between **Trees** or **Graphs**
3. Select your preferred algorithm type
4. Follow the on-screen instructions

---

## 🌳 Tree Algorithms

### Generic Binary Tree
**For understanding basic tree operations**

#### How to Use:
1. Select **Trees** → **Generic Binary Tree**
2. **Click** to add nodes
3. **Right-click** to delete nodes
4. Watch traversals and LCA operations!

#### Features:
- **Insert/Delete**: Dynamic tree modification
- **Traversals**: Inorder, Preorder, Postorder
- **LCA (Lowest Common Ancestor)**: Find common ancestors

### BST (Binary Search Tree)
**For understanding ordered tree structures**

#### How to Use:
1. Select **Trees** → **BST**
2. **Click** to insert values
3. **Right-click** to delete nodes
4. Watch the tree maintain its order!

#### Features:
- **Automatic ordering**: Values are placed correctly
- **Search operations**: Find values efficiently
- **Traversals**: See the sorted order

### AVL Tree
**For understanding self-balancing trees**

#### How to Use:
1. Select **Trees** → **AVL**
2. **Click** to insert values
3. Watch automatic rebalancing!
4. **Right-click** to delete nodes

#### Features:
- **Automatic balancing**: Tree stays balanced
- **Rotation animations**: See how rebalancing works
- **Height maintenance**: Optimal performance

### Trie
**For understanding string data structures**

#### How to Use:
1. Select **Trees** → **Trie**
2. **Type words** to insert them
3. **Search** for existing words
4. **Prefix matching**: Find all words with a prefix

#### Features:
- **Word insertion**: Build the trie structure
- **Word search**: Find specific words
- **Prefix search**: Find all words with a prefix
- **Delete operations**: Remove words

### N-ary Tree
**For understanding general tree structures**

#### How to Use:
1. Select **Trees** → **N-ary Tree**
2. **Click** to add nodes
3. **Drag** to create parent-child relationships
4. Watch BFS and DFS traversals!

#### Features:
- **Flexible structure**: Any number of children
- **BFS traversal**: Level-by-level exploration
- **DFS traversal**: Depth-first exploration

---

## 📊 Graph Algorithms

### Maze/Grid Pathfinding
**Perfect for understanding search algorithms**

#### How to Use:
1. Select **Graphs** → **Maze/Grid**
2. **Click** to place walls
3. **Right-click** to set start/end points
4. Choose an algorithm and watch the search!

#### Available Algorithms:
- **BFS (Breadth-First Search)**: Guarantees shortest path
- **DFS (Depth-First Search)**: Explores deep paths first
- **A* Search**: Intelligent search with heuristics
- **Dijkstra**: Shortest path with weighted edges
- **Bidirectional BFS**: Search from both ends

### N-Queens Backtracking
**For understanding constraint satisfaction and backtracking**

#### How to Use:
1. Select **Graphs** → **N-Queens**
2. **Enter board size** (4-16)
3. **Step through** or **auto-solve** the puzzle
4. Watch the backtracking algorithm in action!

#### Features:
- **Interactive solving**: Step-by-step visualization
- **Auto-solve**: Watch the complete solution
- **Multiple solutions**: Explore different valid arrangements
- **Constraint satisfaction**: See how conflicts are resolved

### Undirected Graphs
**For understanding connectivity and graph properties**

#### How to Use:
1. Select **Graphs** → **Undirected Graph**
2. **Click** to add nodes
3. **Drag** to create undirected edges
4. Choose an algorithm and explore!

#### Available Algorithms:
- **BFS**: Level-by-level traversal
- **DFS**: Depth-first exploration
- **Connected Components**: Find all connected groups
- **Cycle Detection**: Detect cycles in undirected graphs
- **Articulation Points**: Find critical nodes
- **Bridges**: Find critical edges
- **Bipartite Check**: Check if graph is bipartite

### Directed Graphs
**For understanding graph traversal and analysis**

#### How to Use:
1. Select **Graphs** → **Directed Graph**
2. **Click** to add nodes
3. **Drag** from one node to another to create directed edges
4. Choose an algorithm and watch the visualization!

#### Available Algorithms:
- **BFS**: Level-by-level traversal
- **DFS**: Depth-first exploration
- **Cycle Detection**: Find cycles in the graph
- **Topological Sort**: Order nodes for dependency resolution
- **SCC (Strongly Connected Components)**: Find connected subgraphs
- **Transitive Closure**: Find all reachable pairs
- **Shortest Path (BFS)**: Unweighted shortest paths

### Weighted Graphs
**For understanding shortest path and minimum spanning tree algorithms**

#### How to Use:
1. Select **Graphs** → **Weighted Graph**
2. **Click** to add nodes
3. **Drag** to create edges (weights appear automatically)
4. **Click on edges** to edit weights
5. **Set Start/Target nodes** for pathfinding algorithms
6. Choose an algorithm and watch the computation!

#### Available Algorithms:
- **Dijkstra**: Single-source shortest paths
- **Bellman-Ford**: Handles negative weights
- **Floyd-Warshall**: All-pairs shortest paths
- **Prim's MST**: Minimum spanning tree
- **Kruskal's MST**: Alternative MST algorithm
- **A* Search**: Heuristic shortest path
- **Johnson's**: All-pairs shortest paths (sparse graphs)
- **SPFA**: Shortest path with negative weights
- **TopoSort+Relax**: Shortest paths in DAGs

---

## 🎮 Interactive Features

### Common Controls
- **Mouse Click**: Add nodes, select items
- **Mouse Drag**: Create edges, move nodes
- **Right Click**: Delete nodes/edges
- **Delete Key**: Remove selected items
- **R Key**: Reset the current visualization
- **H Key**: Show/hide help information
- **Q Key**: Quit the current visualization

### Visualization Features
- **Step-by-step animation**: Watch algorithms progress
- **Color coding**: Different colors for different states
- **Real-time updates**: See changes as they happen
- **Error messages**: Clear feedback when something goes wrong
- **Contextual buttons**: Only relevant buttons are shown

### Tips for Best Experience
1. **Start with examples**: Use "Load Example" buttons to see pre-built graphs
2. **Experiment**: Try different algorithms on the same graph
3. **Watch carefully**: Pay attention to the step-by-step animations
4. **Read messages**: The bottom of the screen shows helpful information
5. **Use help**: Press 'H' for additional information

---

## 🔧 Troubleshooting

### Common Issues

#### **Application won't start**
- **Solution**: Make sure Python 3.8+ is installed
- **Solution**: Run `pip install -r requirements.txt`

#### **Pygame errors**
- **Solution**: Update pygame: `pip install --upgrade pygame`
- **Solution**: On macOS, you might need: `brew install sdl2`

#### **Visualization is slow**
- **Solution**: Close other applications to free up memory
- **Solution**: Use smaller graphs for complex algorithms

#### **Buttons not responding**
- **Solution**: Make sure you're in the correct mode
- **Solution**: Check the bottom message for instructions

#### **Algorithm not working as expected**
- **Solution**: Verify your graph structure is correct
- **Solution**: Check if you've set start/target nodes when required
- **Solution**: Try the "Load Example" button for a working demonstration

### Getting Help
- **In-app help**: Press 'H' in any visualization
- **Error messages**: Read the messages at the bottom of the screen
- **Examples**: Use "Load Example" buttons to see working demonstrations

---

## 📚 Learning Resources

### Understanding the Algorithms
- **Start with BFS/DFS**: These are fundamental to understanding graph traversal
- **Move to shortest paths**: Dijkstra and A* show different approaches
- **Explore trees**: BST and AVL demonstrate data structure concepts
- **Try complex algorithms**: SCC and MST show advanced graph concepts

### Recommended Learning Path
1. **Beginner**: BFS, DFS, Basic Tree Traversals
2. **Intermediate**: Dijkstra, A*, BST, AVL
3. **Advanced**: SCC, MST, Complex Graph Algorithms

### Tips for Learning
- **Watch the animations**: Don't just look at the final result
- **Try different inputs**: See how algorithms behave with different data
- **Compare algorithms**: Run different algorithms on the same graph
- **Build your own graphs**: Create custom examples to test understanding

---

## 🎯 Advanced Features

### Custom Graph Creation
- **Add nodes**: Click anywhere to place nodes
- **Add edges**: Drag from one node to another
- **Edit weights**: Click on edges to modify weights (weighted graphs)
- **Delete elements**: Right-click or use Delete key

### Algorithm Parameters
- **Start nodes**: Required for pathfinding algorithms
- **Target nodes**: Required for A* algorithm
- **Edge weights**: Important for weighted algorithms

### Export and Sharing
- **Screenshots**: Use your system's screenshot tool
- **Video recording**: Record the animations for presentations
- **Graph sharing**: Recreate interesting examples

---

## 🏆 Success Tips

1. **Start simple**: Begin with basic algorithms before moving to complex ones
2. **Use examples**: The "Load Example" buttons provide great starting points
3. **Experiment**: Try different graph structures and see how algorithms behave
4. **Take notes**: Observe patterns in how algorithms work
5. **Practice**: Recreate examples from your textbooks or courses

---

**Happy Learning! 🚀**

The DSA Visualizer is designed to make complex algorithms accessible and understandable. Take your time, experiment, and enjoy the learning process! 