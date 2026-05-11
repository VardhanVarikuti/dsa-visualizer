# Contributing to DSA Visualizer

Thank you for your interest in contributing to the DSA Visualizer project! We welcome contributions that improve the educational value, performance, and accessibility of the tool.

## 🚀 How to Contribute

### 1. Adding New Algorithms
-   Implement the algorithm in the appropriate subdirectory within `core/`.
-   Use generator functions (`yield`) if you want to support step-by-step visualization.
-   Ensure the implementation is pure Python and follows standard algorithmic practices.

### 2. Improving Visualizations
-   Add or update visual logic in the `ui/` directory.
-   Follow the existing class structure and use the `Button` and `VisualNode` helpers.
-   **CRITICAL**: Use `utils.ui_helpers.draw_wrapped_messages` for any text rendering to ensure it remains responsive and doesn't overlap on small windows.
-   Maintain a consistent color palette using `ui.constants`.

### 3. Documentation
-   Update `ALGORITHM_COMPLEXITY.md` if you add a new algorithm.
-   Keep the `USER_GUIDE.md` and `DEVELOPER_GUIDE.md` updated with any significant changes.

## 🛠️ Development Environment
1.  Fork the repository and clone it.
2.  Install development dependencies: `pip install -r requirements.txt`.
3.  Run tests before submitting a PR: `pytest`.

## 🎨 Code Style
-   Follow PEP 8 guidelines.
-   Add descriptive docstrings to all classes and public functions.
-   Ensure UI elements are responsive and handle window resizing events correctly.

## 📬 Submitting Changes
-   Create a feature branch.
-   Commit with clear, descriptive messages.
-   Open a Pull Request with a summary of your changes and any new features added.

---
*Let's make algorithm learning accessible to everyone!*
