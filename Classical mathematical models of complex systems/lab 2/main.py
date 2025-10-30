from math import cos, pi, sin
from matplotlib.pyplot import plot, show, xlabel, ylabel
from random import randint

def start():
    tau = 1.0
    t_end = 59
    V_air = 10
    V_wind = 2
    K_angle = 0
    A_angle = 0
    d = 2 * pi
    x = [0]
    y = [0]
    for t in range(t_end):
        x.append(x[-1] + (V_air * cos(K_angle) + V_wind * cos(d)) * cos(A_angle))
        y.append(y[-1] + (V_air * sin(K_angle) + V_wind * sin(d)) * cos(A_angle))

    plot(x, y)
    xlabel("Широта")
    ylabel("Долгота")
    show()

def main():
    tau = 1.0
    t_end = 59
    V_air = 10
    V_wind = 2
    K_angle = 0
    A_angle = 0
    d = 60

    start()
    

main()