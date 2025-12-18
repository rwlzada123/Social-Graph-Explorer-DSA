from typing import Dict, List
from .graph import Graph

def dfs_iterative(graph: Graph, start_user: str) -> List[str]:
    if not graph.has_user(start_user):
        return []

    start_id = graph.get_user_id(start_user)
    
    stack = [start_id]
    visited = set()
    order_ids = []

    get_neighbors = graph.get_neighbors
    get_name = graph.get_user_name

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            order_ids.append(u)

            neighbors = sorted(get_neighbors(u), key=get_name, reverse=True)
            for v in neighbors:
                if v not in visited:
                    stack.append(v)

    return [get_name(n) for n in order_ids]