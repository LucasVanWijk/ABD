from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector
import datetime
import random
import networkx as nx
import CBS_csv_to_groupinfo
from demographic import *

def compute_healthy(model):
    return sum([1 if not agent.infected and not agent.recovered else 0 for agent in model.schedule.agents])

def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents])

def compute_recovered(model):
    return sum([1 if agent.recovered else 0 for agent in model.schedule.agents])

class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, network_params, p_nodes, altruism, infect_chanse=20, seed=41, min_per_step=60,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
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
        self.total_agents = healthy_N + sick_N
        self.percent_infected = (sick_N / self.total_agents) * 100
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
        self.demo_distribution = {Child: 0,Student: 0, Adult:0, Elderly: 0}
        age_dict = CBS_csv_to_groupinfo.get_info_piramide()
        change_to_age_dict= {1: Child, 2: Student, 3: Adult, 4: Elderly}

        altruist_left = round(self.total_agents * altruism)
        # Distributes demographics
        for n in self.grid.G.nodes.data():
            if n[1]["type"] == "House":
                chance = random.uniform(0,1)
                agent_type = change_to_age_dict[sum([1 if x < chance else 0 for x in age_dict.values()])]
                agent = Infect_Agent(n[0], self, n[0], False, True, agent_type)
                if altruist_left > 0:
                    agent.altruist = True
                    altruist_left -= 1
                self.schedule.add(agent)
                self.grid.place_agent(agent, n[0])
                self.demo_distribution[agent_type] += 1

        # infect agents
        houses = []
        nodes = self.grid.G.nodes.data()
        for node in nodes:
            if node[1]["type"] == "House":
                houses.append(node)

        infected_houses = random.sample(houses, k=self.sick_agent)
        for house in infected_houses:
            house[1]["agent"][0].infected = True


        self.datacollector = DataCollector(
            model_reporters={"healthy": compute_healthy,
                            "infected": compute_infected,
                            "recovered": compute_recovered})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()
