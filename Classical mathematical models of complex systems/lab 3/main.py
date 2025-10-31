from math import exp, log, cos, sin, radians
from matplotlib.pyplot import plot, show, legend, subplots, xlabel, ylabel

class error_simulator():  
    def __init__(self, flight_duration, GPS_period, GPS_duration):
        self.flight_duration    = flight_duration
        self.GPS_period         = GPS_period
        self.GPS_duration       = GPS_duration
        self.k                  = - log(1 - 0.95) / GPS_duration
        self.C                  = 0.001
        self.dt                 = 1
        self.errors_list = list()
        self.errors_list_without_correction = list()        
        self.calculate_with_correction()
        self.calculate_without_correction()

    def calculate_with_correction(self):
        error = 0
        self.errors_list.clear()   
        t_local = 0
        for t in range(self.flight_duration):
            if t_local >= self.GPS_period:
                error -= error * (1 - exp(- self.k * self.GPS_duration))
                if t_local - self.GPS_period == self.GPS_duration:
                    t_local = 0
                t_local += 1
            else:
                error += self.C * t_local * self.dt
                t_local += 1
            self.errors_list.append(error)

    def calculate_without_correction(self):
        error = 0
        self.errors_list_without_correction.clear()
        for t in range(self.flight_duration):
            error += self.C * t * self.dt
            self.errors_list_without_correction.append(error)

    def get_errors(self):
        return self.errors_list
    
    def get_errors_without_correction(self):
        return self.errors_list_without_correction
    
    def show_plot(self):
        t = [i for i in range(self.flight_duration)]
        plot(t, self.errors_list, label="Ошибка с комплексированием")
        plot(t, self.errors_list_without_correction, label="Ошибка без комплексирования")
        xlabel("Время")
        ylabel("Ошибка")
        legend()
        show()

class plane():
    def __init__(self):
        self.air_speed          = 300
        self.wind_speed         = 25
        self.aircraft_heading   = radians(90)
        self.wind_direction     = radians(45)
        self.angle_of_attack    = radians(5)
        self.flight_duration    = 16000 
        self.GPS_period         = 1000
        self.GPS_duration       = 10
        self.es = error_simulator(self.flight_duration,
                             self.GPS_period,
                             self.GPS_duration)
        self.x_coords = list()
        self.y_coords = list()
    
    def simulate_flight(self):
        self.x_coords.clear()
        self.y_coords.clear()
        self.x_coords.append(0)
        self.y_coords.append(0)
        for t in range(1, self.flight_duration):
            self.x_coords.append(self.x_coords[-1] + (self.air_speed * cos(self.aircraft_heading) 
                                            + self.wind_speed * cos(self.wind_direction)) * cos(self.angle_of_attack))
            self.y_coords.append(self.y_coords[-1] + (self.air_speed * sin(self.aircraft_heading) 
                                            + self.wind_speed * sin(self.wind_direction)) * cos(self.angle_of_attack))

    def show_plots(self):
        t = [i for i in range(self.flight_duration)]    
        fg, axs = subplots(3, 1)
        x_coords_with_error = [self.x_coords[i] + self.es.get_errors()[i] for i in range(self.flight_duration)]
        x_coords_with_error_without_correction = [self.x_coords[i] + self.es.get_errors_without_correction()[i] for i in range(self.flight_duration)] 
        y_coords_with_error = [self.y_coords[i] + self.es.get_errors()[i] for i in range(self.flight_duration)]
        y_coords_with_error_without_correction = [self.y_coords[i] + self.es.get_errors_without_correction()[i] for i in range(self.flight_duration)] 
        
        axs[0].plot(t, self.x_coords, color='blue', label="Координата x (широта)")
        axs[0].plot(t, x_coords_with_error, color='orange', label="Координата x (широта) с комплексированием",  linestyle='--')
        axs[0].plot(t, x_coords_with_error_without_correction, color='red', label="Координата x (широта) без комплексирования")
        axs[0].legend()
        axs[0].set_xlabel("t")
        axs[0].set_ylabel("x")
        
        axs[1].plot(t, self.y_coords, color='blue', label="Координата y (долгата)")
        axs[1].plot(t, y_coords_with_error, color='orange', label="Координата y (долгата) с комплексированием", linestyle='--')
        axs[1].plot(t, y_coords_with_error_without_correction, color='red', label="Координата y (долгата) без комплексирования")
        axs[1].legend()
        axs[1].set_xlabel("t")
        axs[1].set_ylabel("y")

        axs[2].plot(self.x_coords, self.y_coords, color='blue', label="Маршрут")
        axs[2].plot( x_coords_with_error,  y_coords_with_error, color='orange', label="Маршрут с комплексированием", linestyle='--')
        axs[2].plot(x_coords_with_error_without_correction, y_coords_with_error_without_correction, color='red', label="Маршрут без комплексирования")
        axs[2].legend()
        axs[2].set_xlabel("x")
        axs[2].set_ylabel("y")
        
        show()      

def main():
    p = plane()
    p.simulate_flight()
    p.show_plots()

main()