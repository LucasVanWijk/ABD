def agent():
    #TODO has a agent which moves to a random square every tick
    infected = None
    
    def check_neighbours(self):
        neighbours = self.model.grid.get_cell_list_contents([self.pos])
        for person in neighbours:
            if person.infected:
                return True
        return False
        
    def move(self):
        #  https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html

        possible_steps = self.model.grid.get_neighborhood(
        self.pos,
        moore=True,
        include_center=False)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()
        if self.check_neighbours(): #TODO if neigbor is infected become infected
            self.infected = True
        