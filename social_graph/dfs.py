from typing import Dict, List, Optional, Any
from time import perf_counter
from .graph import Graph


# =====================================================================
# DFSResult: structured data container
# =====================================================================
class DFSResult:
    def __init__(
        self,
        order: List[str],
        parent: Dict[str, Optional[str]],
        depth: Dict[str, int],
        tin: Dict[str, int],
        tout: Dict[str, int],
        time_ms: float = 0.0
    ):
        self.order = order
        self.parent = parent
        self.depth = depth
        self.tin = tin
        self.tout = tout
        self.time_ms = time_ms


# =====================================================================
# MAIN DFS TRAVERSAL (Tree + timestamps)
# =====================================================================
def dfs_traversal(graph: Graph, start_user: str, return_full: bool = True):

    start_time = perf_counter()

    if not graph.has_user(start_user):
        return DFSResult([], {}, {}, {}, {}, 0) if return_full else []

    start_id = graph.get_user_id(start_user)

    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    visited = set()
    parent = {start_id: None}
    depth = {}
    order_ids = []

    tin, tout = {}, {}
    timer = [1]

    def dfs(u, d):
        visited.add(u)
        depth[u] = d
        order_ids.append(u)
        tin[u] = timer[0]
        timer[0] += 1

        for v in sorted(get_neighbors(u), key=get_name):
            if v not in visited:
                parent[v] = u
                dfs(v, d + 1)

        tout[u] = timer[0]
        timer[0] += 1

    dfs(start_id, 0)

    order_names = [get_name(n) for n in order_ids]
    parent_named = {get_name(k): (None if v is None else get_name(v)) for k, v in parent.items()}
    depth_named = {get_name(k): v for k, v in depth.items()}
    tin_named = {get_name(k): v for k, v in tin.items()}
    tout_named = {get_name(k): v for k, v in tout.items()}

    elapsed = (perf_counter() - start_time) * 1000

    return DFSResult(order_names, parent_named, depth_named, tin_named, tout_named, elapsed)


# =====================================================================
# DFS PATH FINDER (USED BY DFS WINDOW)
# =====================================================================
class DFSPathResult:
    def __init__(self, path, visited_order, distances):
        self.path = path
        self.visited_order = visited_order
        self.distances = distances


def dfs_shortest_path(graph, start_user, target_user, return_full_result=True):
    print(" dfs_shortest_path CALLED")

    if not graph.has_user(start_user) or not graph.has_user(target_user):
        return DFSPathResult([], [], {})

    start = graph.get_user_id(start_user)
    target = graph.get_user_id(target_user)

    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    visited = set()
    path = []
    all_paths = []  # store every valid path

    # Full DFS that finds ALL paths
    def dfs(u):
        visited.add(u)
        path.append(u)

        if u == target:
            all_paths.append(path.copy())
        else:
            for v in get_neighbors(u):
                if v not in visited:
                    dfs(v)

        # backtrack
        visited.remove(u)
        path.pop()

    # Run full DFS
    dfs(start)

    # If no path found
    if not all_paths:
        return DFSPathResult([], [], {})

    # Choose the SHORTEST path among all found
    shortest = min(all_paths, key=len)

    # Convert to names
    shortest_named = [get_name(n) for n in shortest]

    # visited_order for animation = shortest path only
    visited_order_named = shortest_named.copy()

    return DFSPathResult(shortest_named, visited_order_named, {})
