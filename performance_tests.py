# performance_tests.py

from social_graph.graph import Graph
from social_graph.bfs import bfs_shortest_path
from social_graph.dfs_iterative import dfs_iterative

from time import perf_counter
from random import randint, choice


def build_graph(n_users: int, edge_density: float = 0.01) -> Graph:
    g = Graph()

    # Add users
    for i in range(n_users):
        g.add_user(f"User_{i}")

    # Random friendships
    edges = int(n_users * n_users * edge_density)
    for _ in range(edges):
        u = f"User_{randint(0, n_users - 1)}"
        v = f"User_{randint(0, n_users - 1)}"
        if u != v:
            g.add_friendship(u, v)

    return g


def measure_avg_time(func, runs=3):
    total = 0
    for _ in range(runs):
        t0 = perf_counter()
        func()
        total += (perf_counter() - t0)
    return (total / runs) * 1000   # ms


def test_bfs(g: Graph):
    users = g.get_all_users()
    start = choice(users)
    end = choice(users)
    bfs_shortest_path(g, start, end, return_full_result=True)


def test_dfs(g: Graph):
    users = g.get_all_users()
    start = choice(users)
    dfs_iterative(g, start)


def run_benchmarks():
    sizes = [1000, 5000, 10000] 

    print("\n===== ALGORITHM RUNTIME BENCHMARKS =====\n")
    print("Sizes tested: ", sizes)
    print("Values reported in milliseconds (ms)\n")

    for size in sizes:
        print(f"\n=== GRAPH SIZE: N = {size} USERS ===")

        g = build_graph(size)

        bfs_time = measure_avg_time(lambda: test_bfs(g))
        dfs_time = measure_avg_time(lambda: test_dfs(g))

        print(f"Average BFS time: {bfs_time:.4f} ms")
        print(f"Average DFS time: {dfs_time:.4f} ms")


if __name__ == "__main__":
    run_benchmarks()