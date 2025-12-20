from tissue import Tissue
from matplotlib.pyplot import subplots, show
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue
import time
from copy import deepcopy


def print_queue(q):
    print()
    temp_q = Queue()
    
    while not q.empty():
        item = q.get()
        print(item)
        temp_q.put(item)
    
    
    while not temp_q.empty():
        q.put(temp_q.get())

class SimEvent(ABC):
    def __init__(self, smltr, obj=None):
        self._smltr = smltr
        self._obj = obj

    @abstractmethod
    def execute(self):
        pass


class NextEvent(SimEvent):
    def execute(self):
        #print(f"# Событие Next tick:{self._smltr.tick}")
        if len(self._smltr.memory) - 1 == self._smltr.tick:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))
        else:
            self._smltr.tick += 1


class PrevEvent(SimEvent):
    def execute(self):
        #print(f"# Событие Prev tick:{self._smltr.tick}")
        if self._smltr.tick > 0:
            self._smltr.tick -= 1


class EventB(SimEvent):
    def execute(self):
        #print(f"### Событие B tick:{self._smltr.tick}")
        for z in range(self._obj.h):
            for x in range(self._obj.l):
                self._smltr.events_queue.put(
                    EventA(self._smltr, self._obj.tissue[z][x])
                )
        self._smltr.events_queue.put(EventC(self._smltr, self._obj))


class EventA(SimEvent):
    def execute(self):
        #print(f"##### Событие A")
        self._obj.compute_next_state()
        self._smltr.targeted_x, self._smltr.targeted_z = self._obj.coords


class EventC(SimEvent):
    def execute(self):
        #print(f"### Событие C tick:{self._smltr.tick}")
        self._obj.apply_next_state()
        self._smltr.memory.append(self._obj.pattern)
        self._smltr.tick += 1
        if self._smltr.play:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))


class PlayEvent(SimEvent):
    def execute(self):
        if not self._smltr.play:
            self._smltr.events_queue.put(EventB(self._smltr, self._obj))
        self._smltr.play = not self._smltr.play


class Simulator():
    def __init__(self, tissue: Tissue):
        self.tissue = tissue
        self.events_queue = Queue()
        self.tick = 0
        self.memory = [tissue.pattern]
        self.play = False
        self.__img = None

        self.targeted_x = 0
        self.targeted_z = 0
        _, self.__ax = subplots(1, 4)
        self.__ax[1].set_title(f'Tick: {self.tick}')

        self.__next_button = Button(self.__ax[2], '> (1)')
        self.__prev_button = Button(self.__ax[0], '< (-1)')
        self.__play_button = Button(self.__ax[3], '|>')

        self.__next_button.on_clicked(self.__next)
        self.__prev_button.on_clicked(self.__prev)
        self.__play_button.on_clicked(self.__play)

        self.__ax[1].tick_params(
            top=False, bottom=False, left=False, right=False,
            labelleft=False, labelbottom=False
        )

        self.__img = self.__ax[1].imshow(
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
            print_queue(self.events_queue)
            time.sleep(0.1)

    def start_simulation(self, duration):
        self.t = Thread(target=self.update_queue, daemon=True)
        self.t.start()
        
        show()

    def update_plot(self):
        self.__next_button.label.set_text(f'> ({self.tick + 1})')
        self.__prev_button.label.set_text(f'< ({self.tick - 1})')
        self.__play_button.label.set_text('||' if self.play else '|>')
        self.__next_button.set_active(False if self.play else True)
        self.__prev_button.set_active(False if self.play else True)
        
        p = deepcopy(self.memory[self.tick])
        p[self.targeted_z][self.targeted_x] += 2
        
        if 0 <= self.tick < len(self.memory):
            self.__img.set_data(p)

        self.__ax[1].set_title(f'Tick: {self.tick}')
        self.__img.figure.canvas.draw_idle()

    def __next(self, event):
        self.events_queue.put(NextEvent(self, self.tissue))

    def __prev(self, event):
        self.events_queue.put(PrevEvent(self, self.tissue))

    def __play(self, event):
        self.events_queue.put(PlayEvent(self, self.tissue))


def simulation():
    t = Tissue(5, 5)
    s = Simulator(t)
    s.start_simulation(30)


def main():
    simulation()


main()
