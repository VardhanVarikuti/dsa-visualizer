# DSA Visualizer - Developer Guide

This guide is for developers who want to contribute to, maintain, or extend the DSA Visualizer project.

---

## 🏗️ Project Architecture

### **Directory Structure**
```
dsa-visualizer/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── USER_GUIDE.md          # User documentation
├── ALGORITHM_COMPLEXITY.md # Algorithm analysis
├── DEVELOPER_GUIDE.md     # This file
├── menus/                 # CLI menu system
│   ├── main_menu.py       # Main application menu
│   ├── graph_menu.py      # Graph algorithm menu
│   └── tree_menu.py       # Tree algorithm menu
├── core/                  # Core algorithm implementations
│   ├── graph/             # Graph data structures and algorithms
│   │   ├── graph.py       # Graph class implementation
│   │   └── algorithms/    # Graph algorithm implementations
│   ├── tree/              # Tree data structures and algorithms
│   │   ├── bst.py         # Binary Search Tree
│   │   ├── avl.py         # AVL Tree
│   │   ├── trie.py        # Trie data structure
│   │   ├── nary_tree.py   # N-ary tree
│   │   └── operations.py  # Tree operations
│   ├── grid/              # Grid/maze algorithms
│   │   ├── grid.py        # Grid data structure
│   │   ├── cell.py        # Cell implementation
│   │   └── maze_algorithms/ # Pathfinding algorithms
│   └── n_queens/          # N-Queens backtracking
├── ui/                    # Pygame-based visualizers
│   ├── constants.py       # UI constants and colors
│   ├── weighted_graph_visualizer.py    # Weighted graph UI
│   ├── directed_graph_visualizer.py    # Directed graph UI
│   ├── undirected_graph_visualizer.py  # Undirected graph UI
│   ├── grid_visualizer.py # Grid/maze visualizer
│   ├── tree_visualizer.py # BST/AVL visualizer
│   ├── trie_visualizer.py # Trie visualizer
│   ├── nary_tree_visualizer.py # N-ary tree visualizer
│   ├── generic_tree_visualizer.py # Generic tree visualizer
│   └── nqueens_visualizer.py # N-Queens visualizer
└── utils/                 # Utility functions
    ├── colors.py          # Color definitions
    ├── timer.py           # Timing utilities
    └── helpers.py         # Helper functions
```

### **Core Design Principles**

#### **1. Separation of Concerns**
- **Core Logic**: Algorithm implementations in `core/`
- **UI Logic**: Visualization code in `ui/`
- **Menu Logic**: CLI navigation in `menus/`

#### **2. Modularity**
- Each algorithm is self-contained
- Visualizers are independent of core logic
- Easy to add new algorithms or visualizers

#### **3. Consistency**
- Standardized naming conventions
- Consistent error handling patterns
- Uniform UI/UX across visualizers

---

## 🔧 Development Setup

### **Prerequisites**
- Python 3.8 or higher
- Pygame 2.0.0 or higher
- Git for version control

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd dsa-visualizer

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### **Development Environment**
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest  # For testing
pip install black   # For code formatting
pip install flake8  # For linting
```

---

## 📝 Adding New Algorithms

### **Step 1: Implement Core Algorithm**

Create a new file in `core/graph/algorithms/` or `core/tree/`:

```python
"""
Your Algorithm Name
Brief description of what the algorithm does
"""

def your_algorithm(graph, source, target=None, visualize=False):
    """
    Your algorithm implementation
    
    Args:
        graph: Graph object
        source: Starting node
        target: Target node (if applicable)
        visualize: Whether to yield visualization steps
    
    Yields:
        Visualization steps for UI
    """
    # Initialize data structures
    visited = set()
    queue = [source]
    
    while queue:
        current = queue.pop(0)
        
        if visualize:
            yield ("visit", current)
        
        # Your algorithm logic here
        
        if visualize:
            yield ("done", result)
    
    return result
```

### **Step 2: Add to Algorithm List**

Update the appropriate `ALGO_LIST` in the visualizer:

```python
# In ui/weighted_graph_visualizer.py
ALGO_LIST = [
    # ... existing algorithms ...
    ("Your Algorithm", "Brief description"),
]
```

### **Step 3: Implement Visualization Logic**

Add visualization handling in the visualizer's `run_selected_algorithm` method:

```python
elif self.active_algo == "Your Algorithm":
    if not self.start_node:
        self.error_msg = "Please set a start node first."
        return
    
    try:
        # Call your algorithm
        result = your_algorithm(self.graph, self.start_node, visualize=True)
        self.animation_steps = list(result)
        self.animating = True
        self.animation_index = 0
    except Exception as e:
        self.error_msg = f"Error: {str(e)}"
```

### **Step 4: Add Example Graph**

Create an example in the `load_example_graph` method:

```python
elif self.active_algo == "Your Algorithm":
    # Add nodes
    self.add_node((200, 200))  # A
    self.add_node((400, 200))  # B
    # ... more nodes
    
    # Add edges
    self.add_edge('A', 'B', 5)
    # ... more edges
    
    self.start_node = self.nodes[0]  # Set start node
```

---

## 🎨 Adding New Visualizers

### **Step 1: Create Visualizer Class**

Create a new file in `ui/`:

```python
"""
Your Visualizer Name
Brief description of what this visualizer does
"""

import pygame
from ui.constants import *

class YourVisualizer:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Your Visualizer")
        # ... initialization code
    
    def setup_buttons(self):
        """Set up UI buttons"""
        # ... button setup code
    
    def draw(self):
        """Draw the visualization"""
        # ... drawing code
    
    def run(self):
        """Main event loop"""
        # ... event handling code

def run_your_visualizer():
    """Entry point for your visualizer"""
    YourVisualizer().run()
```

### **Step 2: Add to Menu System**

Update the appropriate menu file:

```python
# In menus/graph_menu.py or menus/tree_menu.py
def your_visualizer_menu():
    print("Launching Your Visualizer...")
    from ui.your_visualizer import run_your_visualizer
    run_your_visualizer()
```

### **Step 3: Follow UI Standards**

- Use consistent color schemes from `ui/constants.py`
- Implement standard controls (mouse, keyboard)
- Add proper error handling
- Include help text and instructions

---

## 🧪 Testing Guidelines

### **Unit Testing**
Create tests for core algorithms:

```python
# tests/test_algorithms.py
import pytest
from core.graph.graph import Graph
from core.graph.algorithms.your_algorithm import your_algorithm

def test_your_algorithm():
    # Create test graph
    graph = Graph(directed=True)
    graph.add_edge('A', 'B', 5)
    graph.add_edge('B', 'C', 3)
    
    # Test algorithm
    result = your_algorithm(graph, 'A', 'C')
    
    # Assert expected results
    assert result is not None
    # ... more assertions
```

### **Integration Testing**
Test visualizer integration:

```python
# tests/test_visualizers.py
def test_visualizer_import():
    """Test that visualizers can be imported"""
    from ui.weighted_graph_visualizer import WeightedGraphVisualizer
    assert WeightedGraphVisualizer is not None
```

### **Manual Testing Checklist**
- [ ] All algorithms work with example graphs
- [ ] UI controls respond correctly
- [ ] Error handling works properly
- [ ] Animations are smooth and clear
- [ ] Help text is accurate and helpful

---

## 🔍 Code Quality Standards

### **Python Style Guide**
Follow PEP 8 conventions:
- Use 4 spaces for indentation
- Maximum line length of 79 characters
- Use snake_case for functions and variables
- Use CamelCase for classes
- Add docstrings for all functions and classes

### **Code Organization**
```python
"""
Module docstring
Brief description of what this module does
"""

# Standard library imports
import sys
import os

# Third-party imports
import pygame

# Local imports
from ui.constants import *
from core.graph.graph import Graph

# Constants
CONSTANT_NAME = "value"

class YourClass:
    """Class docstring"""
    
    def __init__(self):
        """Initialize the class"""
        pass
    
    def your_method(self):
        """Method docstring"""
        pass
```

### **Error Handling**
```python
def safe_algorithm_call(self):
    """Example of proper error handling"""
    try:
        result = self.algorithm(self.graph, self.start_node)
        self.display_result(result)
    except ValueError as e:
        self.error_msg = f"Invalid input: {str(e)}"
    except Exception as e:
        self.error_msg = f"Unexpected error: {str(e)}"
        # Log the full error for debugging
        import traceback
        print(f"Error details: {traceback.format_exc()}")
```

---

## 🚀 Performance Optimization

### **Algorithm Optimization**
- Use appropriate data structures (heaps, sets, etc.)
- Avoid unnecessary computations in loops
- Cache results when possible
- Use generators for large datasets

### **UI Optimization**
- Limit frame rate for smooth animations
- Use efficient drawing techniques
- Minimize object creation in loops
- Use dirty rectangle rendering when possible

### **Memory Management**
- Clear unused data structures
- Use weak references when appropriate
- Avoid memory leaks in long-running visualizations

---

## 🐛 Debugging Guide

### **Common Issues**

#### **Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Test specific imports
python -c "from core.graph.algorithms.astar import astar"
```

#### **Pygame Issues**
```bash
# Check pygame installation
python -c "import pygame; print(pygame.version.ver)"

# Test pygame display
python -c "import pygame; pygame.init(); print('Pygame works')"
```

#### **Algorithm Errors**
- Add debug prints to algorithm functions
- Check input data validity
- Verify graph structure before algorithm execution

### **Debugging Tools**
```python
# Add to your code for debugging
import pdb; pdb.set_trace()  # Breakpoint

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

---

## 📚 Documentation Standards

### **Code Documentation**
- Add docstrings to all functions and classes
- Include parameter types and return values
- Provide usage examples for complex functions
- Document algorithm complexity where relevant

### **User Documentation**
- Update `USER_GUIDE.md` for new features
- Add screenshots for new visualizers
- Include step-by-step instructions
- Provide troubleshooting tips

### **Algorithm Documentation**
- Update `ALGORITHM_COMPLEXITY.md` for new algorithms
- Include time and space complexity analysis
- Explain when to use each algorithm
- Provide implementation notes

---

## 🔄 Contributing Workflow

### **1. Fork and Clone**
```bash
git clone <your-fork-url>
cd dsa-visualizer
git checkout -b feature/your-feature-name
```

### **2. Make Changes**
- Follow coding standards
- Add tests for new functionality
- Update documentation

### **3. Test Your Changes**
```bash
# Run basic tests
python -c "from ui.weighted_graph_visualizer import WeightedGraphVisualizer"

# Test specific functionality
python main.py
```

### **4. Commit and Push**
```bash
git add .
git commit -m "Add: brief description of changes"
git push origin feature/your-feature-name
```

### **5. Create Pull Request**
- Provide clear description of changes
- Include screenshots if UI changes
- Reference related issues

---

## 🎯 Best Practices

### **Algorithm Implementation**
- Start with a clear understanding of the algorithm
- Use standard data structures when possible
- Implement visualization steps for educational value
- Handle edge cases gracefully

### **UI Development**
- Keep visualizations clear and uncluttered
- Use consistent color schemes
- Provide clear feedback for user actions
- Include helpful error messages

### **Code Maintenance**
- Write self-documenting code
- Use meaningful variable names
- Keep functions small and focused
- Add comments for complex logic

### **Testing Strategy**
- Test with various input sizes
- Verify edge cases work correctly
- Ensure error handling is robust
- Test UI responsiveness

---

## 🚀 Future Enhancements

### **Planned Features**
- [ ] Export visualizations as images/videos
- [ ] Save/load graph configurations
- [ ] More algorithm visualizations
- [ ] Mobile-friendly interface
- [ ] Web-based version

### **Architecture Improvements**
- [ ] Plugin system for algorithms
- [ ] Configuration management
- [ ] Performance profiling tools
- [ ] Automated testing suite

### **Documentation Improvements**
- [ ] Interactive tutorials
- [ ] Video demonstrations
- [ ] Algorithm comparison tools
- [ ] Performance benchmarks

---

**Happy Coding! 🚀**

This developer guide should help you contribute effectively to the DSA Visualizer project. Remember to follow the established patterns and maintain code quality standards. 