import pygame
import sys
import string
from core.graph.graph import Graph
from core.graph.algorithms.topo_sort import topo_sort
from core.graph.algorithms.bellman_ford import bellman_ford

WIDTH, HEIGHT = 1200, 800
NODE_RADIUS = 32
NODE_COLOR = (100, 149, 237)
NODE_SELECTED_COLOR = (255, 140, 0)
EDGE_COLOR = (60, 60, 60)
EDGE_SELECTED_COLOR = (200, 60, 60)
TEXT_COLOR = (0, 0, 0)
BG_COLOR = (245, 245, 245)
INSTR_COLOR = (10, 30, 120)
ERROR_COLOR = (200, 40, 40)
FONT_SIZE = 28

class VisualNode:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.selected = False

class VisualEdge:
    def __init__(self, u, v, weight=1):
        self.u = u
        self.v = v
        self.weight = weight
        self.selected = False

class GraphVisualizer:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Directed Graph Visualizer")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=True)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.dragging = False
        self.drag_start = None
        self.selected_edge = None
        self.message = "Click to add node | Drag to add edge | Del: delete | T: TopoSort | B: Bellman-Ford | R: Reset | Q: Quit"
        self.error_msg = ''
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.bf_source = None
        self.awaiting_bf_source = False

    def reset(self):
        self.nodes = []
        self.edges = []
        self.graph = Graph(directed=True)
        self.node_labels = iter(string.ascii_uppercase)
        self.selected_node = None
        self.selected_edge = None
        self.dragging = False
        self.drag_start = None
        self.message = "Click to add node | Drag to add edge | Del: delete | T: TopoSort | B: Bellman-Ford | R: Reset | Q: Quit"
        self.error_msg = ''
        self.animating = False
        self.animation_steps = []
        self.animation_index = 0
        self.bf_source = None
        self.awaiting_bf_source = False

    def add_node(self, pos):
        try:
            label = next(self.node_labels)
        except StopIteration:
            self.error_msg = "Max 26 nodes (A-Z) supported."
            return
        self.nodes.append(VisualNode(label, pos))
        self.graph.adj[label] = []

    def get_node_at_pos(self, pos):
        for node in self.nodes:
            if (node.pos[0] - pos[0]) ** 2 + (node.pos[1] - pos[1]) ** 2 <= NODE_RADIUS ** 2:
                return node
        return None

    def add_edge(self, u, v, weight=1):
        if u == v:
            self.error_msg = "No self-loops allowed."
            return
        for edge in self.edges:
            if edge.u == u and edge.v == v:
                self.error_msg = "Edge already exists."
                return
        self.edges.append(VisualEdge(u, v, weight))
        self.graph.add_edge(u.label, v.label, weight)

    def get_edge_at_pos(self, pos):
        for edge in self.edges:
            ux, uy = edge.u.pos
            vx, vy = edge.v.pos
            # Midpoint of edge
            mx, my = (ux + vx) / 2, (uy + vy) / 2
            if (mx - pos[0]) ** 2 + (my - pos[1]) ** 2 <= (NODE_RADIUS // 2) ** 2:
                return edge
        return None

    def delete_selected(self):
        if self.selected_node:
            # Remove edges connected to node
            self.edges = [e for e in self.edges if e.u != self.selected_node and e.v != self.selected_node]
            if self.selected_node.label in self.graph.adj:
                del self.graph.adj[self.selected_node.label]
            for adj in self.graph.adj.values():
                adj[:] = [pair for pair in adj if pair[0] != self.selected_node.label]
            self.nodes.remove(self.selected_node)
            self.selected_node = None
        elif self.selected_edge:
            self.edges.remove(self.selected_edge)
            # Remove from graph
            u, v = self.selected_edge.u.label, self.selected_edge.v.label
            self.graph.adj[u] = [pair for pair in self.graph.adj[u] if pair[0] != v]
            self.selected_edge = None

    def draw(self):
        self.win.fill(BG_COLOR)
        # Draw edges
        for edge in self.edges:
            color = EDGE_SELECTED_COLOR if edge.selected else EDGE_COLOR
            self.draw_arrow(edge.u.pos, edge.v.pos, color, edge.weight)
        # Draw nodes
        for node in self.nodes:
            color = NODE_SELECTED_COLOR if node.selected else NODE_COLOR
            pygame.draw.circle(self.win, color, node.pos, NODE_RADIUS)
            pygame.draw.circle(self.win, (0,0,0), node.pos, NODE_RADIUS, 2)
            label_surf = self.font.render(node.label, True, TEXT_COLOR)
            rect = label_surf.get_rect(center=node.pos)
            self.win.blit(label_surf, rect)
        # Draw dragging edge
        if self.dragging and self.drag_start:
            pygame.draw.line(self.win, (120,120,120), self.drag_start.pos, pygame.mouse.get_pos(), 3)
        # Draw messages
        self.show_message(self.message, INSTR_COLOR, y_abs=HEIGHT-60)
        if self.error_msg:
            self.show_message(self.error_msg, ERROR_COLOR, y_abs=HEIGHT-30)
        pygame.display.update()

    def draw_arrow(self, start, end, color, weight=1):
        # Draw line
        pygame.draw.line(self.win, color, start, end, 5)
        # Draw arrowhead
        import math
        dx, dy = end[0] - start[0], end[1] - start[1]
        angle = math.atan2(dy, dx)
        length = NODE_RADIUS
        arrow_size = 18
        x1 = end[0] - length * math.cos(angle)
        y1 = end[1] - length * math.sin(angle)
        for offset in [-0.3, 0.3]:
            x2 = x1 - arrow_size * math.cos(angle + offset)
            y2 = y1 - arrow_size * math.sin(angle + offset)
            pygame.draw.line(self.win, color, (x1, y1), (x2, y2), 5)
        # Draw weight
        if weight != 1:
            mx, my = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
            wsurf = self.font.render(str(weight), True, (80,0,0))
            self.win.blit(wsurf, (mx, my))

    def show_message(self, msg, color, y_abs):
        surf = self.font.render(msg, True, color)
        rect = surf.get_rect(center=(WIDTH//2, y_abs))
        self.win.blit(surf, rect)

    def animate_toposort(self, order, cycle):
        self.animating = True
        self.animation_steps = order
        self.animation_index = 0
        self.error_msg = "Cycle detected! No topological order." if cycle else ""
        while self.animating and self.animation_index < len(self.animation_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            # Highlight current node
            for node in self.nodes:
                node.selected = (node.label == self.animation_steps[self.animation_index])
            self.draw()
            pygame.time.delay(600)
            self.animation_index += 1
        for node in self.nodes:
            node.selected = False
        self.animating = False
        self.draw()
        if not cycle:
            self.error_msg = "TopoSort order: " + "  " + " ".join(order)

    def animate_bellman_ford(self, dist, negative_cycle):
        self.animating = True
        self.animation_steps = list(dist.items())
        self.animation_index = 0
        self.error_msg = "Negative weight cycle detected!" if negative_cycle else ""
        while self.animating and self.animation_index < len(self.animation_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            # Highlight current node
            for node in self.nodes:
                node.selected = (node.label == self.animation_steps[self.animation_index][0])
            self.draw()
            pygame.time.delay(600)
            self.animation_index += 1
        for node in self.nodes:
            node.selected = False
        self.animating = False
        self.draw()
        if not negative_cycle:
            msg = "Shortest distances: " + ", ".join(f"{k}:{v if v!=float('inf') else '∞'}" for k,v in dist.items())
            self.error_msg = msg

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        node = self.get_node_at_pos(event.pos)
                        if node:
                            self.selected_node = node
                            node.selected = True
                            self.dragging = True
                            self.drag_start = node
                        else:
                            self.add_node(event.pos)
                    elif event.button == 3:  # Right click
                        edge = self.get_edge_at_pos(event.pos)
                        if edge:
                            self.selected_edge = edge
                            edge.selected = True
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
                elif event.type == pygame.KEYDOWN:
                    self.error_msg = ''
                    if event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.delete_selected()
                    elif event.key == pygame.K_t:
                        # Topological Sort
                        order = topo_sort(self.graph)
                        cycle = (len(order) != len(self.nodes))
                        self.animate_toposort(order, cycle)
                    elif event.key == pygame.K_b:
                        # Bellman-Ford
                        if not self.awaiting_bf_source:
                            self.message = "Type source node label (A-Z) and press Enter:"
                            self.awaiting_bf_source = True
                            self.bf_source = ''
                    elif self.awaiting_bf_source:
                        if event.key == pygame.K_RETURN:
                            src = self.bf_source.upper()
                            if src in [n.label for n in self.nodes]:
                                dist = bellman_ford(self.graph, src)
                                negative_cycle = (dist is None)
                                if negative_cycle:
                                    dist = {n.label: float('inf') for n in self.nodes}
                                self.animate_bellman_ford(dist, negative_cycle)
                                self.awaiting_bf_source = False
                                self.message = "Click to add node | Drag to add edge | Del: delete | T: TopoSort | B: Bellman-Ford | R: Reset | Q: Quit"
                            else:
                                self.error_msg = f"Node '{src}' does not exist."
                                self.bf_source = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.bf_source = self.bf_source[:-1]
                        elif event.unicode.isalpha():
                            self.bf_source += event.unicode.upper()


def run_graph_visualizer():
    GraphVisualizer().run()

if __name__ == "__main__":
    run_graph_visualizer() 