from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector
import datetime
import random
import networkx as nx
from demographic import *


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents])


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, network_params, p_nodes, infect_chanse=20, seed=41, min_per_step=60,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
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
        self.demo_distribution = {Student: 10, Elderly: 10, Child: 10}
        self.network_types = [i[1] for i in network_params]
        self.nodes_by_type = dict()
        random.seed(seed)

        node_index = 0
        for network_param in network_params:
            for i in range(network_param[0]):
                self.grid.G.nodes[node_index]["type"] = network_param[1]
                self.grid.G.nodes[node_index]["color"] = network_param[2]
                node_index += 1
        
        # split nodes by type
        for n_type in self.network_types:
            self.nodes_by_type[n_type] = [i[0] for i in self.grid.G.nodes.data() if i[1]["type"] == n_type]

        # Create agents
        for n in self.grid.G.nodes.data():
            if n[1]["type"] == "House":
                agent = Infect_Agent(n[0], self, n[0], False, True, Adult)
                self.schedule.add(agent)
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


        all_dif_agent_demos = []
        for key in self.demo_distribution:
            all_dif_agent_demos += [key] * self.demo_distribution[key]



        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()
