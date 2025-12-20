from random import random
from enum import Enum
from copy import deepcopy

class State(Enum):
    DEAD  = 0
    ALIVE = 1

class Cell():
    def __init__(self, state = State.DEAD, coords = (0, 0)):
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
        alive_count = sum(1 for c in self.__neighbours if c.state == State.ALIVE)
        self.__next_state = self.__state 

        if self.__state == State.ALIVE and (alive_count > 3 or alive_count < 2):
            self.__next_state = State.DEAD
        
        if self.__state == State.DEAD and (alive_count == 3):
            self.__next_state = State.ALIVE
    
    def apply_next_state(self):
        self.__state = self.__next_state
        
class Tissue():
    def __init__(self, l, h):
        self.__tissue = list()
        self.__l = l
        self.__h = h
        self.__pattern = self.generate_random_pattern()
        self.regenerate(l, h)

    def regenerate(self, l, h):
        self.__l = l
        self.__h = h
        self.__tissue = [[Cell() for _ in range(l)] for _ in range(h)]
        for z in range(h):
            for x in range(l):
                solo_cell = self.__tissue[z][x]
                solo_cell.coords = (x, z)
                solo_cell.state = State(self.__pattern[z][x])
                self.__add_neighbours(solo_cell)
                    
    @property
    def tissue(self):
        return self.__tissue
    
    @tissue.setter
    def tissue(self, value):
        self.__tissue = value
    
    @property
    def l(self):
        return self.__l
    
    @l.setter
    def l(self, value):
        self.__l = value
        
    @property
    def h(self):
        return self.__h
    
    @h.setter
    def h(self, value):
        self.__h = value        
        
    def __add_neighbours(self, solo_cell):
        x, z = solo_cell.coords
        dz_range = (0,) if self.__h == 1 else (-1, 0, 1)
        dx_range = (0,) if self.__l == 1 else (-1, 0, 1)

        for dz in dz_range:
                for dx in dx_range:
                    if dx == 0 and dz == 0:
                        continue
                    nx = (x + dx) % self.__l
                    nz = (z + dz) % self.__h
                    solo_cell.neighbours.append(self.__tissue[nz][nx])
    @property
    def pattern(self):
        return deepcopy(self.__pattern)
    
    @pattern.setter
    def pattern(self, pattern):
        if len(pattern) == self.__h and len(pattern[0]) == self.__l:
            self.__pattern = pattern
            for z in range(self.__h):
                for x in range(self.__l):
                    self.__tissue[z][x].state = State(pattern[z][x]) 

    def compute_next_state(self):
        for z in range(self.__h):
            for x in range(self.__l):
                self.__tissue[z][x].compute_next_state()

    @property
    def cell(self, x, y):
        return self.__tissue[x][y]
        
    def apply_next_state(self):
        for z in range(self.__h):
            for x in range(self.__l):
                self.__tissue[z][x].apply_next_state()
                self.__pattern[z][x] = self.__tissue[z][x].state.value

    def generate_random_pattern(self, density=0.3):
        new_pattern = list()
        for z in range(self.__h):
            new_pattern.append(list())
            for _ in range(self.__l):
                if random() < density:
                    new_pattern[z].append(State.ALIVE.value)
                else:
                    new_pattern[z].append(State.DEAD.value)
        return new_pattern        