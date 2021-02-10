from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Infect_Agents import Infect_Agent
from mesa.datacollection import DataCollector

def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])

class Base_Model(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height):
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        
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
        self.datacollector.collect(self)
        self.schedule.step()