""" Exersise 2.8
Implement  a  performance-measuring  environment  simulator  for  the  vacuum-cleanerworld
depicted in Figure 2.2 and specified on page 38. 
Your implementation should be modu-lar so that the sensors, actuators,
and environment characteristics (size, shape, dirt placement,etc.) can be changed easily. 
(Note:for some choices of programming language and operatingsystem there are already implementations in the online code repository.)
"""

""" Exersise 2.9
Implement a simple reflex agent for the vacuum environment in Exercise 2.8.
Run theenvironment  with this agent  for all possible  initial  dirt  configurations  and agent  locations.
Record the performance score for each configuration and the overall average score.

I will do some configuretions not all
"""


import random
class Vaccuum():
    def __init__(self, startLocation, VERBOSE=False):
        self.currentLocation = startLocation
        self.locIsDirty = None
        self.VERBOSE = VERBOSE

    def step(self):
        self.percieve()
        self.act()
        if self.VERBOSE:
            print(self.currentLocation)


    def percieve(self):
        self.currentLocation = self.detLocation()
        self.locIsDirty = self.detLocationIsDirty()

    def act(self,):
        if self.locIsDirty:
            if self.VERBOSE:
                print("Action: Suck")
            self.suck()
        else:
            if self.VERBOSE:
                print("Action: Move")
            if self.currentLocation == random.randint(0,1):
                self.move("right")
            else:
                self.move("left")

    def detLocation(self):
        #Reduntant but it says in the agent description that it looks where it is first
        return self.currentLocation
    
    def detLocationIsDirty(self):
        if world[self.currentLocation]:
            locIsDirty = True 
        else:
            locIsDirty = False

        return locIsDirty

    def move(self, direction):
        if direction == "left" and self.currentLocation != 0:
            self.currentLocation -= 1
        else:
            if self.currentLocation != len(world) -1:
                self.currentLocation += 1
    
    def suck(self):
        world[self.currentLocation] = False

def sim(stepsCount, initWorld, VERBOSE=False,startLocations=[0]):
    roombas = []
    simScore = []
    global world
    world = initWorld
    for loc in startLocations:
        roombas.append(Vaccuum(loc, VERBOSE=VERBOSE))
    for step in range(stepsCount):
        for roomba in roombas:
            roomba.step()
        simScore.append(len(world) -1 -sum(world))
    return (sum(simScore) / len(simScore))

def createWorld(size=5, dirySquares=[1,3]):
    world = [False for i in range(5)]
    for s in dirySquares:
        world[s] = True
    return world

print(sim(100,createWorld()))
print(sim(100,createWorld(dirySquares=[1,2,3,4])))