"""
Example usage of the DAAG package.
This recreates the example from the original script.
"""

from daag import DAAG, simple_subgraph_filtering


def create_example_graph():
    """Create an example graph with multiple subgraph patterns."""
    # Create a new DAAG
    graph = DAAG()

    # ----- SIMPLE SUBGRAPH 1: Linear chain -----
    graph.add_vertex("A1", 1)
    graph.add_vertex("B1", 2)
    graph.add_vertex("C1", 3)

    graph.add_edge("A1", "B1")
    graph.add_edge("B1", "C1")

    # ----- SIMPLE SUBGRAPH 2: Diamond pattern -----
    graph.add_vertex("A2", 1)
    graph.add_vertex("B2", 2)
    graph.add_vertex("C2", 2)
    graph.add_vertex("D2", 3)

    graph.add_edge("A2", "B2")
    graph.add_edge("A2", "C2")
    graph.add_edge("B2", "D2")
    graph.add_edge("C2", "D2")

    # ----- SIMPLE SUBGRAPH 3: One-to-many-to-one -----
    graph.add_vertex("A3", 1)
    graph.add_vertex("B3", 2)
    graph.add_vertex("C3", 2)
    graph.add_vertex("D3", 2)
    graph.add_vertex("E3", 3)

    graph.add_edge("A3", "B3")
    graph.add_edge("A3", "C3")
    graph.add_edge("A3", "D3")
    graph.add_edge("B3", "E3")
    graph.add_edge("C3", "E3")
    graph.add_edge("D3", "E3")

    # ----- COMPLEX SUBGRAPH: Multiple interconnected paths -----
    # Layer 1 nodes
    graph.add_vertex("A4", 1)
    graph.add_vertex("B4", 1)
    graph.add_vertex("C4", 1)
    graph.add_vertex("D4", 1)
    graph.add_vertex("E4", 1)

    # Layer 2 nodes
    graph.add_vertex("F4", 2)
    graph.add_vertex("G4", 2)
    graph.add_vertex("H4", 2)
    graph.add_vertex("I4", 2)
    graph.add_vertex("J4", 2)
    graph.add_vertex("K4", 2)

    # Layer 3 nodes
    graph.add_vertex("L4", 3)
    graph.add_vertex("M4", 3)
    graph.add_vertex("N4", 3)

    # Layer 1 to Layer 2 connections
    graph.add_edge("A4", "F4")
    graph.add_edge("A4", "G4")
    graph.add_edge("B4", "F4")
    graph.add_edge("B4", "H4")
    graph.add_edge("C4", "G4")
    graph.add_edge("C4", "I4")
    graph.add_edge("D4", "I4")
    graph.add_edge("D4", "J4")
    graph.add_edge("E4", "J4")
    graph.add_edge("E4", "K4")

    # Layer 2 to Layer 3 connections
    graph.add_edge("F4", "L4")
    graph.add_edge("G4", "L4")
    graph.add_edge("G4", "M4")
    graph.add_edge("H4", "M4")
    graph.add_edge("I4", "M4")
    graph.add_edge("I4", "N4")
    graph.add_edge("J4", "N4")
    graph.add_edge("K4", "N4")

    # ----- SIMPLE SUBGRAPH 4: Y-pattern -----
    graph.add_vertex("A5", 1)
    graph.add_vertex("B5", 2)
    graph.add_vertex("C5", 3)
    graph.add_vertex("D5", 3)

    graph.add_edge("A5", "B5")
    graph.add_edge("B5", "C5")
    graph.add_edge("B5", "D5")

    # ----- SIMPLE SUBGRAPH 5: Two isolated paths -----
    graph.add_vertex("A6", 1)
    graph.add_vertex("B6", 1)
    graph.add_vertex("C6", 2)
    graph.add_vertex("D6", 2)
    graph.add_vertex("E6", 3)
    graph.add_vertex("F6", 3)

    graph.add_edge("A6", "C6")
    graph.add_edge("B6", "D6")
    graph.add_edge("C6", "E6")
    graph.add_edge("D6", "F6")

    return graph


if __name__ == "__main__":
    # Create the example graph
    graph = create_example_graph()

    # Use interactive visualization
    simple_subgraph_filtering(graph)
