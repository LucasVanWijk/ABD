import random
import copy

class environment():
    bin_dict = {
        "unknown" : 0,
        "empty": 1,
        "agent": 2,
        "wumpus": 4,
        # "deadwumpus": 8,
        "stench": 16,
        "pit": 32,
        "breeze": 64,
        "gold": 128}

    dict_bin = {
        0 : "[]",
        1 : "E",
        2 : "A",
        4 : "W",
        # 8 : "D",
        16 : "s",
        32 : "P",
        64 : "b",
        128 : "G"}

    def check_no_player(self, random_loc):
        if random_loc != ((self.grid_size ** 2) - self.grid_size):
            return random_loc
        else:
            return -1

    def make_grid(self):
        grid = []
        for i in range(self.grid_size):
            grid.append([])
            for j in range(self.grid_size):
                grid[i].append(0)
        return grid

    def create_pits(self):
        pits = []
        for i in range(0, self.grid_size ** 2):  # pits
            if self.check_no_player(i) != -1 and 0.2 > random.uniform(0, 1):  # start
                pits.append(i)
        return pits

    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.grid = self.make_grid()

        self.wumpus, self.gold = -1, -1
        while self.wumpus == -1 or self.gold == -1:
            self.wumpus = self.check_no_player(random.randint(0, grid_size**2)-1)
            self.gold = self.check_no_player(random.randint(0, grid_size**2)-1)

        self.pits = self.create_pits()
        self.agent = (grid_size ** 2) - grid_size
        self.binary_grid()       

    def binary_grid(self):

        def get_surroundings(loc):
            x = [loc // self.grid_size][0]
            y = [loc % self.grid_size][0]
            sur = []
            for x2 in [x-1, x+1]:
                if x2 >= 0 and x2 < self.grid_size:
                    sur.append((x2 * self.grid_size) + y)

            for y2 in [y-1, y+1]:
                if y2 >= 0 and y2 < self.grid_size:
                    sur.append((x * self.grid_size) + y2)
            return sur

        def add_grid(var, dict_var):
            self.grid[var // self.grid_size][var % self.grid_size] += self.bin_dict[dict_var]

        # agent
        add_grid(self.agent, "agent")

        # gold
        add_grid(self.gold, "gold")

        # wumpus
        add_grid(self.wumpus, "wumpus")
        wumpus_set = set(get_surroundings(self.wumpus))

        # pits
        pit_set = set()
        for pit in self.pits:
            add_grid(pit, "pit")
            pit_set.update(get_surroundings(pit))

        # stench and breeze 
        pit_set -= set(self.pits)
        wumpus_set -= set(self.pits)
        [add_grid(coord, "stench") for coord in list(wumpus_set)]
        [add_grid(coord, "breeze") for coord in list(pit_set)]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                coord = (x * self.grid_size) + y
                if self.grid[x][y] == 0 or coord == self.agent:
                    self.grid[x][y] += 1

    def agent_grid(self):
        agent_grid = self.make_grid()

        agent_loc = ((self.grid_size ** 2) - self.grid_size)
        x_loc = agent_loc // self.grid_size
        y_loc = agent_loc % self.grid_size
        agent_grid[x_loc][y_loc] = self.grid[x_loc][y_loc]

        return agent_grid


class wumpus():
    agent_decode = {
        0 : "unknown",
        1 : "safe",
        2 : "visited",
        4 : "unsure pit",
        8 : "sure pit",
        16: "unsure wumpus",
        32: "sure wumpus",
        64: "dead wumpus"
    }

    decode = {
        0 : "[]",
        1 : "E",
        2 : "A",
        4 : "W",
        8 : "D",
        16 : "s",
        32 : "P",
        64 : "b",
        128 : "G"}
        
    def __init__(self,full_grid, known_grid):
        self.invis_grid = full_grid
        self.known_grid = known_grid
        self.grid_size = len(known_grid[0])
        self.coord = (self.grid_size ** 2) - self.grid_size
        self.old_coord = copy.deepcopy(self.coord)
        
        self.direction = "R"
        self.end = True
        self.arrow = True
        self.points = 0
        self.wumpus_alive = True

    def update_grid(self):
        if self.old_coord != self.coord:
            agent_old_x = self.old_coord // self.grid_size
            agent_old_y = self.old_coord % self.grid_size
            self.invis_grid[agent_old_x][agent_old_y] -= 2
            self.known_grid[agent_old_x][agent_old_y] -= 2

            agent_new_x = self.coord // self.grid_size
            agent_new_y = self.coord % self.grid_size
            self.invis_grid[agent_new_x][agent_new_y] += 2
            self.known_grid[agent_new_x][agent_new_y] = copy.deepcopy(self.invis_grid[agent_new_x][agent_new_y])

            self.old_coord = copy.deepcopy(self.coord)
        return        

    def change_dir(self,newdir):
        direction_cycle = ["U","R","D","L"]
        if newdir == "L":
            self.direction = direction_cycle[(direction_cycle.index(self.direction) - 1) % 4]    

        elif newdir == "R":
            self.direction = direction_cycle[(direction_cycle.index(self.direction) + 1) % 4]
        return 
    
    def check_death_win(self):
        lst,lst2 = self.decode_wumpus()
        if 4 in lst or 32 in lst:
            self.death()
        elif 128 in lst:
            self.win()

    def forward(self):
        self.points -= 1
        print("moving ",end="")
        agent_x = self.coord // self.grid_size
        agent_y = self.coord % self.grid_size

        if self.direction == "U":    
            if agent_x > 0:
                self.coord -= self.grid_size
                print("up")
            else:
                print("bump")
            
        elif self.direction == "D":
            if agent_x < (self.grid_size - 1):
                self.coord += self.grid_size
                print("down")
            else:
                print("bump")

        elif self.direction == "L":
            if agent_y > 0:
                self.coord -= 1
                print("left")
            else:
                print("bump")

        elif self.direction == "R":
            if agent_y < (self.grid_size - 1):
                self.coord += 1
                print("right")
            else:
                print("bump")

        self.update_grid()
        self.check_death_win()
    
    def decode_wumpus(self, decode_coord = -1 ):
        if decode_coord == -1:
            decode_coord = self.coord

        lst = []
        lst2 = []
        agent_x = decode_coord // self.grid_size
        agent_y = decode_coord  % self.grid_size
        bincode = self.invis_grid[agent_x][agent_y]

        for binary in list(reversed(sorted(self.decode.keys()))):
            if (bincode - binary) >= 0:
                bincode = bincode - binary
                lst.append(binary)
                lst2.append(self.decode[binary])

        return lst,lst2

    def decode_grid(self,grid_to_decode):
        new_grid = []
        for x in range(self.grid_size):
            new_grid.append([])
            for y in range(self.grid_size):
                new_grid[x].append([])

                if grid_to_decode[x][y] == 0 or grid_to_decode[x][y] == 1:
                    new_grid[x][y] = self.decode[grid_to_decode[x][y]]

                else:
                    value = grid_to_decode[x][y]
                    lst = []
                    for binary in list(reversed(sorted(self.decode.keys()))):
                        if (value - binary) >= 0 and binary > 1:
                            value = value - binary
                            lst.append(self.decode[binary])
                    new_grid[x][y] = ' '.join(lst)

        return new_grid
    
    def shoot(self): 
        if self.arrow == True:
            self.points -= 10
            newcoord = copy.deepcopy(self.coord)
            agent_x = self.coord // self.grid_size
            agent_y = self.coord % self.grid_size
        
            self.arrow = False
            if self.direction == "U":    
                if agent_x > 0:
                    newcoord -= self.grid_size
            
            elif self.direction == "D":
                if agent_x < (self.grid_size - 1):
                    newcoord += self.grid_size

            elif self.direction == "L":
                if agent_y > 0:
                    newcoord -= 1

            elif self.direction == "R":
                if agent_y < (self.grid_size - 1):
                    newcoord += 1
            lst,lst2 = self.decode_wumpus(newcoord)

            
            if 4 in lst:
                new_x =  newcoord // self.grid_size
                new_y = newcoord  % self.grid_size
                self.invis_grid[new_x][new_y] += 4
                self.wumpus_alive = False
                print("Scream")
        else:
            print("You dont have an arrow")

    def death(self):
        self.points -= 1000
        print("you died")
        self.end = False

    def win(self):
        self.points += 1000
        print("you win")
        self.end = False

    def leave(self):
        if self.coord == (self.grid_size ** 2) - self.grid_size:
            print("you left the cave")
            self.end = False

    def play_self(self):
        while self.end:
            print(player)
            move = input("next move?\n").upper()
            if move == "L" or move == "R":
                self.change_dir(move)
            elif move == "F":
                self.forward()
            elif move == "S":
                print("shooting")
                self.shoot()
            elif move == "LEAVE":
                self.leave()
            else:
                pass

    def __str__(self,):        
        print_string = ""
        if self.end:
            grid = self.known_grid
        else:
            grid = self.invis_grid

        for row in self.decode_grid(grid):
            print_string += ('\t'.join(str(e) for e in row))
            print_string += "\n"

        if self.end:
            print_string += "looking: " + self.direction + "\n"
            
        print_string += "points: " + str(self.points) + "\n"

        return print_string

a = environment(4)
wumpusgrid = a.grid
agent_grid = a.agent_grid()

player = wumpus(wumpusgrid, agent_grid)

player.play_self()
print(player)

# player.death()