from mesa import Agent
from demographic import demo
import random
import queue
import networkx as nx


class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, home, infected, altruist, demo_class):
        super().__init__(unique_id, model)
        self.infected = infected
        self.altruist = altruist
        self.home = home
        self.fear = 1
        self.demo = demo_class
        self.current_loc = None

        def get_sub_network(full_network, node_type, source):
            #Given the full network x network return a sub network where all nodes are of the given type
            #And where the source (node) is present
            return full_network

        
        def find_nearest(G, typeofnode, fromnode):
            subset_typeofnode = lambda G, typestr : [name for name, d in G.nodes(data=True) if 'type' in d and (d['type'] ==typestr)]
            #Calculate the length of paths from fromnode to all other nodes
            lengths=nx.single_source_dijkstra_path_length(G, fromnode, weight='distance')
            paths = nx.single_source_dijkstra_path(G, fromnode)

            #We are only interested in a particular type of node
            subnodes = subset_typeofnode(G, typeofnode)
            subdict = {k: v for k, v in lengths.items() if k in subnodes}

            #return the smallest of all lengths to get to typeofnode
            if subdict: #dict of shortest paths to all entrances/toilets
                nearest =  min(subdict, key=subdict.get) #shortest value among all the keys
                return nearest
            else: #not found, no path from source to typeofnode
                return(None, None, None)


        def find(node_source, type_of_node, all_nodes):
            all_paths =  nx.shortest_path(all_nodes, node_source)    
            shortest_path = min(all_paths, key=len)
            return shortest_path[-1]    


        def pop_closest_dict(home):
            network_types = model.network_types
            network_types.remove("House")
            closest_dict = {"House": home}
            for n_type in network_types:
                sub_network = get_sub_network(self.model.G, n_type, home)
                closest_dict[n_type] = find(home, n_type, sub_network)
            
            return closest_dict
        


        self.closest = pop_closest_dict(home)

    def move(self, time):
        if self.altruist:
            loc_name, base_chanse = self.demo.getAction(time)
            newChanse = base_chanse / self.fear
            if random.randint(0,100) < newChanse:
                locId = self.closest[self.current_loc][loc_name]
                self.model.network.move_agent(self, locId)
                self.current_loc = locId
            else:
                self.model.network.move_agent(self, self.home)
                self.current_loc = self.home

    def infect_other(self):
        """functie op te bepalen wie er in dezelfde node voorkomen, en dus elke tick een kans hebben om geinfecteerd te worden."""
        current = self.model.grid.get_cell_list_contents(self.pos)
        if len(current) > 0:
            for agent in current:
                if isinstance(agent, Infect_Agent):
                    if random.randint(0,100) < self.model.infect_chanse:
                        agent.infected = True

    def step(self):
        self.move(self.model.date)
        if self.infected:
            self.infect_other()





