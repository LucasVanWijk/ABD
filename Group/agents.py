from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,infected=False):
        super().__init__(unique_id, model)
        self.infected = infected

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect_other(self):
        surround = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=True)
        for cell in surround:
            cellmates = self.model.grid.get_cell_list_contents([cell])
            if len(cellmates) > 0:
                for agent in cellmates:
                    agent.infected = True

    def step(self):
        self.move()
        if self.infected:
            self.infect_other()


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height):
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        
        # infected agent
        for i in range(self.sick_agent):
            a = MoneyAgent(i, self,True)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create healthy agents
        for i in range(self.sick_agent,self.sick_agent+ self.healthy_agents):
            a = MoneyAgent(i, self)
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