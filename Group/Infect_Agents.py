from mesa import Agent
from demographic import demo
import random
import queue
from make_dict_with_closest_loc import pop_closest_dict

class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, home, infected, altruist, demo_class):
        super().__init__(unique_id, model)
        self.infected_timer = random.randint(2*24,7*24+1)
        self.suspectable_duration = random.randint(10*24,15*24+1) - self.infected_timer
        self.infected = infected
        self.recovered = False
        self.altruist = altruist
        self.home = home
        self.fear = 1
        self.demo = demo_class
        self.current_loc_type = "House"
        self.closest = pop_closest_dict(self)
        self.infec_score = -31

    def make_percept_sentence(self):
        # TELL to an Agent: statement that asserts perception of info at given timestep
        #(env tells an agent relevant info)

        self.infected_sample_size = self.model.percent_infected
        self.time = self.model.date
        
        #if the current time is in the schedule returns the location it needs to go to and how much it want to go
        schedule = self.demo.getAction(self.demo, self.time)
        if schedule != None:
            self.base_chance, self.desired_loc_name = schedule
        else:
            self.base_chance, self.desired_loc_name = (None,None)


    def make_action_query(self):
        # ASK from Agent: constructs corresponding action to perception at given timestep
        #(env asks an agent what action should be taken)

        # def determin_fear(infected_sample_size):
        #     p = infected_sample_size
        #     if p > 75:
        #         return 4
        #     elif p > 50:
        #         return 3
        #     elif p > 25:
        #         return 2
        #     else:
        #         return 1

        # self.fear = determin_fear(self.infected_sample_size)
        # #Determins a new base_chanse
        # if self.base_chance != None:
        #     if self.altruist:
        #         self.chance_to_move = self.base_chance / self.fear
        #     else:
        #         self.chance_to_move = self.base_chance
        # else:
        #     self.chance_to_move = None
        
        # if self.chance_to_move != None:
        #     if random.randint(0, 100) < self.chance_to_move:
        #         pass
        #     else:
        #         self.desired_loc_name = "Home"
        if self.base_chance != None:
            infect_factor = self.model.percent_infected * 0.01
            self.going = self.base_chance * (1 - infect_factor) + (self.infec_score * infect_factor)
            self.not_going = 2
            if self.going < 5:
                if self.going < 3:
                    if self.going < 2:
                        pass 
        else:
            self.going = None
            self.not_going = None


    def make_action_sentence(self):
        # TELL to an Agent: take action and asserts that chosen action was executed
        
        def move(self):
            if self.going != None:
                try:
                    if self.going > self.not_going:
                        locId = self.closest[self.desired_loc_name]
                        self.model.grid.move_agent(self, locId)
                        self.current_loc_type = self.desired_loc_name
                    else:
                        self.model.grid.move_agent(self, self.home)
                        self.current_loc_type = self.home

                except:
                    self.model.grid.place_agent(self, self.home)
                    self.current_loc_type = "House"

        def infect_other(self):
            """functie op te bepalen wie er in dezelfde node voorkomen, en dus elke tick een kans hebben om geinfecteerd te worden."""
            
            if self.suspectable_duration == 0:
                self.infected = False
                self.recovered = True
                return

            if self.infected:
                self.suspectable_duration -= 1
                current = self.model.grid.G.nodes[self.pos]["agent"]
                if len(current) > 1:
                    for agent in current:
                        if isinstance(agent, Infect_Agent):
                            #determins infect chance
                            # Source https://www.sciencedirect.com/science/article/pii/S1684118220301432
                            # Acording to this paper the attack rate is 0.84% 
                            base_infect_per_10k = 84
                            p1 = ["Work","Home","School", "Bar"]
                            p2 = ["University"]
                            p3 = ["Shop"]
                            p4 = ["Park"]
                            location = self.current_loc_type

                            if location in p1:
                                infect_chance = base_infect_per_10k
                            
                            elif location in p2:
                                infect_chance = base_infect_per_10k/2

                            elif location in p3:
                                infect_chance = base_infect_per_10k/4

                            elif location in p4:
                                infect_chance = base_infect_per_10k/8
                            
                            else:
                                infect_chance = base_infect_per_10k
                            
                            if  random.randint(0,10000) < infect_chance:
                                agent.infected = True
        
        move(self)
        infect_other(self)

    def step(self):
        self.make_percept_sentence()
        self.make_action_query()
        self.make_action_sentence()





