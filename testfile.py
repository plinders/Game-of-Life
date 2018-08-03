
import numpy as np

class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.new_state = state

    def updateState(self):
        self.state = self.new_state

    def calcSurvival(self, num_neighbours):
        if self.state == 0 and num_neighbours == REPRODUCTION:
            self.new_state = 1
        elif self.state == 1 and (num_neighbours < UNDERPOPULATION or num_neighbours > OVERPOPULATION):
            self.new_state = 0
        else: self.new_state = self.state

def createWorld(width, height):
    world = [[Cell(x, y, np.random.randint(0, 2)) for y in range(height)] for x in range(width)]
    return(world)

def toArray(world):
    frame = [[world[x][y].state for y in range(len(world[0]))] for x in range(len(world[1]))]
    return(np.array(frame))

world = createWorld(10, 10)
print(world)
print(toArray(world))
print(toArray(world).sum())
