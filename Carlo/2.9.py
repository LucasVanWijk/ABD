import numpy


class Environment:

    def __init__(self, size, amount_dirt):
        self.squares = numpy.zeros(size)
        self.current_location = 0

        # generate random dirt
        self.squares[:amount_dirt] = 1
        numpy.random.shuffle(self.squares)


class VacuumCleaner:

    def __init__(self):
        self.environment = Environment(20, 13)
        self.performance = 0
        self.direction = "right"

    def start(self, time):
        for _ in range(time):
            if self.dirt_on_current_location():
                self.suck()
            if self.next_move_is_collision(self.direction):
                self.switch_direction()
            if self.direction == "right":
                self.move_right()
            elif self.direction == "left":
                self.move_left()

    def get_location(self):
        return self.environment.current_location

    def dirt_on_current_location(self):
        if self.environment.squares[self.get_location()] == 1:
            return True
        else:
            return False

    def next_move_is_collision(self, direction):
        if direction == "right" and self.get_location() + 1 >= len(self.environment.squares):
            return True
        elif direction == "left" and self.get_location() - 1 <= -1:
            return True
        else:
            return False

    def switch_direction(self):
        if self.direction == "right":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "right"

    def move_left(self):
        self.environment.current_location -= 1
        print("The vacuum cleaner moved left to square {}.".format(self.get_location()))

    def move_right(self):
        self.environment.current_location += 1
        print("The vacuum cleaner moved right to square {}.".format(self.get_location()))

    def suck(self):
        self.environment.squares[self.get_location()] = 0
        self.performance += 1
        print("Location {} is cleaned. Current performance is {}.".format(self.get_location(), self.performance))


if __name__ == '__main__':
    vc = VacuumCleaner()
    vc.start(200)
