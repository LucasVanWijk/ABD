from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector
import CBS_csv_to_groupinfo 
import datetime
import random
import networkx as nx
from demographic import *


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents])


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, network_params, p_nodes, infect_chanse=20, seed=41, min_per_step=10,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.total_agents = healthy_N + sick_N
        self.percent_infected = (sick_N / self.total_agents) * 100
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
        self.network_types = [i[1] for i in network_params]
        random.seed(seed)


        node_index = 0
        for network_param in network_params:
            for i in range(network_param[0]):
                self.grid.G.nodes[node_index]["type"] = network_param[1]
                self.grid.G.nodes[node_index]["sub_type"] = network_param[2]
                self.grid.G.nodes[node_index]["color"] = network_param[3]
                node_index += 1

        # Create agents
        self.demo_distribution = {Child: 0,Student: 0, Adult:0, Elderly: 0}
        age_dict = CBS_csv_to_groupinfo.get_info_piramide()
        change_to_age_dict= {1: Child, 2: Student, 3: Adult, 4: Elderly}

        for n in self.grid.G.nodes.data():
            if n[1]["type"] == "House":
                chance = random.uniform(0,1)
                agent_type = change_to_age_dict[sum([1 if x < chance else 0 for x in age_dict.values()])]
                agent = Infect_Agent(n[0], self, n[0], False, True, agent_type)
                
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


        all_dif_agent_demos = []
        for key in self.demo_distribution:
            all_dif_agent_demos += [key] * self.demo_distribution[key]

        diff_demo_houses = random.sample(houses, k=sum(self.demo_distribution.values()))
        for house in diff_demo_houses:
            house[1]["agent"][0].demo = all_dif_agent_demos.pop()            

        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.percent_infected = (compute_infected(self) / self.total_agents)*100
        self.datacollector.collect(self)
        self.schedule.step()
