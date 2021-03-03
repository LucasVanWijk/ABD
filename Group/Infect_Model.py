from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector
import datetime
import random
import networkx as nx


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents])


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, network_params, p_nodes, infect_chanse=20, seed=41, min_per_step=10,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.parallel_amount = 16
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date

        n_nodes = 0
        for network_param in network_params:
            n_nodes += network_param[0]

        self.G = nx.erdos_renyi_graph(n=n_nodes, p=p_nodes)
        self.grid = NetworkGrid(self.G)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date
        self.infect_chanse = infect_chanse
        random.seed(seed)

        node_index = 0
        for network_param in network_params:
            for i in range(network_param[0]):
                self.grid.G.nodes[node_index]["type"] = network_param[1]
                self.grid.G.nodes[node_index]["sub_type"] = network_param[2]
                self.grid.G.nodes[node_index]["color"] = network_param[3]
                node_index += 1

        # Create healthy agents
        for n in self.grid.G.nodes.data():
            if n[1]["type"] == "House":
                agent = Infect_Agent(n[0], self, n[0], False, True)
                self.grid.place_agent(agent, n[0])

        # infect agents
        houses = []
        nodes = self.grid.G.nodes.data()
        for node in nodes:
            if node[1]["type"] == "House":
                houses.append(node)

        infected_houses = random.sample(houses, k=self.sick_agent)
        for house in infected_houses:
            house[1]["agent"][0].infected = True
        
        for agent_type in self.agent_types:
            target_houses = random.sample(houses, k=agent_type[0])
            for house in target_houses:
                house[1]["agent"][0].demo = agent_type[1]

        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()
