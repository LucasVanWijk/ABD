from mesa import Agent
from demographic import demo
import random


class Infect_Agent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, home, infected, altruist):
        super().__init__(unique_id, model)
        self.infected = infected
        self.altruist = altruist
        self.home = home
        self.fear = 1
        self.demo = demo()
        self.current_loc = None
        self.closest = pop_closest_dict(home)

        def move_to_recursion(node, desired_node_type):
            '''
            :param queue: list: [current node]
            :param visited: list: [current node]
            :param node: int/node: current node
            :param desired_node_type: string: "school"
            :return:
            '''
            
            def recursive(queue,visited, node, desired_node_type):
                s = queue.pop(0)
                for neighbour in [i for i in model.G.neighbors(node)]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
                        if model.G.nodes[neighbour]["type"] == desired_node_type:
                            return neighbour
                    node = neighbour
                recursive(queue, visited, node, desired_node_type)

            que = [node]
            visited = [node]
            return recursive(que, visited, node, desired_node_type)          

        def pop_closest_dict(home):
            network_types = model.network_types
            get_dict = lambda cell_id, network_types: {n_type: move_to_recursion(cell_id, n_type) for n_type in network_types}
            #get_dict = lambda cell_id, network_types: {n_type:home for n_type in network_types}
            to_determin_types = network_types[:].remove("Home")
            home_dict = get_dict(home, to_determin_types)
            closest_dict = {}
            closest_dict["Home"] = home_dict
            for key in home_dict:
                to_determin_types = network_types[:].remove(key)
                val = home_dict[key]
                closest_dict[val] = get_dict(val, to_determin_types)
            return closest_dict

    def move(self, time):
        if self.altruist:
            loc_name, base_chanse = self.demo.getAction(time)
            newChanse = base_chanse / self.fear
            if random.randint(0,100) < newChanse:
                locId = self.closest[self.current_loc][loc_name]
                self.model.network.move_agent(self, locId)
                self.current_loc = locId
            else:
                self.model.network.move_agent(self, self.home)
                self.current_loc = self.home

    def infect_other(self):
        """functie op te bepalen wie er in dezelfde node voorkomen, en dus elke tick een kans hebben om geinfecteerd te worden."""
        current = self.model.grid.get_cell_list_contents(self.pos)
        if len(current) > 0:
            for agent in current:
                if isinstance(agent, Infect_Agent):
                    if random.randint(0,100) < self.model.infect_chanse:
                        agent.infected = True

    def step(self):
        self.move(self.model.date)
        if self.infected:
            self.infect_other()





