from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from Infect_Agents import Infect_Agent, Work, Recreation
from mesa.datacollection import DataCollector
import datetime
import random
import networkx as nx


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents])


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, n_nodes, p_nodes, work_n, rec_n, infect_chanse=20, seed=41, min_per_step=10,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.parallel_amount = 16
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date
        self.G = nx.erdos_renyi_graph(n=n_nodes, p=p_nodes)
        self.grid = NetworkGrid(self.G)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date
        self.work = []
        self.recreation = []
        self.infect_chanse = infect_chanse
        random.seed(seed)

        # build work
        self.work = random.sample(range(n_nodes), k=work_n)
        for w_node in self.work:
            self.grid.G.nodes[w_node]["type"] = "work"

        # build recreation
        nodes = list(range(n_nodes))
        for n in self.work:
            nodes.remove(n)
        self.recreation = random.sample(nodes, k=rec_n)
        for r_node in self.recreation:
            self.grid.G.nodes[r_node]["type"] = "recreation"

        # build empty
        nodes = list(range(n_nodes))
        for n in self.work:
            nodes.remove(n)
        for n in self.recreation:
            nodes.remove(n)
        for e_node in nodes:
            self.grid.G.nodes[e_node]["type"] = "empty"


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
