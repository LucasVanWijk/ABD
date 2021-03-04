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



        def find(node_source, type_of_node, model):
            all_nodes = model.temp_node
            network = model.G
            shortest = [0] * 99
            for t in all_nodes:
                shortest_path =  nx.shortest_path(network, source=node_source, target=t)
                if len(shortest_path) < len(shortest):
                    shortest = shortest_path
                return shortest[-1]


        def pop_closest_dict(home):
            network_types = model.network_types.copy()
            network_types.remove("House")
            closest_dict = {"House": home}
            for n_type in network_types:
                closest_dict[n_type] = find(home, n_type, model)
            
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





