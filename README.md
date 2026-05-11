# DSA Visualizer 🚀

A comprehensive Python framework for visualizing Data Structures and Algorithms through interactive CLI menus and beautiful Pygame GUIs. Deployed to the web using X11 + noVNC with a full DevOps pipeline.

## ✨ What's Included

### **Tree Algorithms** 🌳
- **Binary Trees**: BST, AVL, Generic Binary Tree
- **Specialized Trees**: Trie, N-ary Tree
- **Operations**: Insert, Delete, Traversals, LCA, Search

### **Graph Algorithms** 📊
- **Undirected Graph**: BFS, DFS, Connected Components, Bipartite Check
- **Directed Graph**: Topological Sort, Bellman-Ford, Cycle Detection
- **Weighted Graph**: Dijkstra, Prim, Kruskal, Floyd-Warshall

### **Miscellaneous** 🧩
- **Maze/Grid Pathfinding**: BFS, DFS, A*, Dijkstra, Bidirectional BFS
- **N-Queens**: Backtracking visualization

### **Interactive Features**
- Real-time animations with step-by-step visualization
- Dynamic layouts that adapt to content
- Error handling with clear feedback

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🏗️ Build Standalone Executables

```bash
# macOS
bash build_scripts/build_macos.sh

# Linux
bash build_scripts/build_linux.sh

# Windows
build_scripts\build_windows.bat
```

## ☁️ DevOps Deployment (X11 + noVNC)

See [README_DEVOPS.md](README_DEVOPS.md) for the full pipeline:
- **Docker**: Containerized Pygame app with virtual display
- **Kubernetes**: Orchestrated deployment
- **Jenkins**: CI/CD pipeline
- **Terraform**: AWS infrastructure
- **Prometheus + Grafana**: Monitoring stack

```bash
# Quick local test
docker build -t dsa-visualizer .
docker run -p 6080:6080 dsa-visualizer
# Open http://localhost:6080/vnc.html
```

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)**: Complete user guide
- **[ALGORITHM_COMPLEXITY.md](ALGORITHM_COMPLEXITY.md)**: Complexity analysis
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)**: Developer documentation
- **[README_DEVOPS.md](README_DEVOPS.md)**: DevOps pipeline guide

## 📄 License

MIT License - See [LICENSE](LICENSE)