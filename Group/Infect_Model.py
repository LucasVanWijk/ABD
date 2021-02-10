from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Infect_Agents import Infect_Agent, City, Village, Recreation
from mesa.datacollection import DataCollector
import datetime


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])


def build_city_village_rec(model, start_h, start_w, size, type_build):
    for h in range(start_h, start_h + size):
        for w in range(start_w, start_w + size):
            if type_build == "city":
                city = City(int(str(h) + "0" + str(w)), model)
                model.grid.place_agent(city, (w, h))
            elif type_build == "village":
                village = City(int(str(h) + "0" + str(w)), model)
                model.grid.place_agent(village, (w, h))
            elif type_build == "recreation":
                recreation = City(int(str(h) + "0" + str(w)), model)
                model.grid.place_agent(recreation, (w, h))


class Base_Model(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height, min_per_step=1,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date

        # build cities
        build_city_village_rec(self, 5, 4, 7, "city")

        # build villages
        build_city_village_rec(self, 30, 20, 4, "village")
        build_city_village_rec(self, 30, 20, 5, "village")

        # build recreations
        build_city_village_rec(self, 31, 21, 2, "recreation")
        build_city_village_rec(self, 6, 5, 2, "recreation")

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