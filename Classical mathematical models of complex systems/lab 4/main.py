from tissue import Tissue
from matplotlib.pyplot import subplots, show
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue
import time
from copy import deepcopy

class SimEvent(ABC):
    def __init__(self, smltr, obj=None):
        self._smltr = smltr
        self._obj = obj

    @abstractmethod
    def execute(self):
        pass

class NextEvent(SimEvent):
    def execute(self):
        if len(self._smltr.memory) - 1 == self._smltr.tick:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))
        else:
            self._smltr.tick += 1

class PrevEvent(SimEvent):
    def execute(self):
        if self._smltr.tick > 0:
            self._smltr.tick -= 1

class EventB(SimEvent):
    def execute(self):
        for z in range(self._obj.h):
            for x in range(self._obj.l):
                self._smltr.events_queue.put(
                    EventA(self._smltr, self._obj.tissue[z][x])
                )
        self._smltr.events_queue.put(EventC(self._smltr, self._obj))

class EventA(SimEvent):
    def execute(self):
        self._obj.compute_next_state()
        self._smltr.targeted_x, self._smltr.targeted_z = self._obj.coords
        if self._smltr.show_event_A:
            time.sleep(0.9)

class EventC(SimEvent):
    def execute(self):
        self._obj.apply_next_state()
        self._smltr.memory.append(self._obj.pattern)
        self._smltr.tick += 1
        if self._smltr.play:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))
            time.sleep(0.03)

class PlayEvent(SimEvent):
    def execute(self):
        if not self._smltr.play:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))
        self._smltr.play = not self._smltr.play
        
class ChangeShowingAEvent(SimEvent):
    def execute(self):
        self._smltr.show_event_A = not self._smltr.show_event_A

class Simulator():
    def __init__(self, tissue: Tissue):
        self.tissue = tissue
        self.events_queue = Queue()
        self.tick = 0
        self.memory = [tissue.pattern]
        self.play = False
        self.__img = None
        self.show_event_A = False

        self.targeted_x = 0
        self.targeted_z = 0
        _, self.__ax = subplots()
        self.__ax.set_title(f'Tick: {self.tick}')
         
        prev_button_ax = self.__ax.figure.add_axes([0.35, 0.05, 0.08, 0.05])
        next_button_ax = self.__ax.figure.add_axes([0.45, 0.05, 0.08, 0.05])
        play_button_ax = self.__ax.figure.add_axes([0.55, 0.05, 0.08, 0.05])
        A_button_ax = self.__ax.figure.add_axes([0.65, 0.05, 0.08, 0.05])

        self.__next_button = Button(next_button_ax, '>')
        self.__prev_button = Button(prev_button_ax, '<')
        self.__play_button = Button(play_button_ax, '|>')
        self.__A_button = Button(A_button_ax, 'A')

        self.__next_button.on_clicked(self.__next)
        self.__prev_button.on_clicked(self.__prev)
        self.__play_button.on_clicked(self.__play)
        self.__A_button.on_clicked(self.__change_A)

        self.__ax.tick_params(
            top=False, bottom=False, left=False, right=False,
            labelleft=False, labelbottom=False
        )

        self.__img = self.__ax.imshow(
            self.memory[self.tick],
            cmap=ListedColormap(['white', 'green', 'gray', '#006400']),
            vmin=0,
            vmax=3,
            interpolation='nearest'
        )

    def update_queue(self):
        while True:
            e = self.events_queue.get()
            e.execute()
            self.update_plot()
                     
    def start_simulation(self):
        self.t = Thread(target=self.update_queue, daemon=True)
        self.t.start()    
        show()

    def update_plot(self):
        self.__play_button.label.set_text('||' if self.play else '|>')
        self.__A_button.label.set_text('-A' if self.show_event_A else 'A')
        self.__next_button.set_active(False if self.play else True)
        self.__prev_button.set_active(False if self.play else True)

        p = self.memory[self.tick]
        if self.show_event_A:
            p = deepcopy(self.memory[self.tick])
            p[self.targeted_z][self.targeted_x] += 2
        
        if 0 <= self.tick < len(self.memory):
            self.__img.set_data(p)

        self.__ax.set_title(f'Tick: {self.tick}')
        self.__img.figure.canvas.draw_idle()

    def __next(self, event):
        self.events_queue.put(NextEvent(self, self.tissue))

    def __prev(self, event):
        self.events_queue.put(PrevEvent(self, self.tissue))

    def __play(self, event):
        self.events_queue.put(PlayEvent(self, self.tissue))

    def __change_A(self, event):
        self.events_queue.put(ChangeShowingAEvent(self)) 
        
def simulation():
    t = Tissue(10, 10)
    '''t.pattern = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
                 [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]'''
    s = Simulator(t)
    s.start_simulation()

def main():
    simulation()

main()
