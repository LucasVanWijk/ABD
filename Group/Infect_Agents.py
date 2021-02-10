from mesa import Agent
from Find_Closest_Cell import find
from pathfinding import  get_positions

class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,infected=False):
        super().__init__(unique_id, model)
        self.infected = infected
        self.closest_rec = find(self.model.recreation, self.pos)
        self.closest_work = find(self.model.work, self.pos)
        self.move_que = []

    def move(self, time):
        # possible_steps = self.model.grid.get_neighborhood(
        #     self.pos,
        #     moore=True,
        #     include_center=False)
        # new_position = self.random.choice(possible_steps)
        # self.model.grid.move_agent(self, new_position)

        if 8 == time.hour:
            self.closest_work = find(self.model.work, self.pos)
            self.move_que = get_positions(self.pos, self.closest_work)
        
        elif 17 == time.hour:
            self.closest_rec = find(self.model.recreation, self.pos)
            self.move_que = get_positions(self.pos, self.closest_rec)

        elif 19 == time.hour:
            self.move_que = get_positions(self.pos, self.model.grid.find_empty())
        
        if len(self.move_que) > 0:
            self.model.grid.move_agent(self, self.move_que[0])
            self.move_que = self.move_que[1:]


    def infect_other(self):
        surround = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        for cell in surround:
            cellmates = self.model.grid.get_cell_list_contents([cell])
            if len(cellmates) > 0:
                    for agent in cellmates:
                        if isinstance(agent, Infect_Agent):
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




