from mesa import Agent

from pathfinding import get_positions, find_closest_cell
import random


class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, home, infected):
        super().__init__(unique_id, model)
        self.infected = infected
        self.closest_rec = None
        self.closest_work = None
        self.home = home
        self.move_que = []

    def move(self, time):
        # possible_steps = self.model.network.get_neighborhood(
        #     self.pos,
        #     moore=True,
        #     include_center=False)
        # new_position = self.random.choice(possible_steps)
        # self.model.network.move_agent(self, new_position)

        if 8 == time.hour and time.minute == 0:
            self.closest_work = find_closest_cell(self.model.work, self.pos)
            self.move_que = get_positions(self.pos, self.closest_work)
        
        elif 17 == time.hour and time.minute == 0:
            self.closest_rec = find_closest_cell(self.model.recreation, self.pos)
            self.move_que = get_positions(self.pos, self.closest_rec)

        elif 19 == time.hour and time.minute == 0:
            self.move_que = get_positions(self.pos, self.home)
        
        if len(self.move_que) > 0:
            self.model.grid.move_agent(self, self.move_que[0])
            self.move_que = self.move_que[1:]

    def infect_other(self):
        surround = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
        if len(surround) > 0:
            for agent in surround:
                if isinstance(agent, Infect_Agent):
                    if random.randint(0,100)<self.model.infect_chanse:
                        agent.infected = True

    def step(self):
        self.move(self.model.date)
        if self.infected:
            self.infect_other()


class Work(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Recreation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)




