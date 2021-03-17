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
        self.closest = self.pop_closest_dict(home)

    def make_percept_sentence(self):
        # TELL to an Agent: statement that asserts perception of info at given timestep
        #(env tells an agent relevant info)
        infected_sample_size = self.model.percent_infected
        self.infected_size = infected_sample_size
        self.time = self.model.date
        self.base_chance, self.desired_loc_name = self.demo.getAction(self.demo, self.time)
        pass

    def make_action_query(self):
        # ASK from Agent: constructs corresponding action to perception at given timestep
        #(env asks an agent what action should be taken)
        self.fear = self.determin_fear(self.infected_sample_size)
        if self.altruist:
            self.chance_to_move = self.base_chance/ self.fear
        else:
            self.chance_to_move = self.base_chance
        pass

    def make_action_sentence(self):
        # TELL to an Agent: take action and asserts that chosen action was executed
        # moves the agent
        try:
            if random.randint(0, 100) < self.chance_to_move:
                locId = self.closest[self.desired_loc_name]
                self.model.grid.move_agent(self, locId)
                self.current_loc_type = self.desired_loc_name
            else:
                self.model.grid.move_agent(self, self.home)
                self.current_loc_type = self.home

        except:
            self.model.grid.place_agent(self, self.home)
            self.current_loc_type = "House"

    def find(self, node_source, type_of_node, model):
        all_nodes = model.nodes_by_type[type_of_node]
        network = model.G
        shortest = None
        max_for_type = {"House": 2,
                        "Work": 5,
                        "School": 30,
                        "Shop": 5,
                        "Bar": 20,
                        "Park": 1000,
                        "University": 1000}

        for t in all_nodes:
            if len(self.model.grid.G.nodes[t]["agent"]) < max_for_type[type_of_node]:
                if nx.has_path(network, source=node_source, target=t):
                    shortest_path = nx.shortest_path(network, source=node_source, target=t)
                    if shortest == None or len(shortest_path):
                        shortest = shortest_path

        if shortest is not None:
            return shortest[-1]
        else:
            return None

    def pop_closest_dict(self,home):
        network_types = self.model.network_types.copy()
        network_types.remove("House")
        closest_dict = {"House": home}
        for n_type in network_types:
            closest_dict[n_type] = self.find(home, n_type, self.model)

        return closest_dict



    def move(self, time):
        try:
            if random.randint(0, 100) < self.chance_to_move:
                locId = self.closest[self.desired_loc_name]
                self.model.grid.move_agent(self, locId)
                self.current_loc_type = self.desired_loc_name
            else:
                self.model.grid.move_agent(self, self.home)
                self.current_loc_type = self.home

        except:
            self.model.grid.place_agent(self, self.home)
            self.current_loc_type = "House"


    def infect_other(self):
        """functie op te bepalen wie er in dezelfde node voorkomen, en dus elke tick een kans hebben om geinfecteerd te worden."""
        
        if self.suspectable_duration == 0:
            self.infected = False
            self.recovered = True
            return

        if self.infected:
            self.suspectable_duration -= 1

        current = self.model.grid.G.nodes[self.pos]["agent"]
        print(current)
        if len(current) > 1:
            for agent in current:
                if isinstance(agent, Infect_Agent):
                    if random.randint(0,100) < ifunc.get_information_agent(self.current_loc_type):
                        # if self.infected_timer == 0 and not agent.recovered:
                        agent.infected = True

    def determin_fear(self,infected_sample_size):
        p = infected_sample_size
        if p > 75:
            return 4
        elif p > 50:
            return 3
        elif p > 25:
            return 2
        else:
            return 1

    def step(self):
        # roept percet etc aan
        self.make_percept_sentence()
        self.make_action_query()
        self.make_action_sentence()
        # infect_other is not an conscious action of an Agent, so the action is not defined in make_action_sentence
        if self.infected:
            self.infect_other()




