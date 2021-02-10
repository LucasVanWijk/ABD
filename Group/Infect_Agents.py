from mesa import Agent
import datetime
class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,infected=False):
        super().__init__(unique_id, model)
        self.infected = infected

    def move(self, time):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect_other(self):
        surround = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        for cell in surround:
            cellmates = self.model.grid.get_cell_list_contents([cell])
            if len(cellmates) > 0:
                for agent in cellmates:
                    agent.infected = True

    def step(self):
        time = self.model.ini_date + datetime.timedelta(minutes= self.model.min_per_step * self.model.schedule.steps)
        self.move(time)
        if self.infected:
            self.infect_other()


