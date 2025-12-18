from social_graph.graph import Graph
from social_graph.bfs import bfs_shortest_path


def test_bfs_simple_path():
    g = Graph()
    g.add_user("A")
    g.add_user("B")
    g.add_user("C")

    g.add_friendship("A", "B")
    g.add_friendship("B", "C")

    result = bfs_shortest_path(g, "A", "C")
    assert result.path == ["A", "B", "C"]


def test_bfs_no_path():
    g = Graph()
    g.add_user("A")
    g.add_user("B")
    g.add_user("C")

    g.add_friendship("A", "B")

    result = bfs_shortest_path(g, "A", "C")
    assert result.path == []


def test_bfs_same_node():
    g = Graph()
    g.add_user("A")

    result = bfs_shortest_path(g, "A", "A")
    assert result.path == ["A"]
