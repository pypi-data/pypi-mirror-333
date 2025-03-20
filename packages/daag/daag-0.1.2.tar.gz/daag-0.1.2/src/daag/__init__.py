"""
DAAG: Directed Acyclic Adjacency Graph

A Python library for creating, visualizing, and manipulating Directed Acyclic Adjacency Graphs - 
specialized graphs where edges are directed, no cycles are allowed, 
and edges only connect vertices in adjacent layers.
"""

from .core import DAAG
from .visualization import simple_subgraph_filtering

__version__ = "0.1.2"
