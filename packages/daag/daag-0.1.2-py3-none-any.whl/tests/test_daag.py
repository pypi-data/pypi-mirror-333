"""
Tests for the DAAG package.
"""

import unittest
from daag import DAAG


class TestDAAG(unittest.TestCase):
    """Test cases for the DAAG class."""

    def setUp(self):
        """Set up a simple graph for testing."""
        self.graph = DAAG()

        # Create a diamond pattern
        self.graph.add_vertex("A", 1)
        self.graph.add_vertex("B", 2)
        self.graph.add_vertex("C", 2)
        self.graph.add_vertex("D", 3)

        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("C", "D")

    def test_vertices_by_layer(self):
        """Test the get_vertices_by_layer method."""
        layers = self.graph.get_vertices_by_layer()
        self.assertEqual(set(layers[1]), {"A"})
        self.assertEqual(set(layers[2]), {"B", "C"})
        self.assertEqual(set(layers[3]), {"D"})

    def test_adjacency_property(self):
        """Test that the adjacency property is enforced."""
        self.assertTrue(self.graph.verify_adjacency_property())

        # Try to add an edge that violates adjacency property
        with self.assertRaises(ValueError):
            self.graph.add_edge("A", "D")  # Cannot connect layer 1 to layer 3

    def test_acyclic_property(self):
        """Test that cycles are not allowed."""
        # Add new vertices that could form a cycle
        self.graph.add_vertex("E", 4)
        self.graph.add_vertex("F", 5)

        # Add edges to these new vertices
        self.graph.add_edge("D", "E")
        self.graph.add_edge("E", "F")

        # Try to create a cycle (F -> A) - should fail because
        # it would violate the adjacency property
        with self.assertRaises(ValueError):
            self.graph.add_edge("F", "A")

    def test_duplicate_vertex(self):
        """Test that duplicate vertices are not allowed."""
        with self.assertRaises(ValueError):
            self.graph.add_vertex("A", 1)  # A already exists

    def test_duplicate_edge(self):
        """Test that duplicate edges are not allowed."""
        with self.assertRaises(ValueError):
            self.graph.add_edge("A", "B")  # Edge already exists

    def test_nonexistent_vertex_edge(self):
        """Test handling of edges with nonexistent vertices."""
        with self.assertRaises(ValueError):
            self.graph.add_edge("A", "Z")  # Z doesn't exist

        with self.assertRaises(ValueError):
            self.graph.add_edge("Z", "A")  # Z doesn't exist

    def test_networkx_conversion(self):
        """Test conversion to NetworkX graph."""
        nx_graph = self.graph.to_networkx()

        # Check nodes
        self.assertEqual(set(nx_graph.nodes()), {"A", "B", "C", "D"})

        # Check edges
        expected_edges = {("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")}
        self.assertEqual(set(nx_graph.edges()), expected_edges)

        # Check node attributes (layer)
        self.assertEqual(nx_graph.nodes["A"]["layer"], 1)
        self.assertEqual(nx_graph.nodes["B"]["layer"], 2)
        self.assertEqual(nx_graph.nodes["C"]["layer"], 2)
        self.assertEqual(nx_graph.nodes["D"]["layer"], 3)


if __name__ == "__main__":
    unittest.main()
