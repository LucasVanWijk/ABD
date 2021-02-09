from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

def visu():
    def agent_portrayal(agent):
        if agent.infected():
            portrayal = {"Shape": "circle",
                        "Color": "red",
                        "Filled": "true",
                        "Layer": 0,
                        "r": 0.5}
            return portrayal
        else:    
            portrayal = {"Shape": "circle",
                        "Color": "Green",
                        "Filled": "true",
                        "Layer": 0,
                        "r": 0.5}
            return portrayal

    world = CanvasGrid(agent_portrayal, 10, 10, 500, 500)    
    chart = ChartModule([{"Label": "Gini",
                        "Color": "Black"}],
                        data_collector_name='datacollector')

    server = ModularServer(MoneyModel,
                        [world, chart],
                        "Money Model",
                        {"N":100, "width":10, "height":10})
    
    server.port = 8521 # The default
    server.launch()

visu()