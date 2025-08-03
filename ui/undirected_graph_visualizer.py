import pygame
import sys
import string
import math
from core.graph.graph import Graph
# Import algorithms (to be implemented if not present)
from core.graph.algorithms.bfs import bfs
from core.graph.algorithms.dfs import dfs
from core.graph.algorithms.connected_components import connected_components
from core.graph.algorithms.cycle_detection_undirected import has_cycle_undirected
from core.graph.algorithms.articulation_points import articulation_points_and_bridges
from core.graph.algorithms.bipartite import is_bipartite
from .constants import *

ALGO_LIST = [
    ("BFS", "Breadth-First Search"),
    ("DFS", "Depth-First Search"),
    ("Connected Components", "Find all connected groups"),
    ("Cycle Detection", "Detect cycles"),
    ("Articulation Points", "Find critical nodes"),
    ("Bridges", "Find critical edges"),
    ("Bipartite Check", "Check if graph is bipartite")
]

MODE_EDIT = 'Edit Graph'
MODE_SET_START = 'Set Start Node'

class VisualNode:
    """A visual node in the graph, with label and position."""
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.selected = False
        # For coloring/animation
        self.color_id = None
        self.temp_color = None
        self.is_ap = False
        self.is_conflict = False

class VisualEdge:
    """A visual edge between two VisualNode objects."""
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.selected = False
        self.is_bridge = False

class Button:
    """A clickable UI button."""
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.active = False

    def draw(self, win, font):
        """Draw the button on the window."""
        color = BUTTON_ACTIVE if self.active else BUTTON_COLOR
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        pygame.draw.rect(win, (100,100,100), self.rect, 2, border_radius=8)
        btn_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        surf = btn_font.render(self.text, True, BUTTON_TEXT)
        rect = surf.get_rect(center=self.rect.center)
        win.blit(surf, rect)

    def is_hover(self, pos):
        """Check if the mouse is over the button."""
        return self.rect.collidepoint(pos)

class UndirectedGraphVisualizer:
    """Main class for the undirected graph visualizer UI and logic."""
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Undirected Graph Visualizer")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=False)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.start_node = None  # For BFS/DFS
        self.dragging = False
        self.drag_start = None
        self.selected_edge = None
        self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        self.error_msg = ''
        self.result_msg = ''
        self.buttons = []
        self.example_buttons = []
        self.run_button = None
        self.mode_buttons = []
        self.current_mode = MODE_EDIT
        self.active_algo = None
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.animation_delay = 600  # ms
        self.show_help = False
        self.setup_buttons()

    def setup_buttons(self):
        """Set up all UI buttons for algorithms, modes, and actions."""
        # Place algorithm buttons at the top, more spacious and centered
        w, h = 150, 36
        gap = 30
        total_width = len(ALGO_LIST) * w + (len(ALGO_LIST)-1) * gap
        x = (WIDTH - total_width) // 2
        y = 16
        self.buttons = []
        for i, (algo, desc) in enumerate(ALGO_LIST):
            btn = Button((x + i*(w+gap), y, w, h), algo, lambda a=algo: self.select_algo(a))
            self.buttons.append(btn)
        # Mode buttons (top left)
        mb_w, mb_h = 140, 32
        mb_x, mb_y = 30, y + h + 30
        self.mode_buttons = [
            Button((mb_x, mb_y, mb_w, mb_h), "Edit Graph", lambda: self.set_mode(MODE_EDIT)),
        ]
        
        # Add Set Start Node button only for algorithms that require it
        start_node_algorithms = ["BFS", "DFS"]
        if self.active_algo in start_node_algorithms:
            self.mode_buttons.append(Button((mb_x + mb_w + 16, mb_y, mb_w, mb_h), "Set Start Node", lambda: self.set_mode(MODE_SET_START)))
        # Example and Run buttons: vertical stack at top right, below algo buttons
        btn_w, btn_h = 150, 36
        btn_x = WIDTH - btn_w - 30
        btn_y1 = y + h + 30  # 30px below algo buttons
        btn_y2 = btn_y1 + btn_h + 12
        self.example_buttons = [
            Button((btn_x, btn_y1, btn_w, btn_h), "Load Example", self.load_example_graph)
        ]
        self.run_button = Button((btn_x, btn_y2, btn_w, btn_h), "Run", self.run_selected_algorithm)

    def set_mode(self, mode):
        """Switch between edit and set start node modes."""
        self.current_mode = mode
        if mode == MODE_EDIT:
            self.error_msg = "Edit mode: Click to add node, drag to add edge."
        elif mode == MODE_SET_START:
            self.error_msg = "Set Start Node mode: Click a node to select as start for BFS/DFS."

    def select_algo(self, algo):
        """Select an algorithm and update UI state."""
        self.active_algo = algo
        self.result_msg = ''
        self.error_msg = f"Selected: {algo}. Click 'Load Example' for a demo, or build your own graph."
        self.start_node = None
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        # Rebuild buttons to show/hide Set Start Node button based on selected algorithm
        self.setup_buttons()
        # Do NOT clear the graph here! Only update UI state.
        self.set_mode(MODE_EDIT)

    def load_example_graph(self):
        """Load a demo/example graph for the selected algorithm."""
        # Always clear the graph before loading a new example
        self.nodes.clear()
        self.edges.clear()
        self.graph = Graph(directed=False)
        self.node_labels = iter(string.ascii_uppercase)
        used_labels = set()
        orig_add_node_at = self._add_node_at
        def add_and_track(pos):
            node = orig_add_node_at(pos)
            if node:
                used_labels.add(node.label)
            return node
        self._add_node_at = add_and_track
        self.start_node = None
        if self.active_algo == "BFS":
            self._example_bfs_graph()
        elif self.active_algo == "DFS":
            self._example_dfs_graph()
        elif self.active_algo == "Connected Components":
            self._example_components()
        elif self.active_algo == "Cycle Detection":
            self._example_cycle()
        elif self.active_algo == "Articulation Points":
            self._example_articulation()
        elif self.active_algo == "Bridges":
            self._example_bridges()
        elif self.active_algo == "Bipartite Check":
            self._example_bipartite()
        # Restore the original method BEFORE updating node_labels
        self._add_node_at = orig_add_node_at
        all_labels = [c for c in string.ascii_uppercase if c not in used_labels]
        self.node_labels = iter(all_labels)
        self.result_msg = ''
        self.error_msg = f"Loaded example for {self.active_algo}."
        self.set_mode(MODE_EDIT)

    # General graph for BFS
    def _example_bfs_graph(self):
        self._add_node_at((200, 200)) # A
        self._add_node_at((400, 200)) # B
        self._add_node_at((600, 200)) # C
        self._add_node_at((300, 400)) # D
        self._add_node_at((500, 400)) # E
        self._add_node_at((700, 400)) # F
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('B', 'C')
        self._add_edge_by_label('A', 'D')
        self._add_edge_by_label('B', 'D')
        self._add_edge_by_label('B', 'E')
        self._add_edge_by_label('C', 'F')
        self._add_edge_by_label('E', 'F')
    # General graph for DFS
    def _example_dfs_graph(self):
        self._add_node_at((200, 200)) # A
        self._add_node_at((400, 200)) # B
        self._add_node_at((600, 200)) # C
        self._add_node_at((300, 400)) # D
        self._add_node_at((500, 400)) # E
        self._add_node_at((700, 400)) # F
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('B', 'C')
        self._add_edge_by_label('A', 'D')
        self._add_edge_by_label('B', 'D')
        self._add_edge_by_label('B', 'E')
        self._add_edge_by_label('C', 'F')
        self._add_edge_by_label('E', 'F')
    def _example_components(self):
        # Two components
        self._add_node_at((200, 200)) # A
        self._add_node_at((350, 200)) # B
        self._add_node_at((200, 350)) # C
        self._add_node_at((350, 350)) # D
        self._add_node_at((700, 200)) # E
        self._add_node_at((850, 200)) # F
        self._add_node_at((700, 350)) # G
        self._add_node_at((850, 350)) # H
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('A', 'C')
        self._add_edge_by_label('B', 'D')
        self._add_edge_by_label('C', 'D')
        self._add_edge_by_label('E', 'F')
        self._add_edge_by_label('E', 'G')
        self._add_edge_by_label('F', 'H')
        self._add_edge_by_label('G', 'H')
    def _example_cycle(self):
        # Simple cycle
        self._add_node_at((300, 300)) # A
        self._add_node_at((500, 300)) # B
        self._add_node_at((400, 500)) # C
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('B', 'C')
        self._add_edge_by_label('C', 'A')
    def _example_articulation(self):
        # Articulation point: B
        self._add_node_at((300, 300)) # A
        self._add_node_at((500, 300)) # B
        self._add_node_at((700, 300)) # C
        self._add_node_at((500, 500)) # D
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('B', 'C')
        self._add_edge_by_label('B', 'D')
    def _example_bridges(self):
        # Bridge: B-C
        self._add_node_at((300, 300)) # A
        self._add_node_at((500, 300)) # B
        self._add_node_at((700, 300)) # C
        self._add_node_at((500, 500)) # D
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('B', 'C')
        self._add_edge_by_label('C', 'D')
    def _example_bipartite(self):
        # Bipartite: two sets
        self._add_node_at((300, 300)) # A
        self._add_node_at((300, 500)) # B
        self._add_node_at((500, 300)) # C
        self._add_node_at((500, 500)) # D
        self._add_edge_by_label('A', 'B')
        self._add_edge_by_label('A', 'D')
        self._add_edge_by_label('C', 'B')
        self._add_edge_by_label('C', 'D')

    def _add_node_at(self, pos):
        """Add a node at the given position and return it."""
        try:
            label = next(self.node_labels)
        except StopIteration:
            return
        node = VisualNode(label, pos)
        self.nodes.append(node)
        self.graph.adj[label] = []
        return node
    def _add_edge_by_label(self, l1, l2):
        """Add an edge between nodes with labels l1 and l2."""
        n1 = next((n for n in self.nodes if n.label == l1), None)
        n2 = next((n for n in self.nodes if n.label == l2), None)
        if n1 and n2:
            self.edges.append(VisualEdge(n1, n2))
            self.graph.add_edge(n1.label, n2.label)

    def reset(self):
        """Reset the graph and UI to the initial state."""
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=False)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.selected_edge = None
        self.dragging = False
        self.drag_start = None
        self.message = "Click to add node | Drag to add edge | Del: delete | R: Reset | Q: Quit | H: Help"
        self.error_msg = ''
        self.result_msg = ''
        self.active_algo = None
        self.start_node = None
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.set_mode(MODE_EDIT)

    def add_node(self, pos):
        """Add a node at the given position, preventing overlap."""
        # Prevent overlap: do not add if too close to existing node
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 < (2 * NODE_RADIUS) ** 2:
                self.error_msg = "Too close to another node. Move further away."
                return None
        node = self._add_node_at(pos)
        return node

    def get_node_at_pos(self, pos):
        """Return the node at the given position, if any."""
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 <= NODE_RADIUS ** 2:
                return node
        return None

    def add_edge(self, u, v):
        """Add an edge between two nodes, if valid."""
        if u == v:
            self.error_msg = "No self-loops allowed."
            return
        for edge in self.edges:
            if (edge.u == u and edge.v == v) or (edge.u == v and edge.v == u):
                self.error_msg = "Edge already exists."
                return
        self.edges.append(VisualEdge(u, v))
        self.graph.add_edge(u.label, v.label)

    def get_edge_at_pos(self, pos):
        """Return the edge at the given position, if any."""
        for edge in self.edges:
            u, v = edge.u, edge.v
            x1, y1 = u.pos
            x2, y2 = v.pos
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            # For curved edges, check near the control point as well
            dist_to_line = self._point_line_distance(pos, u.pos, v.pos)
            if dist_to_line <= NODE_RADIUS // 2:
                return edge
            # For multiple edges, check near the curve
            key = tuple(sorted([u.label, v.label]))
            if sum(1 for e in self.edges if tuple(sorted([e.u.label, e.v.label])) == key) > 1:
                dx, dy = y2 - y1, x1 - x2
                norm = math.hypot(dx, dy)
                if norm == 0:
                    norm = 1
                offset = 30
                ox, oy = mx + dx / norm * offset, my + dy / norm * offset
                if math.hypot(pos[0] - ox, pos[1] - oy) <= NODE_RADIUS:
                    return edge
        return None

    def delete_selected(self):
        """Delete the currently selected node or edge."""
        if self.selected_node:
            self.edges = [e for e in self.edges if e.u != self.selected_node and e.v != self.selected_node]
            if self.selected_node.label in self.graph.adj:
                del self.graph.adj[self.selected_node.label]
            for adj in self.graph.adj.values():
                adj[:] = [pair for pair in adj if pair[0] != self.selected_node.label]
            self.nodes.remove(self.selected_node)
            self.selected_node = None
            if self.start_node and self.start_node not in self.nodes:
                self.start_node = None
        elif self.selected_edge:
            self.edges.remove(self.selected_edge)
            u, v = self.selected_edge.u.label, self.selected_edge.v.label
            self.graph.adj[u] = [pair for pair in self.graph.adj[u] if pair[0] != v]
            self.graph.adj[v] = [pair for pair in self.graph.adj[v] if pair[0] != u]
            self.selected_edge = None

    def draw(self):
        """Draw the entire UI, including nodes, edges, buttons, and messages."""
        # Always get current window size
        win_width, win_height = self.win.get_size()
        self.win.fill(BG_COLOR)
        # Draw edges (curved if needed)
        edge_counts = {}
        for edge in self.edges:
            key = tuple(sorted([edge.u.label, edge.v.label]))
            edge_counts[key] = edge_counts.get(key, 0) + 1
        edge_drawn = {}
        for edge in self.edges:
            color = EDGE_SELECTED_COLOR if edge.selected else EDGE_COLOR
            u, v = edge.u, edge.v
            key = tuple(sorted([u.label, v.label]))
            count = edge_counts[key]
            idx = edge_drawn.get(key, 0)
            if count == 1:
                # Single edge: straight line
                pygame.draw.line(self.win, color, u.pos, v.pos, 3)
            else:
                # Multiple edges: draw as offset curves
                # Compute midpoint and perpendicular offset
                x1, y1 = u.pos
                x2, y2 = v.pos
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = y2 - y1, x1 - x2
                norm = math.hypot(dx, dy)
                if norm == 0:
                    norm = 1
                offset = 30 * ((idx + 1) - (count + 1) / 2)
                ox, oy = mx + dx / norm * offset, my + dy / norm * offset
                points = [u.pos, (ox, oy), v.pos]
                pygame.draw.aalines(self.win, color, False, points, 2)
            edge_drawn[key] = idx + 1
        # Draw nodes
        for node in self.nodes:
            if node == self.start_node:
                color = (0, 200, 0)  # Highlight start node
            elif hasattr(node, 'color_id') and node.color_id is not None:
                color = COMPONENT_COLORS[node.color_id % len(COMPONENT_COLORS)]
            elif hasattr(node, 'temp_color') and node.temp_color is not None:
                color = node.temp_color
            elif node.selected:
                color = NODE_SELECTED_COLOR
            else:
                color = NODE_COLOR
            pygame.draw.circle(self.win, color, node.pos, NODE_RADIUS)
            pygame.draw.circle(self.win, (0,0,0), node.pos, NODE_RADIUS, 2)
            label_surf = self.font.render(node.label, True, TEXT_COLOR)
            rect = label_surf.get_rect(center=node.pos)
            self.win.blit(label_surf, rect)
        # Draw dragging edge
        if self.dragging and self.drag_start:
            pygame.draw.line(self.win, (120,120,120), self.drag_start.pos, pygame.mouse.get_pos(), 2)
        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.win, self.font)
        for btn in self.mode_buttons:
            btn.draw(self.win, self.font)
        if self.active_algo:
            for btn in self.example_buttons:
                btn.draw(self.win, self.font)
            self.run_button.draw(self.win, self.font)
        # Draw current mode
        mode_surf = self.font.render(f"Mode: {self.current_mode}", True, (80, 80, 80))
        self.win.blit(mode_surf, (30, win_height-40))
        # Draw messages
        self.show_message(self.message, INSTR_COLOR, y_abs=win_height-60)
        if self.error_msg:
            self.show_message(self.error_msg, ERROR_COLOR, y_abs=win_height-30)
        if self.result_msg:
            self.show_message(self.result_msg, (0, 120, 0), y_abs=win_height-90)
        # Show animation speed if animating
        if self.animating:
            self.show_message(f"Animation speed: {self.animation_delay} ms (+/-)", (80, 80, 80), y_abs=win_height-120)
        # Draw help overlay if needed
        if self.show_help:
            overlay = pygame.Surface((win_width, win_height), pygame.SRCALPHA)
            overlay.fill((240, 240, 255, 230))
            self.win.blit(overlay, (0, 0))
            help_lines = [
                "CONTROLS:",
                "Left Click: Add node / Select node / Drag to add edge",
                "Right Click: Select edge",
                "Del/Backspace: Delete selected node/edge",
                "R: Reset graph",
                "Q: Quit",
                "E: Edit mode",
                "S: Set start node (for BFS/DFS)",
                "+/-: Adjust animation speed",
                "H: Toggle this help overlay",
                "",
                "ALGORITHMS:",
                "BFS/DFS: Traversal from start node (select node, then Run)",
                "Connected Components: Finds all groups",
                "Cycle Detection: Finds a cycle if present",
                "Articulation Points: Finds critical nodes",
                "Bridges: Finds critical edges",
                "Bipartite Check: 2-coloring test",
                "",
                "Use 'Load Example' for a demo graph for each algorithm!"
            ]
            font = pygame.font.SysFont(None, 28)
            for i, line in enumerate(help_lines):
                surf = font.render(line, True, (30, 30, 80))
                rect = surf.get_rect(center=(win_width//2, 80 + i*32))
                self.win.blit(surf, rect)
            pygame.display.update()
            return
        pygame.display.update()

    def show_message(self, msg, color, y_abs):
        win_width, _ = self.win.get_size()
        surf = self.font.render(msg, True, color)
        rect = surf.get_rect(center=(win_width//2, y_abs))
        self.win.blit(surf, rect)

    def run_selected_algorithm(self):
        """Start the selected algorithm and prepare animation steps."""
        if not self.active_algo:
            self.error_msg = "Select an algorithm first."
            return
        self.result_msg = ''
        self.error_msg = ''
        self.animation_steps = []
        self.animation_index = 0
        self.animating = False
        # Reset all node/edge highlights
        for node in self.nodes:
            node.selected = False
            node.color_id = None
            node.temp_color = None
            node.is_ap = False
            node.is_conflict = False
        for edge in self.edges:
            edge.selected = False
            edge.is_bridge = False
        if self.active_algo in ("BFS", "DFS"):
            if not self.start_node:
                self.error_msg = "Select a start node (click a node) before running."
                return
            self.animating = True
            self.animation_steps = list(bfs(self.graph, self.start_node.label)) if self.active_algo == "BFS" else list(dfs(self.graph, self.start_node.label))
            self.animation_index = 0
        elif self.active_algo == "Connected Components":
            self.animating = True
            self.animation_steps = list(connected_components(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Cycle Detection":
            self.animating = True
            self.animation_steps = list(has_cycle_undirected(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Articulation Points":
            self.animating = True
            self.animation_steps = list(articulation_points_and_bridges(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Bridges":
            self.animating = True
            self.animation_steps = list(articulation_points_and_bridges(self.graph, visualize=True))
            self.animation_index = 0
        elif self.active_algo == "Bipartite Check":
            self.animating = True
            self.animation_steps = list(is_bipartite(self.graph, visualize=True))
            self.animation_index = 0
        else:
            self.error_msg = f"{self.active_algo} not implemented yet."

    def animate(self):
        """Animate the algorithm step-by-step, updating the UI."""
        if self.animating and self.animation_index < len(self.animation_steps):
            step = self.animation_steps[self.animation_index]
            # Reset highlights for each step
            for node in self.nodes:
                node.selected = False
                node.temp_color = None
                node.is_ap = False
                node.is_conflict = False
            for edge in self.edges:
                edge.selected = False
                edge.is_bridge = False
            msg = ''
            if self.active_algo in ("BFS", "DFS"):
                # step is node label
                for node in self.nodes:
                    node.selected = (node.label == step)
                msg = f"{self.active_algo} visiting: {step}"
            elif self.active_algo == "Connected Components":
                # step: (type, ...)
                if step[0] == "new_component":
                    self.current_component_color = COMPONENT_COLORS[step[1] % len(COMPONENT_COLORS)]
                    msg = f"New component {step[1]+1}"
                elif step[0] == "visit":
                    label = step[1]
                    color_id = step[2]
                    for node in self.nodes:
                        if node.label == label:
                            node.selected = True
                            node.color_id = color_id
                    msg = f"Component {color_id+1}: visiting {label}"
                elif step[0] == "done":
                    comps, color_map = step[1], step[2]
                    for node in self.nodes:
                        if node.label in color_map:
                            node.color_id = color_map[node.label]
                    msg = f"Found {len(comps)} components."
            elif self.active_algo == "Cycle Detection":
                if step[0] == "visit":
                    label = step[1]
                    path = step[2]
                    for node in self.nodes:
                        if node.label in path:
                            node.selected = True
                    msg = f"DFS path: {' → '.join(path)}"
                elif step[0] == "cycle":
                    cycle_path = step[1]
                    for node in self.nodes:
                        if node.label in cycle_path:
                            node.selected = True
                    msg = f"Cycle found: {' → '.join(cycle_path)}"
                elif step[0] == "done":
                    has_cycle = step[1]
                    cycle_path = step[2]
                    if has_cycle:
                        msg = f"Cycle Detected! Path: {' → '.join(cycle_path)}"
                    else:
                        msg = "No Cycles."
            elif self.active_algo in ("Articulation Points", "Bridges"):
                if step[0] == "visit":
                    label = step[1]
                    for node in self.nodes:
                        if node.label == label:
                            node.selected = True
                    msg = f"DFS visiting: {label}"
                elif step[0] == "ap":
                    label = step[1]
                    for node in self.nodes:
                        if node.label == label:
                            node.is_ap = True
                    msg = f"Articulation Point: {label}"
                elif step[0] == "bridge":
                    u, v = step[1]
                    for edge in self.edges:
                        if (edge.u.label, edge.v.label) == (u, v) or (edge.u.label, edge.v.label) == (v, u):
                            edge.is_bridge = True
                    msg = f"Bridge: {u}-{v}"
                elif step[0] == "done":
                    aps, bridges = step[1], step[2]
                    msg = f"Articulation Points: {sorted(aps)} | Bridges: {sorted(bridges)}"
            elif self.active_algo == "Bipartite Check":
                if step[0] == "color":
                    label = step[1]
                    color = step[2]
                    for node in self.nodes:
                        if node.label == label:
                            node.temp_color = BIPARTITE_COLORS[color % len(BIPARTITE_COLORS)]
                    msg = f"Coloring {label} as set {color+1}"
                elif step[0] == "conflict":
                    v, w = step[1], step[2]
                    for node in self.nodes:
                        if node.label in (v, w):
                            node.is_conflict = True
                    msg = f"Conflict: {v} and {w} have same color!"
                elif step[0] == "done":
                    is_bip, color_map, conflict = step[1], step[2], step[3]
                    for node in self.nodes:
                        if node.label in color_map:
                            node.temp_color = BIPARTITE_COLORS[color_map[node.label] % len(BIPARTITE_COLORS)]
                    if is_bip:
                        msg = "Graph is Bipartite!"
                    else:
                        msg = f"Not Bipartite. Conflict: {conflict[0]}-{conflict[1]}"
            self.result_msg = msg
            self.draw()
            pygame.time.delay(self.animation_delay)
            self.animation_index += 1
        else:
            self.animating = False
            # Final result message for each algo
            if self.active_algo == "Connected Components" and self.animation_steps:
                comps = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else []
                self.result_msg = f"Connected Components: {['{' + ', '.join(comp) + '}' for comp in comps]}"
            elif self.active_algo == "Cycle Detection" and self.animation_steps:
                has_cycle = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else False
                cycle_path = self.animation_steps[-1][2] if self.animation_steps[-1][0] == "done" else []
                self.result_msg = "Cycle Detected!" if has_cycle else "No Cycles."
            elif self.active_algo in ("Articulation Points", "Bridges") and self.animation_steps:
                aps = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else []
                bridges = self.animation_steps[-1][2] if self.animation_steps[-1][0] == "done" else []
                self.result_msg = f"Articulation Points: {sorted(aps)} | Bridges: {sorted(bridges)}"
            elif self.active_algo == "Bipartite Check" and self.animation_steps:
                is_bip = self.animation_steps[-1][1] if self.animation_steps[-1][0] == "done" else True
                self.result_msg = "Bipartite" if is_bip else "Not Bipartite"
            elif self.active_algo in ("BFS", "DFS") and self.animation_steps:
                order = [str(x) for x in self.animation_steps]
                self.result_msg = f"{self.active_algo} order: {' -> '.join(order)}"
            for node in self.nodes:
                node.selected = False
                node.is_ap = False
                node.is_conflict = False
            for edge in self.edges:
                edge.selected = False
                edge.is_bridge = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            if self.animating:
                self.animate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    # Update window size
                    self.win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    # Optionally, reposition nodes/buttons here for dynamic layout
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_help:
                        self.show_help = False
                        continue
                    # 1. Check all buttons first
                    for btn in self.mode_buttons + self.buttons + self.example_buttons + [self.run_button]:
                        if btn.is_hover(event.pos):
                            btn.active = True
                            btn.action()
                            break
                    else:
                        node = self.get_node_at_pos(event.pos)
                        if self.current_mode == MODE_SET_START and node:
                            self.start_node = node
                            self.error_msg = f"Start node: {node.label}. Click 'Run' to start {self.active_algo}."
                        elif self.current_mode == MODE_EDIT:
                            if node:
                                self.selected_node = node
                                node.selected = True
                                self.dragging = True
                                self.drag_start = node
                            else:
                                self.add_node(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging and self.drag_start:
                        node = self.get_node_at_pos(event.pos)
                        if node and node != self.drag_start:
                            self.add_edge(self.drag_start, node)
                        self.dragging = False
                        self.drag_start = None
                        if self.selected_node:
                            self.selected_node.selected = False
                            self.selected_node = None
                    for btn in self.buttons + self.example_buttons + [self.run_button] + self.mode_buttons:
                        btn.active = False
                elif event.type == pygame.KEYDOWN:
                    self.error_msg = ''
                    if event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.delete_selected()
                    elif event.key == pygame.K_e:
                        self.set_mode(MODE_EDIT)
                    elif event.key == pygame.K_s:
                        self.set_mode(MODE_SET_START)
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.animation_delay = max(100, self.animation_delay - 100)
                        self.error_msg = f"Animation speed: {self.animation_delay} ms"
                    elif event.key == pygame.K_MINUS:
                        self.animation_delay = min(2000, self.animation_delay + 100)
                        self.error_msg = f"Animation speed: {self.animation_delay} ms"
                    elif event.key == pygame.K_h:
                        self.show_help = not self.show_help
                        continue
            clock.tick(60)


def run_undirected_graph_visualizer():
    UndirectedGraphVisualizer().run()

if __name__ == "__main__":
    run_undirected_graph_visualizer() 