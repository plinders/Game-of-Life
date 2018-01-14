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

    def update_state(self):
        self.state = self.new_state

    def survival(self, num_neighbours):
        if self.state and not UNDERPOPULATION <= num_neighbours <= OVERPOPULATION:
            self.new_state = 0
        elif num_neighbours == REPRODUCTION:
            self.new_state = 1

def count_neighbours(universe, cell):
    num_neighbours = 0
    cols = len(universe)
    rows = len(universe[0])

    for i in range(cell.x - 1, cell.x + 2):
        for j in range(cell.y - 1, cell.x + 2):
            col = (cell.x + i + cols) % cols
            row = (cell.y + j + rows) % rows
            num_neighbours += universe[col][row].state
    num_neighbours -= cell.state
    return(num_neighbours)

def generation(universe):
    # Simple loop over every possible xy coordinate.
    for x in range(len(universe)):
        for y in range(len(universe[0])):
            neighbours = count_neighbours(universe, universe[x][y])
            universe[x][y].survival(neighbours)

    for x in range(len(universe)):
        for y in range(len(universe[0])):
            universe[x][y].update_state()

    return universe


def animate_life(dim, n_generations=30, interval=300, save=False):
    # Initialise the universe and seed
    universe = []
    for x in range(dim[0]):
        inner = []
        for y in range(dim[1]):
            inner.append(Cell(x, y, np.random.randint(0, 2)))
            universe.append(inner)

    # Animate
    fig = plt.figure()
    plt.axis('off')
    ims = []

    for i in range(n_generations):
        frame = np.zeros((len(universe), len(universe[0])))
        for x in range(len(universe)):
            for y in range(len(universe[0])):
                frame[x, y] = universe[x][y].state

        ims.append((plt.imshow(frame, cmap='Blues'),))
        universe = generation(universe)
        print(f'frame{i}')

    im_ani = animation.ArtistAnimation(fig, ims, interval=interval, repeat_delay=3000,
                                       blit=True)

    # Optional: save the animation, with a name based on the seed.
    if save:
        im_ani.save(('Class_test.mp4'), writer=animation.FFMpegWriter(), dpi=300)


animate_life(dim=(25, 25), n_generations=100, interval=1, save=True)
