"""
Visualization utilities for DAAG.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button


def simple_subgraph_filtering(graph):
    """
    Creates a simple filtering interface with subgraph checkboxes and select all/clear all buttons.
    All subgraphs are selected by default.
    
    Args:
        graph: A DAAG instance to visualize
    """
    # Import here to avoid circular imports
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("NetworkX is required for this functionality. "
                          "Install it with: pip install networkx")

    # Find all terminal nodes
    terminal_nodes = [
        vid for vid, v in graph.vertices.items() if not v["out_edges"]
    ]
    terminal_nodes.sort()

    if not terminal_nodes:
        print(
            "No terminal nodes found in the graph. Cannot create filtering interface."
        )
        return

    # Convert to NetworkX graph
    G_full = graph.to_networkx()

    # Calculate positions
    layers = graph.get_vertices_by_layer()
    max_layer = max(layers.keys()) if layers else 0

    pos = {}
    for layer_num, vertices in layers.items():
        y = 1 - (layer_num - 1) / max(1, max_layer - 1)
        num_vertices = len(vertices)
        for i, v_id in enumerate(sorted(vertices)):
            x = (i + 0.5) / max(1, num_vertices)
            pos[v_id] = (x, y)

    # Dictionary to hold subgraph nodes for each terminal node
    subgraph_nodes = {}
    for terminal_id in terminal_nodes:
        nodes = set()

        def add_ancestors(node_id):
            nodes.add(node_id)
            for parent_id in graph.vertices[node_id]["in_edges"]:
                if parent_id not in nodes:
                    add_ancestors(parent_id)

        add_ancestors(terminal_id)
        subgraph_nodes[terminal_id] = nodes

    # Create figure
    fig = plt.figure(figsize=(15, 10))
    main_ax = plt.axes([0.2, 0.1, 0.75, 0.8])

    # Initial state: all selected
    selected = {node: True for node in terminal_nodes}

    def draw_graph():
        main_ax.clear()

        # Get all selected terminals
        active_terminals = [node for node in terminal_nodes if selected[node]]

        if not active_terminals:
            main_ax.text(0.5,
                         0.5,
                         "No nodes selected",
                         ha='center',
                         va='center',
                         fontsize=14)
            main_ax.axis('off')
            fig.canvas.draw_idle()
            return

        # Collect nodes to show
        nodes_to_show = set()
        for terminal in active_terminals:
            nodes_to_show.update(subgraph_nodes[terminal])

        # Create subgraph
        G_sub = G_full.subgraph(nodes_to_show)

        # Highlight terminal nodes
        node_colors = [
            '#FF9999' if node in active_terminals else '#9999FF'
            for node in G_sub.nodes()
        ]

        # Draw graph
        nx.draw_networkx(G_sub,
                         pos,
                         ax=main_ax,
                         node_size=800,
                         node_color=node_colors,
                         arrows=True,
                         with_labels=True,
                         font_weight='bold')

        main_ax.set_title(
            f"Selected terminal nodes: {', '.join(active_terminals)}")
        main_ax.axis('off')
        fig.canvas.draw_idle()

    # Create checkboxes - we'll handle changes manually
    rax = plt.axes([0.02, 0.3, 0.15, 0.6])
    rax.set_title("Terminal Nodes")
    check = CheckButtons(rax, terminal_nodes, [True for _ in terminal_nodes])

    select_all_ax = plt.axes([0.05, 0.2, 0.1, 0.05])
    select_all_button = Button(select_all_ax, 'Select All')

    clear_all_ax = plt.axes([0.05, 0.1, 0.1, 0.05])
    clear_all_button = Button(clear_all_ax, 'Clear All')

    def node_clicked(label):
        # Instead of toggling, explicitly set based on the checkbox state
        # Find the index of this label
        idx = terminal_nodes.index(label)
        # Get the current checkbox state
        is_checked = check.get_status()[idx]
        # Set our tracking to match
        selected[label] = is_checked
        # Redraw
        draw_graph()

    def select_all_clicked(event):
        # Select all nodes
        for node in terminal_nodes:
            selected[node] = True

        # Update checkboxes
        for i, label in enumerate(terminal_nodes):
            if not check.get_status()[i]:
                check.set_active(i)

        draw_graph()

    def clear_all_clicked(event):
        # First, update our internal tracking of selected nodes
        for node in terminal_nodes:
            selected[node] = False

        # Then manually ensure all checkboxes are unchecked
        for i, label in enumerate(terminal_nodes):
            # Only toggle if it's currently checked
            if check.get_status()[i]:
                check.set_active(i)

        # Force a complete redraw
        main_ax.clear()
        main_ax.text(0.5,
                     0.5,
                     "No nodes selected",
                     ha='center',
                     va='center',
                     fontsize=14)
        main_ax.axis('off')
        fig.canvas.draw_idle()

    #
