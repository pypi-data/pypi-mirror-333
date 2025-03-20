# DAAG: Directed Acyclic Adjacency Graph

A specialized graph data structure for representing layered dependencies with adjacency constraints.

## Overview

The Directed Acyclic Adjacency Graph (DAAG) is a graph structure with the following properties:

1. **Directed**: Edges flow in one direction
2. **Acyclic**: No cycles are allowed
3. **Adjacency constraint**: Edges can only connect vertices in adjacent layers

This makes DAAG particularly useful for modeling dependencies where:

- Elements are organized in distinct layers/tiers
- Dependencies can only exist between adjacent layers
- No circular dependencies are allowed

## Features

- Easy creation and manipulation of layered graph structures
- Automatic enforcement of adjacency constraints
- Visualization tools for the full graph and individual subgraphs
- Interactive filtering to explore complex dependency trees

## Basic Usage

```python
from daag import DAAG

# Create a new DAAG
graph = DAAG()

# Add vertices with their respective layers
graph.add_vertex("A", 1)  # Layer 1
graph.add_vertex("B", 2)  # Layer 2
graph.add_vertex("C", 2)  # Also Layer 2
graph.add_vertex("D", 3)  # Layer 3

# Add edges (only allowed between adjacent layers)
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")

# Visualize the graph
graph.visualize(filename="my_graph.png")

# Visualize subgraphs for each terminal node
graph.visualize_subgraphs(directory="subgraphs")

# Interactive visualization with filtering
from daag import simple_subgraph_filtering
simple_subgraph_filtering(graph)
```

## Installation

```
pip install daag
```

## Requirements

- NetworkX
- Matplotlib

## Documentation

For detailed documentation, see the [full technical documentation](./daag_technical_doc.pdf).
