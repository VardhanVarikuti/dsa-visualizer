# 🚀 DSA Visualizer: Technical Walkthrough

Welcome to the **DSA Visualizer**! This project is a high-performance, interactive tool designed to make complex Data Structures and Algorithms intuitive through real-time visualization.

## 📁 Project Architecture

The codebase is organized into a modular structure that separates logic from representation:

-   **`core/`**: The brain of the application. Contains the pure Python implementations of graphs, trees, and algorithms.
-   **`ui/`**: The visual layer. Built with Pygame, it handles rendering, animations, and user interactions.
-   **`menus/`**: CLI-based navigation system that acts as the entry point for various visualizer modules.
-   **`utils/`**: Shared helpers for UI, colors, and timing.
-   **`assets/`**: Static assets like the application icon.
-   **DevOps Suite**:
    -   `Dockerfile` & `.dockerignore`: For containerization.
    -   `terraform/`: Infrastructure as Code for AWS deployment.
    -   `kubernetes/`: Orchestration manifests for scaling.
    -   `monitoring/`: Prometheus and Grafana configurations.

## ✨ Core Features

### 🌳 Tree Visualizers
-   **Generic Binary Tree**: Support for any binary tree structure with animated LCA (Lowest Common Ancestor) pathfinding.
-   **BST & AVL Trees**: Real-time balancing animations and property checks.
-   **Trie Visualizer**: Visualize word insertions and prefix searches.

### 📊 Graph Visualizers
-   **Interactive Editing**: Click to add nodes, drag to create edges.
-   **Comprehensive Algorithms**:
    -   **Traversal**: BFS, DFS (with speed control).
    -   **Connectivity**: Connected Components, Articulation Points, Bridges.
    -   **Shortest Paths**: Dijkstra, Bellman-Ford, Floyd-Warshall.
    -   **Spanning Trees**: Prim, Kruskal.
-   **Dynamic Layouts**: Content wraps and scales to fit any window size.

### 🧩 Miscellaneous Visuals
-   **Maze Pathfinding**: Compare BFS, DFS, A*, and Dijkstra on a grid. Includes obstacle drawing.
-   **N-Queens**: Watch the backtracking algorithm find solutions in real-time.

## ☁️ DevOps & Deployment

This project is built for the modern cloud:

1.  **Headless GUI**: Uses `Xvfb` (Virtual Framebuffer) to run Pygame inside a container without a physical monitor.
2.  **Web Access**: `x11vnc` and `noVNC` bridge the X11 display to your browser via WebSockets.
3.  **CI/CD**: A full Jenkins pipeline handles building, testing, and pushing images.
4.  **Scaling**: Terraform sets up an AWS EKS cluster, and Kubernetes manages the deployment.

## 🛠️ How to Run

### Local Development
```bash
pip install -r requirements.txt
python main.py
```

### Dockerized Run
```bash
docker build -t dsa-visualizer .
docker run -p 6080:6080 dsa-visualizer
```
Access via: `http://localhost:6080/vnc.html`

## 🤝 Contributing
Feel free to add new algorithms to the `core/` directory and create corresponding visual logic in `ui/`. Ensure all text rendering uses the `draw_wrapped_messages` helper to maintain responsiveness.

---
*Created with ❤️ by the DSA Visualizer Team*