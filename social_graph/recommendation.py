from collections import Counter
from typing import List, Tuple
from .graph import Graph

# Recommend friends based on mutual friends
def recommend_friends(graph: Graph, username: str, max_results: int = 5) -> List[Tuple[str, int]]:
    # Returns a list of tuples: [(recommended_user, mutual_friend_count)]

    if not graph.has_user(username):
        return[]
    
    # current friends of user
    direct_friends = set(graph.get_friends(username))

    # mutual friends
    mutual_counts: Counter[str] = Counter()

    for friend in direct_friends:
        friends_of_friend = graph.get_friends(friend)
        for canditate in friends_of_friend:
            if canditate == username:
                continue
            if canditate in direct_friends:
                continue
            mutual_counts[canditate] += 1

    # Sort by highest mutual friends, then alphabetically
    sorted_candidates = sorted(
        mutual_counts.items(),
        key = lambda item: (-item[1], item[0])
    )

    return sorted_candidates[:max_results]