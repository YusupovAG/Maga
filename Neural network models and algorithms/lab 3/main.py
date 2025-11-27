from math import sqrt, exp
from random import random, shuffle
import matplotlib.pyplot as plt

class neuron():

    def __init__(self):
        self.__weights = list()
        pass
    
    @property
    def weights(self):
        return self.__weights
    
    @weights.setter
    def weights(self, w):
        self.__weights = w

class cell():
    def __init__(self):
        self.core = neuron()
        self.__coords = (0, 0)
        self.__color = [0, 0, 0]

    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, value):
        self.__coords = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

class K_map():

    def __init__(self, size, input_vect_size):
        self.__cells = list()
        self.__size = size
        self.rebuild(size, input_vect_size)    
        self.__l_rate0 = 0.1
        self.__nh_radius0 = size / 2
        self.__l_rate = self.__l_rate0
        self.__nh_radius = self.__nh_radius0
        
        pass

    def rebuild(self, size, input_vect_size):
        self.__cells.clear()
        for x in range(size):
            for y in range(size):
                self.__cells.append(cell())
                self.__cells[-1].coords = (x, y)
                self.__cells[-1].core.weights = [random() for _ in range(input_vect_size)]

    
    def train(self, data, epochs=10):
        for epoch in range(epochs):
            print(f'Эпоха: {epoch}')
            shuffle(data)
            for x in data:
                winner_index = self.__find_winner(x)

                for j, j_cell in enumerate(self.__cells):
                    nh_influence = self.__nh_func(j, winner_index)

                    for i in range(len(j_cell.core.weights)):
                        j_cell.core.weights[i] += self.__l_rate * nh_influence * (x[i] - j_cell.core.weights[i])

            self.__l_rate = self.__l_rate0 * exp(-epoch / epochs)
            self.__nh_radius = self.__nh_radius0 * exp(-epoch / epochs)

    def __find_winner(self, x):
        d = list()
        for j, current_cell in enumerate(self.__cells):
            d_j = sum([(x[i] - current_cell.core.weights[i])**2 for i, _ in enumerate(x)])
            d.append(d_j)
        return d.index(min(d))

    def __nh_func(self, neuron_index, winner_neuron_index):
        x1, y1 = self.__cells[neuron_index].coords
        x2, y2 = self.__cells[winner_neuron_index].coords
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return exp(- distance ** 2 / (self.__nh_radius ** 2))

    def show(self):
        import numpy as np
        import matplotlib.pyplot as plt

        grid = np.zeros((self.__size, self.__size, 3))

        for c in self.__cells:
            x, y = c.coords
            w = c.core.weights

            rgb = (w + [0, 0, 0])[:3]
            grid[x, y] = rgb

        plt.imshow(grid)
        plt.title("Карта Кохонена")
        plt.axis("off")
        plt.show()


def get_data():
    file_name = "customer_segmentation.csv"
    data = list()
    
    with open(file_name, 'r') as f:
        next(f)
        for line in f:
            row = [float(n) for n in line.split(',')]
            data.append(row)

    return data

def calculate_map_size(data):
    map_size = 5 * sqrt(len(data))
    return round(map_size)
    #return 15

def main():
    data = get_data()
    print(data)

    m = K_map(calculate_map_size(data), len(data[0]))
    m.show()
    m.train(data)
    m.show()
    


main()