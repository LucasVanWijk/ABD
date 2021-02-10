from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector
import datetime

def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])

class Base_Model(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height, min_per_step=1,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date
        
        # infected agent
        for i in range(self.sick_agent):
            a = Infect_Agent(i, self,True)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create healthy agents
        for i in range(self.sick_agent,self.sick_agent+ self.healthy_agents):
            a = Infect_Agent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()