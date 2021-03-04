from mesa import Agent
from demographic import demo
import random
import queue
import networkx as nx
import Infect_function as ifunc


class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, home, infected, altruist, demo_class):
        super().__init__(unique_id, model)
        self.infected_timer = random.randint(2*24,7*24+1)
        self.suspectable_duration = random.randint(10*24,15*24+1) - self.infected_timer
        self.infected = infected
        self.recovered = False
        self.altruist = altruist
        self.home = home
        self.fear = 1
        self.demo = demo_class
        self.current_loc_type = "House"

        def find(node_source, type_of_node, model):
            all_nodes = model.nodes_by_type[type_of_node]
            network = model.G
            shortest = None
            for t in all_nodes:
                if nx.has_path(network, source=node_source, target=t):
                    shortest_path =  nx.shortest_path(network, source=node_source, target=t)
                    if shortest == None or len(shortest_path) < len(shortest):
                        shortest = shortest_path
            
            if shortest is not None:
                return shortest[-1]
            else:
                return None


        def pop_closest_dict(home):
            network_types = model.network_types.copy()
            network_types.remove("House")
            closest_dict = {"House": home}
            for n_type in network_types:
                closest_dict[n_type] = find(home, n_type, model)
            
            return closest_dict

        self.closest = pop_closest_dict(home)

    def move(self, time):
        return_value = self.demo.getAction(self.demo, time)
        if return_value != None:
            
            base_chanse, loc_name = return_value
            if self.altruist:
                
                newChanse = base_chanse / self.fear
                
                if random.randint(0,100) < newChanse:
                    locId = self.closest[loc_name]
                    print(locId)
                    self.model.grid.move_agent(self, locId)
                    self.current_loc_type = loc_name

                else:
                    print(self.home)
                    self.model.grid.move_agent(self, self.home)
                    self.current_loc_type = self.home
            else:
                locId = self.closest[loc_name]
                self.model.grid.move_agent(self, locId)
                self.current_loc_type = loc_name


    def infect_other(self):
        """functie op te bepalen wie er in dezelfde node voorkomen, en dus elke tick een kans hebben om geinfecteerd te worden."""
        
        if self.suspectable_duration == 0:
            self.infected = False
            self.recovered = True
            return

        if self.infected:
            self.suspectable_duration -= 1

        current = self.model.grid.G.nodes[self.pos]["agent"]
        if len(current) > 1:
            for agent in current:
                if isinstance(agent, Infect_Agent):
                    if random.randint(0,100) < ifunc.get_information_agent(self.current_loc_type):
                        # if self.infected_timer == 0 and not agent.recovered:
                        agent.infected = True
        
        return

    def step(self):
        self.move(self.model.date)
        if self.infected :
            self.infect_other()





