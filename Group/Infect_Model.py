from mesa import Model
from parallel import SimultaneousActivation
from mesa.space import MultiGrid
from Infect_Agents import Infect_Agent, Work, Recreation
from mesa.datacollection import DataCollector
import datetime


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])


def build_work_recreation(model, start_h, start_w, size, type_build):
    for h in range(start_h, start_h + size):
        for w in range(start_w, start_w + size):
            if type_build == "work":
                work = Work(int(str(h) + "0" + str(w)), model)
                model.grid.place_agent(work, (w, h))
                model.work.append((w, h))
            elif type_build == "recreation":
                recreation = Recreation(int(str(h) + "0" + str(w)), model)
                model.grid.place_agent(recreation, (w, h))
                model.recreation.append((w, h))


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height, min_per_step=10,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.parallel_amount = 16
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date
        self.work = []
        self.recreation = []

        # build work
        build_work_recreation(self, 5, 4, 7, "work")
        build_work_recreation(self, 30, 35, 7, "work")

        # build recreations
        build_work_recreation(self, 2, 80, 5, "recreation")
        build_work_recreation(self, 90, 90, 5, "recreation")

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