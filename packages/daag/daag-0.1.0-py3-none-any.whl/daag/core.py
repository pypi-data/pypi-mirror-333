"""
Core implementation of the Directed Acyclic Adjacency Graph (DAAG).
"""

import os


class DAAG:
    """
    Directed Acyclic Adjacency Graph (DAAG)
    
    A graph data structure where:
    1. Edges are directed (flow in one direction)
    2. No cycles are allowed (acyclic)
    3. Edges can only connect vertices in adjacent layers
    """

    def __init__(self):
        """Initialize an empty DAAG."""
        self.vertices = {
        }  # {vertex_id: {"layer": layer, "data": data, "out_edges": [], "in_edges": []}}
        self.edges = []  # List of (from_id, to_id) pairs

    def add_vertex(self, vertex_id, layer, data=None):
        """
        Add a vertex to the graph.
        
        Args:
            vertex_id: Unique identifier for the vertex
            layer: The layer/tier this vertex belongs to (1-indexed)
            data: Optional data to associate with the vertex
            
        Returns:
            The vertex record
        """
        if vertex_id in self.vertices:
            raise ValueError(f"Vertex with ID {vertex_id} already exists")

        if not isinstance(layer, int) or layer < 1:
            raise ValueError("Layer must be a positive integer")

        vertex = {
            "layer": layer,
            "data": data or {},
            "out_edges": [],
            "in_edges": []
        }

        self.vertices[vertex_id] = vertex
        return vertex

    def add_edge(self, from_id, to_id):
        """
        Add an edge between two vertices, enforcing the adjacency property.
        
        Args:
            from_id: ID of the source vertex
            to_id: ID of the target vertex
            
        Returns:
            True if edge was added successfully
        """
        # Verify vertices exist
        if from_id not in self.vertices:
            raise ValueError(f"Source vertex {from_id} does not exist")
        if to_id not in self.vertices:
            raise ValueError(f"Target vertex {to_id} does not exist")

        from_vertex = self.vertices[from_id]
        to_vertex = self.vertices[to_id]

        # Check adjacency property (layers must be adjacent)
        if to_vertex["layer"] != from_vertex["layer"] + 1:
            raise ValueError(
                f"Edge violates adjacency property: {from_id} (layer {from_vertex['layer']}) -> "
                f"{to_id} (layer {to_vertex['layer']})")

        # Check for existing edge
        if to_id in from_vertex["out_edges"]:
            raise ValueError(f"Edge from {from_id} to {to_id} already exists")

        # Add edge
        edge = (from_id, to_id)
        self.edges.append(edge)
        from_vertex["out_edges"].append(to_id)
        to_vertex["in_edges"].append(from_id)

        return True

    def verify_adjacency_property(self):
        """
        Verify that all edges in the graph satisfy the adjacency property.
        
        Returns:
            True if all edges connect vertices in adjacent layers
        """
        for from_id, to_id in self.edges:
            from_layer = self.vertices[from_id]["layer"]
            to_layer = self.vertices[to_id]["layer"]

            if to_layer != from_layer + 1:
                return False

        return True

    def get_vertices_by_layer(self):
        """
        Get vertices grouped by their layer.
        
        Returns:
            Dictionary mapping layer numbers to lists of vertex IDs
        """
        layers = {}
        for vertex_id, vertex in self.vertices.items():
            layer = vertex["layer"]
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(vertex_id)

        return layers

    def to_networkx(self):
        """
        Convert the DAAG to a NetworkX DiGraph for visualization.
        
        Returns:
            A NetworkX DiGraph representation of the DAAG
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError("NetworkX is required for this functionality. "
                              "Install it with: pip install networkx")

        G = nx.DiGraph()

        # Add all vertices with their layer information
        for vertex_id, vertex in self.vertices.items():
            G.add_node(vertex_id, layer=vertex["layer"], **vertex["data"])

        # Add all edges
        for from_id, to_id in self.edges:
            G.add_edge(from_id, to_id)

        return G

    def visualize(self,
                  filename=None,
                  figsize=(10, 8),
                  node_size=1500,
                  node_color='skyblue',
                  edge_color='black',
                  title="Directed Acyclic Adjacency Graph"):
        """
        Visualize the graph using NetworkX and Matplotlib.
        
        Args:
            filename: Optional filename to save the visualization as (e.g. 'graph.png')
            figsize: Size of the figure (width, height) in inches
            node_size: Size of nodes in the visualization
            node_color: Color of nodes
            edge_color: Color of edges
            title: Title of the visualization
        
        Returns:
            The matplotlib figure and axes objects
        """
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "NetworkX and Matplotlib are required for visualization. "
                "Install them with: pip install networkx matplotlib")

        # Convert to NetworkX graph
        G = self.to_networkx()

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Determine layout based on layers (hierarchical)
        layers = self.get_vertices_by_layer()
        max_layer = max(layers.keys()) if layers else 0

        # Create position dictionary for hierarchical layout
        pos = {}
        for layer_num, vertices in layers.items():
            # Normalize y-coordinate (top to bottom)
            y = 1 - (layer_num - 1) / max(1, max_layer - 1)

            # Distribute vertices horizontally
            num_vertices = len(vertices)
            for i, v_id in enumerate(sorted(vertices)):
                x = (i + 0.5) / max(1, num_vertices)
                pos[v_id] = (x, y)

        # Draw the graph
        nx.draw_networkx(G,
                         pos,
                         ax=ax,
                         node_size=node_size,
                         node_color=node_color,
                         edge_color=edge_color,
                         arrows=True,
                         with_labels=True,
                         font_weight='bold')

        # Set title and disable axis
        ax.set_title(title)
        ax.axis('off')

        # Save if filename provided
        if filename:
            plt.savefig(filename, bbox_inches='tight')

        plt.tight_layout()
        return fig, ax

    def visualize_subgraphs(self,
                            directory="subgraphs",
                            figsize=(8, 6),
                            node_size=1200):
        """
        Visualize individual subgraphs for each terminal node.
        A terminal node is defined as a node that has no outgoing edges.
        
        Args:
            directory: Directory to save the visualizations
            figsize: Size of the figure (width, height) in inches
            node_size: Size of nodes in the visualization
            
        Returns:
            Dictionary mapping terminal vertex IDs to their figures
        """
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            import os
        except ImportError:
            raise ImportError(
                "NetworkX and Matplotlib are required for visualization. "
                "Install them with: pip install networkx matplotlib")

        # Create output directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Find all terminal nodes (nodes with no outgoing edges)
        terminal_nodes = [
            vid for vid, v in self.vertices.items() if not v["out_edges"]
        ]

        if not terminal_nodes:
            print("No terminal nodes found in the graph.")
            return {}

        # For each terminal node, build and visualize its subgraph
        figures = {}

        for terminal_id in terminal_nodes:
            # Create an empty set for tracking nodes in this subgraph
            subgraph_nodes = set()

            # Helper function to recursively find all ancestors
            def add_ancestors(node_id):
                subgraph_nodes.add(node_id)
                for parent_id in self.vertices[node_id]["in_edges"]:
                    if parent_id not in subgraph_nodes:
                        add_ancestors(parent_id)

            # Build the subgraph by finding all ancestors of the terminal node
            add_ancestors(terminal_id)

            # Create NetworkX subgraph
            G = self.to_networkx().subgraph(subgraph_nodes)

            # Create a title for the subgraph
            title = f"Subgraph leading to {terminal_id}"

            # Create figure
            fig, ax = plt.subplots(figsize=figsize)

            # Determine layout based on layers
            pos = {}

            # Group nodes by layer
            layers_dict = {}
            for node_id in subgraph_nodes:
                layer = self.vertices[node_id]["layer"]
                if layer not in layers_dict:
                    layers_dict[layer] = []
                layers_dict[layer].append(node_id)

            max_layer = max(layers_dict.keys()) if layers_dict else 0

            # Position nodes according to their layer
            for layer_num, vertices in layers_dict.items():
                # Normalize y-coordinate (top to bottom)
                y = 1 - (layer_num - 1) / max(1, max_layer - 1)

                # Distribute vertices horizontally
                num_vertices = len(vertices)
                for i, v_id in enumerate(sorted(vertices)):
                    x = (i + 0.5) / max(1, num_vertices)
                    pos[v_id] = (x, y)

            # Highlight the terminal node with a different color
            node_colors = [
                '#FF9999' if node == terminal_id else '#9999FF'
                for node in G.nodes()
            ]

            # Draw the subgraph
            nx.draw_networkx(G,
                             pos,
                             ax=ax,
                             node_size=node_size,
                             node_color=node_colors,
                             arrows=True,
                             with_labels=True,
                             font_weight='bold')

            # Set title and disable axis
            ax.set_title(title)
            ax.axis('off')

            # Save the figure
            filename = os.path.join(directory, f"subgraph_{terminal_id}.png")
            plt.savefig(filename, bbox_inches='tight')

            figures[terminal_id] = fig

            print(
                f"Saved subgraph for terminal node {terminal_id} to {filename}"
            )

        return figures
