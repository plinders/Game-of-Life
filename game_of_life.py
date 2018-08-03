#Game of Life
"""
# Ideas:

* Make each pixel an object and follow its state (make sure to return state)
    * Save state, and new_state as properties of the Cell
    * Write methods to update properties
        * This also includes rendering a new frame (move new_state to state)
* GoL in 3D space

#Rules:
1. A living cell will survive into the next generation by default, unless:
    - It has fewer than 2 live neighbours (underpopulation)
    - It has more than three live neighbours (overpopulation)
2. A dead cell will spring to life if has exactly three live neighbours (reproduction)
"""

UNDERPOPULATION = 2
OVERPOPULATION = 3
REPRODUCTION = 3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
            self.new_state = 1.
        elif self.state == 1. and (num_neighbours < UNDERPOPULATION or num_neighbours > OVERPOPULATION):
            self.new_state = 0
        else: self.new_state = self.state

class Universe:
    def __init__(self, dim):
        self.width, self.height = dim
        self.world = createWorld(self.width, self.height)
        self.worldArray = toArray(self.world)
        self.worldList = [self.worldArray]
    def generation(self):
        for y in range(self.height):
            for x in range(self.width):
                neighbours = countNeighbours(self.world, self.world[x][y])
                self.world[x][y].calcSurvival(neighbours)

    def updateWorld(self):
        for y in range(self.height):
            for x in range(self.width):
                self.world[x][y].updateState()

        self.worldArray = toArray(self.world)
        self.worldList.append(self.worldArray)

def createWorld(width, height):
    world = [[Cell(x, y, np.random.randint(0, 2)) for y in range(height)] for x in range(width)]
    return(world)

def toArray(world):
    frame = [[world[x][y].state for y in range(len(world[0]))] for x in range(len(world[1]))]
    return(np.array(frame))

def countNeighbours(world, cell):
    numNeighbours = 0
    cols = len(world[0])
    rows = len(world[1])

    for x in range(-1, 2):
        for y in range(-1, 2):
            if cell.x != x and cell.y != y:
                col = (cell.x + x + cols) % cols
                row = (cell.y + y + rows) % rows
                numNeighbours += world[col][row].state

    return(numNeighbours)

def animate_life(dim, n_generations=30, interval=300, save=False):
    # Initialise the universe and seed
    universe = Universe(dim)

    # Animate
    fig = plt.figure(figsize=(6,6))
    plt.axis('off')
    ims = []

    for i in range(n_generations):
        ims.append((plt.imshow(universe.worldArray, cmap='Blues'),))
        universe.generation()
        universe.updateWorld()
        print(f'frame{i}')
        print(len(universe.worldList))



    im_ani = animation.ArtistAnimation(fig, ims, interval=interval, repeat_delay=None,
                                       blit=True)

    # Optional: save the animation, with a name based on the seed.
    if save:
        im_ani.save(('test.mp4'), writer=animation.FFMpegWriter(), dpi=300)

def runEpoch(dim, n_generations=50):
    universe = Universe(dim)
    for i in range(n_generations):
        universe.generation()
        universe.updateWorld()
    return(universe.worldList)

data = [runEpoch((100, 100)) for i in range(10)]
np.save('data.npy', np.array(data))

# animate_life(dim=(200, 200), n_generations=100, interval=1, save=True)
