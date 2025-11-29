import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from social_graph.graph import Graph
from social_graph.recommendation import recommend_friends

g = Graph()
g.add_friendship("Alice", "Bob")
g.add_friendship("Alice", "Charlie")
g.add_friendship("Bob", "David")
g.add_friendship("Charlie", "David")
g.add_friendship("Charlie", "Eve")

print("Adjacency List")
print(g.print_adjacency_list())

print("Adjacency Matrix")
print(g.print_adjacency_matrix())

print("Recommendations fo Alice: ")
for name, mutual in recommend_friends(g, "Alice"):
    print(f"{name} (mutual friends: {mutual})")





