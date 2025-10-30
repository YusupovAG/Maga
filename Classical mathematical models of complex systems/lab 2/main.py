from math import exp, cos, pi, sin, log
from matplotlib.pyplot import plot, show, xlabel, ylabel, subplots
from random import randint


class error_simulator():
    def __init__(self, flight_duration, GPS_period, GPS_duration):
        self.flight_duration = flight_duration
        self.GPS_period = GPS_period
        self.GPS_duration = GPS_duration
        self.k = 0.001 # - log(0.05)
        self.C = 0.001
        self.dt = 1
        self.errors_list = list()
        self.errors_list_wihout_correction = list()        
        self.calculate_with_correction()
        self.calculate_without_correction()

    def calculate_with_correction(self):
        error = 0
        self.errors_list.clear()

        gps = False
        gps_counter = 0

        for t in range(self.flight_duration):
            if t % self.GPS_period == 0 and t != 0:
                gps = True
                
            if gps:
                print(t)
                print(f'{1 - exp(- self.k * self.GPS_duration)}')
                error -= error * (1 - exp(- self.k * self.GPS_duration))
                gps_counter += 1
                if gps_counter == self.GPS_duration:
                    gps = False
            else:
                error += self.C * t * self.dt

            self.errors_list.append(error)

    def calculate_without_correction(self):
        error = 0
        self.errors_list_wihout_correction.clear()
        for t in range(self.flight_duration):
            error += self.C * t * self.dt
            self.errors_list_wihout_correction.append(error)

    def get_errors(self):
        return self.errors_list
    
    def get_errors_without_correction(self):
        return self.errors_list_wihout_correction
    
    def show_plot(self):
        t = [i for i in range(self.flight_duration)]
        print(self.errors_list)
        print(self.errors_list_wihout_correction)
        plot(t, self.errors_list)
        plot(t, self.errors_list_wihout_correction)
        xlabel("Время")
        ylabel("Ошибка")
        show()


class plane():
    def __init__(self):
        pass

    def read():
        pass

def start():
    tau = 1.0
    t_end = 68
    V_air = 10
    V_wind = 2
    K_angle = 0
    A_angle = 0
    d = pi
    x = [0]
    y = [0]
    for t in range(t_end):
        x.append(x[-1] + (V_air * cos(K_angle) + V_wind * cos(d)) * cos(A_angle))
        y.append(y[-1] + (V_air * sin(K_angle) + V_wind * sin(d)) * cos(A_angle))
    return x
    #plot(x, y)
    #xlabel("Широта")
    #ylabel("Долгота")
    #show()

def main():
    es = error_simulator(69, 59, 10)
    es.show_plot()
    t = [i for i in range(69)]
    m = start()    
    fg, axs =  subplots(1, 3)
    axs[0].plot(t, m, color='blue')
    axs[0].plot(t, [m[i] + es.get_errors()[i] for i in range(len(t))], color='yellow')

    axs[1].plot(t, m, color='blue')
    axs[1].plot(t, [m[i] + es.get_errors_without_correction()[i] for i in range(len(t))], color='red')
    
    axs[2].plot(t, m, color='blue')
    axs[2].plot(t, [m[i] + es.get_errors()[i] for i in range(len(t))], color='yellow')
    axs[2].plot(t, [m[i] + es.get_errors_without_correction()[i] for i in range(len(t))], color='red')
    
    show()
main()