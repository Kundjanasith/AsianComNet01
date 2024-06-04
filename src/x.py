import networkx as nx

# Create a graph
G = nx.Graph()

# Add edges with weights
G.add_edge('A', 'B', weight=4)
G.add_edge('B', 'D', weight=2)
G.add_edge('A', 'C', weight=3)
G.add_edge('C', 'D', weight=4)

# Find the bidirectional shortest path
shortest_path = nx.bidirectional_shortest_path(G, 'D', 'A')
shortest_path_length = nx.shortest_path_length(G, 'D', 'A', weight='weight', method='dijkstra')


print("Bidirectional Shortest Path:", shortest_path)
print("Bidirectional Shortest Path Length:", shortest_path_length)
