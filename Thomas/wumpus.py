import random

class environment():
    bin_dict = {
        "empty": 0,
        "agent": 1,
        "wumpus": 2,
        "stench": 4,
        "pit": 8,
        "breeze": 16,
        "gold": 32,
        "glitter": 64}

    dict_bin = {
        0 : "E",
        1 : "A",
        2 : "W",
        4 : "s",
        8 : "P",
        16 : "b",
        32 : "G",
        64 : "g"}

    def check_no_player(self, grid_size, random_loc):
        if random_loc != ((grid_size ** 2) - grid_size):
            return random_loc
        else:
            return -1

    def make_grid(self, grid_size):
        grid = []
        for i in range(grid_size):
            grid.append([])
            for j in range(grid_size):
                grid[i].append(0)
        return grid

    def create_pits(self, grid_size):
        pits = []
        for i in range(0, grid_size ** 2):  # pits
            if self.check_no_player(grid_size, i) != -1 and 0.2 > random.uniform(0, 1):  # start
                pits.append(i)
        return pits

    def __init__(self, grid_size=4):
        self.grid = self.make_grid(grid_size)

        self.wumpus, self.gold = -1, -1
        while self.wumpus == -1 or self.gold == -1:
            self.wumpus = self.check_no_player(grid_size, random.randint(0, grid_size**2)-1)
            self.gold = self.check_no_player(grid_size, random.randint(0, grid_size**2)-1)

        self.grid_size = grid_size
        self.pits = self.create_pits(grid_size)
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
        gold_set = set(get_surroundings(self.gold))

        # wumpus
        add_grid(self.wumpus, "wumpus")
        wumpus_set = set(get_surroundings(self.wumpus))

        # pits
        pit_set = set()
        for pit in self.pits:
            add_grid(pit, "pit")
            pit_set.update(get_surroundings(pit))
        
        # stench and breeze and glitter
        gold_set -= set(self.pits)
        pit_set -= set(self.pits)
        wumpus_set -= set(self.pits)
        [add_grid(coord, "glitter") for coord in list(gold_set)]
        [add_grid(coord, "stench") for coord in list(wumpus_set)]
        [add_grid(coord, "breeze") for coord in list(pit_set)]
        
    def decode_grid(self):
        new_grid = []
        for x in range(self.grid_size):
            new_grid.append([])
            for y in range(self.grid_size):
                new_grid[x].append([])

                if self.grid[x][y] == 0:
                    new_grid[x][y] = self.dict_bin[0]

                else:
                    value = self.grid[x][y]
                    lst = []
                    for binary in [64,32,16,8,4,2,1]:
                        if (value - binary) >= 0:
                            value = value - binary
                            lst.append(self.dict_bin[binary])
                    new_grid[x][y] = ' '.join(lst)
        
        return new_grid

    def __str__(self):
        
        print_string = ""
        for row in self.decode_grid():
            print_string += ('\t'.join(str(e) for e in row))
            print_string += "\n"
        return print_string[:-1]


class wumpus():
    def __init__(self):
        pass

    def binary_wumpus(self):
        # "empty" : 0,
        # "agent" : 1,
        # "wumpus" : 2,
        # "stench" : 4,
        # "pit" : 8,
        # "breeze" : 16,
        # "gold" : 32,
        # "glitter" : 64,
        # "OK" : 128,
        # "visited" : 256,
        # "unsure" : 512,
        # "sure" : 1024
        pass


a = environment(5)

print(a)