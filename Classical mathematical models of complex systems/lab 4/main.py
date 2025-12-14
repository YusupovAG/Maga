from enum import Enum
from matplotlib.pyplot import subplots, show
class state(Enum):
    DEAD  = 0
    ALIVE = 1

class cell():

    def __init__(self, state = state.ALIVE, coords = (0, 0, 0)):
        self.__state = state
        self.__next_state = state
        self.__neighbours = list()
        self.__coords = coords

    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def next_state(self):
        return self.__next_state
    
    @next_state.setter
    def next_state(self, value):
        self.__next_state = value

    @property
    def coords(self):
        return self.__coords
    
    @coords.setter
    def coords(self, value):
        self.__coords = value

    @property
    def neighbours(self):
        return self.__neighbours

    @neighbours.setter
    def neighbours(self, value):
        self.__neighbours = value

    def compute_next_state(self):
        alive_count = len([c for c in self.__neighbours if c.state == state.ALIVE])

        self.__next_state = self.__state 

        if self.__state == state.ALIVE and (alive_count > 3 or alive_count < 2):
            self.__next_state = state.DEAD
        
        if self.__state == state.DEAD and (alive_count == 3):
            self.__next_state = state.ALIVE
    
    def apply_next_state(self):
        self.__state = self.__next_state
        
class tissue():

    def __init__(self, l, w, h):
        self.__tissue = list()
        self.__l = l
        self.__w = w
        self.__h = h
        self.__start_pattern = list()
        self.regenerate(l, w, h)

    def regenerate(self, l, w, h):
        self.__l = l
        self.__w = w
        self.__h = h
        self.__tissue = [[[cell() for _ in range(l)] for _ in range(w)] for _ in range(h)]
        for z in range(h):
            for y in range(w):
                for x in range(l):
                    solo_cell = self.__tissue[z][y][x]
                    solo_cell.coords = (x, y, z)
                    self.__add_neighbours(solo_cell)

    def __add_neighbours(self, solo_cell):
        x, y, z = solo_cell.coords
        ngbrs = []

        dz_range = (0,) if self.__h == 1 else (-1, 0, 1)
        dy_range = (0,) if self.__w == 1 else (-1, 0, 1)
        dx_range = (0,) if self.__l == 1 else (-1, 0, 1)

        for dz in dz_range:
            for dy in dy_range:
                for dx in dx_range:

                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    nx = (x + dx) % self.__l
                    ny = (y + dy) % self.__w
                    nz = (z + dz) % self.__h

                    ngbrs.append(self.__tissue[nz][ny][nx])

        solo_cell.neighbours = ngbrs

    def set_start_pattern(self, pattern):

        print(self.__h, self.__w, self.__l)
        print(len(pattern), len(pattern[0]), len(pattern[0][0]))
        if not (
            len(pattern) != self.__h or
            len(pattern[0]) != self.__w or
            len(pattern[0][0]) != self.__l
        ):
            for z in range(self.__h):
                for y in range(self.__w):
                    for x in range(self.__l):
                        self.__tissue[z][y][x].state = pattern[z][y][x]
                        self.__tissue[z][y][x].next_state = pattern[z][y][x]  
        for i in self.__tissue[0][0][0].neighbours:
            print(i.coords)

    def next_state(self):
        for z in range(self.__h):
            for y in range(self.__w):
                for x in range(self.__l):
                    self.__tissue[z][y][x].compute_next_state()
        for z in range(self.__h):
            for y in range(self.__w):
                for x in range(self.__l):
                    self.__tissue[z][y][x].apply_next_state()

    def show(self):
        if self.__h > 1:
            fig, ax = subplots(subplot_kw={"projection": "3d"})
            for z in range(self.__h):
                for y in range(self.__w):
                    for x in range(self.__l):
                        cell_state = self.__tissue[z][y][x].state
                        color = 'green' if cell_state == state.ALIVE else 'red'
                        ax.scatter(x, y, z, c=color, s=100, alpha=0.8)
            
        else:
            fig, ax = subplots()
            for z in range(self.__h):
                for y in range(self.__w):
                    for x in range(self.__l):
                        cell_state = self.__tissue[z][y][x].state
                        color = 'green' if cell_state == state.ALIVE else 'red'
                        ax.scatter(x, y, c=color, s=100, alpha=0.8)
        show()

    

def simulation():
    t = tissue(8, 10, 1)
    '''t.set_start_pattern(
        [[[state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
        [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.ALIVE, state.ALIVE, state.ALIVE, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.ALIVE, state.ALIVE, state.ALIVE, state.ALIVE, state.ALIVE],
         [state.DEAD, state.DEAD, state.ALIVE, state.ALIVE, state.DEAD, state.ALIVE, state.ALIVE, state.ALIVE],
         [state.DEAD, state.DEAD, state.DEAD, state.ALIVE, state.ALIVE, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD]]]
    )'''
    '''t.set_start_pattern([[[state.DEAD, state.ALIVE, state.DEAD],
                          [state.DEAD, state.ALIVE, state.DEAD],
                          [state.DEAD, state.ALIVE, state.DEAD]]])'''
    
    '''t.set_start_pattern(
        [[[state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.ALIVE, state.ALIVE, state.ALIVE, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD],
         [state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD, state.DEAD]]]
    )'''

    for i in range(1000):
        t.show()
        t.next_state()

def main():
    simulation()

main()