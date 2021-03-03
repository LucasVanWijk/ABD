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


        #
        # # infected agent
        # for i in range(self.sick_agent):
        #     x = self.random.randrange(self.network.width)
        #     y = self.random.randrange(self.network.height)
        #     a = Infect_Agent(i, self, (x,y), infected=True)
        #     self.schedule.add(a)
        #     # Add the agent to a random network cell
        #     self.network.place_agent(a, (x, y))
        #
        # # Create healthy agents
        # for i in range(self.sick_agent,self.sick_agent+ self.healthy_agents):
        #     x = self.random.randrange(self.network.width)
        #     y = self.random.randrange(self.network.height)
        #     a = Infect_Agent(i, self, (x,y), infected=False)
        #     self.schedule.add(a)
        #     # Add the agent to a random network cell
        #     self.network.place_agent(a, (x, y))
        
        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()
