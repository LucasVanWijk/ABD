import networkx as nx

def find(agent, node_source, type_of_node, model):
    all_nodes = model.nodes_by_type[type_of_node]
    network = model.G
    shortest = None
    max_for_type = {"House": 2,
                    "Work": 10,
                    "School": 30,
                    "Shop": 10,
                    "Bar": 20,
                    "Park": 1000,
                    "University": 1000}

    for t in all_nodes:
        if len(agent.model.grid.G.nodes[t]["agent"]) < max_for_type[type_of_node]:
            if nx.has_path(network, source=node_source, target=t):
                shortest_path = nx.shortest_path(network, source=node_source, target=t)
                if shortest == None or len(shortest_path)<len(shortest):
                    shortest = shortest_path

    if shortest is not None:
        return shortest[-1]
    else:
        return None

def pop_closest_dict(agent):
    home = agent.home
    network_types = agent.model.network_types.copy()
    network_types.remove("House")
    closest_dict = {"House": home}
    for n_type in network_types:
        closest_dict[n_type] = find(agent, home, n_type, agent.model)

    return closest_dict