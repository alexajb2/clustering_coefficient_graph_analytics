import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Set, Dict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QComboBox, QPushButton, QLabel, QWidget, QMessageBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

# Import your existing graph requirements (assumed to be in requirements.py)
from requirements import Graph, get_diameter, get_clustering_coefficient, get_degree_distribution

class ModernGraphViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Visualization Explorer")
        self.resize(1000, 800)
        
        # Set up a modern, dark color scheme
        self.setup_dark_theme()
        
        # Prepare the main container
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)
        
        # Top control section
        top_controls = QHBoxLayout()
        
        # Graph selection dropdown
        self.graph_selector = QComboBox()
        self.graph_selector.setFont(QFont("Segoe UI", 10))
        top_controls.addWidget(self.graph_selector)
        
        # Save button
        save_btn = QPushButton("Save Graph")
        save_btn.setFont(QFont("Segoe UI", 10))
        save_btn.clicked.connect(self.save_graph)
        top_controls.addWidget(save_btn)
        
        main_layout.addLayout(top_controls)
        
        # Info display
        self.info_label = QLabel("Graph Information")
        self.info_label.setFont(QFont("Segoe UI", 10))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.info_label)
        
        # Matplotlib integration for graph visualization
        self.figure, (self.ax_graph, self.ax_info) = plt.subplots(
            2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [3, 1]},
            facecolor='#2C3E50'
        )
        self.canvas = plt.gcf().canvas
        self.canvas.draw()
        
        # Add matplotlib canvas to layout
        main_layout.addWidget(self.canvas)
        
        # Prepare graphs
        self.prepare_test_graphs()
        
        # Populate dropdown
        self.graph_selector.addItems([g["description"] for g in self.graphs])
        self.graph_selector.currentIndexChanged.connect(self.show_graph)
        
        # Initial graph display
        self.show_graph(0)
    
    def setup_dark_theme(self):
        """Apply a dark theme to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QComboBox, QPushButton {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #7F8C8D;
                padding: 5px;
                border-radius: 4px;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 12px;
            }
        """)
    
    def prepare_test_graphs(self):
        """Prepare test graphs similar to the original implementation."""
        test_graphs = [
            (0, set(), "Empty Graph"),
            (1, set(), "Single Node Graph"),
            (2, set(), "Two Nodes, No Edges"),
            (2, {(0, 1)}, "Two Nodes, One Edge"),
            (3, set(), "Three Nodes, No Edges"),
            (3, {(0, 1), (1, 2)}, "Path Graph of 3 Nodes"),
            (3, {(0, 1), (1, 2), (0, 2)}, "Triangle Graph"),
            (10, {(0, 3), (0, 7), (1, 4), (1, 5), (1, 6), (2, 3), (2, 7),
                  (3, 4), (3, 8), (3, 9), (4, 5), (4, 9), (5, 6), (8, 9)},
             "Graph from Algorithm Tests")
        ]
        
        # Create a larger random graph
        num_nodes_large = 50
        edges_large = set()
        random.seed(42)
        while len(edges_large) < 100:
            u, v = random.sample(range(num_nodes_large), 2)
            edge = (min(u, v), max(u, v))
            edges_large.add(edge)
        
        test_graphs.append(
            (num_nodes_large, edges_large, "Large Random Graph (50 Nodes, 100 Edges)")
        )
        
        # Compute graph properties
        self.graphs = []
        for num_nodes, edges, description in test_graphs:
            g_obj = Graph(num_nodes, edges)
            info = {
                "description": description,
                "num_nodes": num_nodes,
                "edges": edges,
                "graph_obj": g_obj,
                "diameter": get_diameter(g_obj),
                "clustering": get_clustering_coefficient(g_obj),
                "degree_distribution": get_degree_distribution(g_obj)
            }
            self.graphs.append(info)
    
    def convert_to_networkx(self, graph_obj):
        """Convert our custom Graph object to a networkx Graph."""
        G = nx.Graph()
        G.add_nodes_from(range(graph_obj.get_num_nodes()))
        for edge in graph_obj.edges:
            G.add_edge(*edge)
        return G
    
    def show_graph(self, index):
        """Display the selected graph."""
        current_info = self.graphs[index]
        g_obj = current_info["graph_obj"]
        
        # Clear previous plots
        self.ax_graph.clear()
        self.ax_info.clear()
        
        # Convert to networkx and draw
        G = self.convert_to_networkx(g_obj)
        pos = nx.spring_layout(G, seed=42)
        
        # Modern color scheme
        nx.draw_networkx_nodes(G, pos, ax=self.ax_graph, 
                                node_color='#3498DB',  # Bright blue nodes
                                node_size=300)
        nx.draw_networkx_edges(G, pos, ax=self.ax_graph, 
                                edge_color='#2ECC71',  # Green edges
                                width=1.5, 
                                alpha=0.7)
        nx.draw_networkx_labels(G, pos, ax=self.ax_graph, 
                                 font_color='white', 
                                 font_weight='bold')
        
        self.ax_graph.set_title(current_info["description"], color='#ECF0F1')
        self.ax_graph.set_facecolor('#2C3E50')
        self.ax_graph.figure.patch.set_facecolor('#2C3E50')
        self.ax_graph.axis('off')
        
        # Prepare info text
        info_text = (
            f"Description: {current_info['description']}\n"
            f"Nodes: {current_info['num_nodes']}\n"
            f"Edges: {len(current_info['edges'])}\n"
            f"Diameter: {current_info['diameter']}\n"
            f"Clustering Coefficient: {current_info['clustering']:.2f}\n"
            f"Degree Distribution: {current_info['degree_distribution']}"
        )
        
        # Display info text in the second subplot
        self.ax_info.text(0.5, 0.5, info_text, 
                           horizontalalignment='center', 
                           verticalalignment='center',
                           fontsize=10, 
                           color='#ECF0F1')
        self.ax_info.axis('off')
        self.ax_info.set_facecolor('#2C3E50')
        
        # Adjust layout and redraw canvas
        plt.tight_layout()
        self.canvas.draw()
        
        # Update info label in the UI
        html_info_text = (
            f"<b>Description:</b> {current_info['description']}<br>"
            f"<b>Nodes:</b> {current_info['num_nodes']}<br>"
            f"<b>Edges:</b> {len(current_info['edges'])}<br>"
            f"<b>Diameter:</b> {current_info['diameter']}<br>"
            f"<b>Clustering Coefficient:</b> {current_info['clustering']:.2f}<br>"
            f"<b>Degree Distribution:</b> {current_info['degree_distribution']}"
        )
        self.info_label.setText(html_info_text)
    
    def save_graph(self):
        """Save the current graph as an image."""
        try:
            current_info = self.graphs[self.graph_selector.currentIndex()]
            filename = f"{current_info['description'].replace(' ', '_')}.png"
            
            # Use the figure that already has both graph and info
            plt.savefig(filename, 
                        facecolor='#2C3E50', 
                        edgecolor='none', 
                        bbox_inches='tight')
            QMessageBox.information(self, "Save Successful", f"Graph saved as {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Save Error", str(e))

def main():
    app = QApplication(sys.argv)
    viewer = ModernGraphViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()