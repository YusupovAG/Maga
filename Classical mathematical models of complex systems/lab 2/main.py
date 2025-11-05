from math import exp, log
from matplotlib.pyplot import plot, show, xlabel, ylabel, legend

class error_simulator():
    def __init__(self, flight_duration, GPS_period, GPS_duration):
        self.flight_duration = flight_duration
        self.GPS_period = GPS_period
        self.GPS_duration = GPS_duration
        self.k = - log(1 - 0.95) / GPS_duration
        self.C = 0.001
        self.dt = 1
        self.errors_list = list()
        self.errors_list_wihout_correction = list()        
        self.calculate_with_correction()
        self.calculate_without_correction()

    def calculate_with_correction(self):
        error = 0
        self.errors_list.clear()   
        t_local = 0
        for t in range(self.flight_duration):
            if t_local >= self.GPS_period:
                error -= error * (1 - exp(- self.k * self.dt))
                if t_local - self.GPS_period == self.GPS_duration:
                    t_local = 0
                t_local += 1
            else:
                error += self.C * t_local * self.dt
                t_local += 1
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
        plot(t, self.errors_list, label="Ошибка с комплексированием")
        plot(t, self.errors_list_wihout_correction, label="Ошибка без комплексирования")
        xlabel("Время")
        ylabel("Ошибка")
        legend()
        show()

def main():
    es = error_simulator(200, 50, 10)
    es.show_plot()

main()