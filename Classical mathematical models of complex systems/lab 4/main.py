from enum import Enum
from matplotlib.pyplot import subplots, show, pause
from matplotlib.colors import ListedColormap
from abc import ABC, abstractmethod
import random

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
        self.__fig, self.__ax = subplots()
        self.__img = None
        self.regenerate(l, h)

    def regenerate(self, l, h):
        self.__l = l
        self.__h = h
        self.__tissue = [[Cell() for _ in range(l)] for _ in range(h)]
        for z in range(h):
                for x in range(l):
                    solo_cell = self.__tissue[z][x]
                    solo_cell.coords = (x, z)
                    self.__add_neighbours(solo_cell)

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

    def set_start_pattern(self, pattern):
        if len(pattern) == self.__h and len(pattern[0]) == self.__l:
            for z in range(self.__h):
                    for x in range(self.__l):
                        self.__tissue[z][x].state = pattern[z][x]
                        self.__tissue[z][x].next_state = pattern[z][x]

    def compute_next_state(self):
        for z in range(self.__h):
                for x in range(self.__l):
                    self.__tissue[z][x].compute_next_state()
    
    def apply_next_state(self):
        for z in range(self.__h):
                for x in range(self.__l):
                    self.__tissue[z][x].apply_next_state()

    def show(self):  
        grid = [[self.__tissue[z][x].state.value for x in range(self.__l)] for z in range(self.__h)]
        
        if self.__img is None:        
            self.__img = self.__ax.imshow(
                grid,
                cmap=ListedColormap(['white', 'green']),
                vmin=0,
                vmax=1
            )
            self.__ax.axis('off')
        else:
            self.__img.set_data(grid)
        pause(0.01)

    def set_random_pattern(self, density=0.3):
        for z in range(self.__h):
            for x in range(self.__l):
                if random.random() < density:
                    self.__tissue[z][x].state = State.ALIVE
                    self.__tissue[z][x].next_state = State.ALIVE
    
class SimEvent(ABC):
    def __init__(self, tick, smltr):
        self._tick = tick
        self._smltr = smltr

    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def log(self):
        pass

    @property
    def tick(self):
        return self._tick
    
    @tick.setter
    def tick(self, value):
        self._tick = value

class GenerationStartEvent(SimEvent):
    def execute(self):
        self._smltr.start_generation()
     
    def log(self):
        print(f'Generation start: tick: {self._tick}')

class ComputeEvent(SimEvent):
    def execute(self):
        self._smltr.compute_next()
      
    def log(self):
        print(f'Compute: tick: {self._tick}')

class ApplyEvent(SimEvent):
    def execute(self):
        self._smltr.apply_next()

    def log(self):
        print(f'Apply state: tick: {self._tick}')

class Simulator():
    def __init__(self, tissue: Tissue, duration):
        self.__tissue = tissue
        self.__events_queue = list()
        self.__tick = 0
        self.__duration = duration
  
    def compute_next(self):
        self.__tissue.compute_next_state()

    def apply_next(self):
        self.__tissue.apply_next_state()

    def start_generation(self):
        self.__events_queue.append(ComputeEvent(self.__tick, self))
        self.__events_queue.append(ApplyEvent(self.__tick, self))
        self.__tick += 1
        self.__events_queue.append(GenerationStartEvent(self.__tick, self))
        self.__tissue.show()
        
    def start_simulation(self):
        self.__events_queue.append(GenerationStartEvent(self.__tick, self))
        for i in range(self.__duration):
            e = self.__events_queue.pop(0)
            e.execute()

def simulation():
    t = Tissue(30, 30)
    t.set_random_pattern()
    s = Simulator(t, 1000)
    s.start_simulation()
    show()

def main():
    simulation()

main()