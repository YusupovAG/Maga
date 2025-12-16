from tissue import Tissue
from matplotlib.pyplot import subplots, show, pause
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
from abc import ABC, abstractmethod
from copy import deepcopy

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
        
class NextEvent(SimEvent):
    def execute(self):
        self._smltr.next()

class PrevEvent(SimEvent):
    def execute(self):
        self._smltr.prev()


class Simulator():
    def __init__(self, tissue: Tissue):
        self.__tissue = tissue
        self.__events_queue = list()
        self.__tick = 0
        self.__fig, self.__ax = subplots(1, 3)
        self.__next_button = Button(self.__ax[2], '> ({1})')
        self.__prev_button = Button(self.__ax[0], '< ({-1})')
        self.__next_button.on_clicked(self.__next)
        self.__prev_button.on_clicked(self.__prev)
        
        self.__img = None
        self.__memory = [deepcopy(tissue.pattern)]
          
    def compute_next(self):
        self.__tissue.compute_next_state()

    def apply_next(self):
        self.__tissue.apply_next_state()

    def start_generation(self):
        self.__events_queue.append(ComputeEvent(self.__tick, self))
        self.__events_queue.append(ApplyEvent(self.__tick, self))
        self.__tick += 1
        self.__events_queue.append(GenerationStartEvent(self.__tick, self))
        self.show()
        
    def start_simulation(self, duration):
        self.__events_queue.append(GenerationStartEvent(self.__tick, self))
        for i in range(duration):
            e = self.__events_queue.pop(0)
            e.execute()

    def show(self): 
        grid = [[self.__memory[self.__tick][z][x].value for x in range(self.__tissue.l)] for z in range(self.__tissue.h)]
        print(f"show {self.__tick}")
        if self.__img is None:        
            self.__img = self.__ax[1].imshow(
                grid,
                cmap=ListedColormap(['white', 'green']),
                vmin=0,
                vmax=1
            )
            self.__ax[1].axis('off')
        else:
            self.__img.set_data(grid)
        pause(0.01)

    def __next(self, event):
        if len(self.__memory) - 1 == self.__tick:
            ComputeEvent(self.__tick, self).execute()
            ApplyEvent(self.__tick, self).execute()
            self.__memory.append(deepcopy(self.__tissue.pattern))
          
        self.__tick += 1
        self.__next_button.label.set_text(f'> ({self.__tick + 1})')
        self.__prev_button.label.set_text(f'< ({self.__tick - 1})')
        print(len(self.__memory))
        self.show()
    
    def __prev(self, event):
        if self.__tick > 0:
            self.__tick -= 1
            self.__next_button.label.set_text(f'> ({self.__tick + 1})')
            self.__prev_button.label.set_text(f'< ({self.__tick - 1})')
            print(len(self.__memory))
            self.show()


def simulation():
    t = Tissue(30, 30)
    s = Simulator(t)
    s.show()
    show()
    

def main():
    simulation()

main()