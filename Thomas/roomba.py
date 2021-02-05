import numpy as np
import random

class floor():
    def __init__(self,size,dirty):
        if dirty < size:
            floor = np.zeros(size)
            dirty = random.sample(range(0, size), dirty)
            for number in dirty:
                floor[number] = 1
        self.floor = floor
        
    def cleanfloor(self,floor_tile):
        self.floor[floor_tile] = 0
        
    def dirtyfloor(self,floor_tile):
        self.floor[floor_tile] = 1


class roomba():
    
    def __init__(self,floor):
        self.direction = "L"
        self.position = random.randint(0,len(floor.floor) - 1)
        self.floor = floor

    def check_move(self):
        new_pos = self.position + self.move()
        return (new_pos >= 0) and (new_pos <= (len(self.floor.floor) - 1))       

    def change_direction(self):
        if self.direction == "L":
            self.direction = "R"
        else:
            self.direction = "L"
    
    def check_dirty(self):
        return self.floor.floor[self.position]

    def clean(self):
        return self.floor.cleanfloor(self.position)

    def move(self):
        if self.direction == "L":
            return -1
        else:
            return 1

    def next(self):
        print(self.floor.floor)
        if self.check_dirty():
            self.clean()
            print('cleaning', self.position)

        elif self.check_move():
            self.position += self.move()
            print("moving to " , self.position)
        
        else:
            self.change_direction()
            print("change direction to ", self.direction)

main_floor = floor(55,22)

cleaner = roomba(main_floor)
for i in range(50):
    cleaner.next()

