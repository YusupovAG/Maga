from math import exp, log, cos, sin, radians
from matplotlib.pyplot import plot, show, legend, subplots, xlabel, ylabel

# --------------------------------------------------------------
# Класс error_simulator моделирует накопление ошибки навигации
# инерциальной системы с учётом периодического GPS-корректирования
# --------------------------------------------------------------
class error_simulator():  
    def __init__(self, flight_duration, GPS_period, GPS_duration):
        # Основные параметры симуляции
        self.flight_duration    = flight_duration       # продолжительность полета (в шагах)
        self.GPS_period         = GPS_period            # период между GPS-коррекциями
        self.GPS_duration       = GPS_duration          # длительность GPS-коррекции (в шагах)
        # Коэффициент экспоненциального затухания ошибки во время GPS-коррекции
        self.k                  = - log(1 - 0.95) / GPS_duration
        # Коэффициент накопления ошибки ИНС
        self.C                  = 0.001
        self.dt                 = 1                     # шаг моделирования по времени
        # Списки для хранения значений ошибок
        self.errors_list = list()                       # ошибки с GPS-коррекцией
        self.errors_list_without_correction = list()    # ошибки без GPS-коррекции
        
        # Сразу при создании объекта выполняется расчет ошибок
        self.calculate_with_correction()
        self.calculate_without_correction()

    # ----------------------------------------------------------
    # Расчёт ошибки координат при наличии GPS-корректирования
    # ----------------------------------------------------------
    def calculate_with_correction(self):
        error = 0               # начальная ошибка
        self.errors_list.clear()   
        t_local = 0             # локальное время между коррекциями

        for t in range(self.flight_duration):
            # Когда проходит период GPS_period, активируется коррекция
            if t_local >= self.GPS_period:
                # Ошибка уменьшается экспоненциально в течение GPS_duration
                error -= error * (1 - exp(- self.k * self.GPS_duration))
                # После завершения интервала GPS-коррекции сбрасываем локальное время
                if t_local - self.GPS_period == self.GPS_duration:
                    t_local = 0
                t_local += 1
            else:
                # Рост ошибки в обычном режиме (ИНС)
                # Ошибка увеличивается пропорционально времени (квадратичная зависимость)
                error += self.C * t_local * self.dt
                t_local += 1

            # Сохраняем значение ошибки для текущего момента времени
            self.errors_list.append(error)

    # ----------------------------------------------------------
    # Расчёт ошибки без GPS-коррекции (только инерциальная система)
    # ----------------------------------------------------------
    def calculate_without_correction(self):
        error = 0
        self.errors_list_without_correction.clear()
        for t in range(self.flight_duration):
            # Ошибка растёт по квадратичному закону: e(t) ~ C * t²
            error += self.C * t * self.dt
            self.errors_list_without_correction.append(error)

    # Методы для получения списков ошибок
    def get_errors(self):
        return self.errors_list
    
    def get_errors_without_correction(self):
        return self.errors_list_without_correction
    
    # ----------------------------------------------------------
    # Визуализация роста ошибки со временем
    # ----------------------------------------------------------
    def show_plot(self):
        t = [i for i in range(self.flight_duration)]
        # С GPS-комплексированием (ошибка уменьшается периодически)
        plot(t, self.errors_list, label="Ошибка с комплексированием")
        # Без GPS — непрерывное накопление ошибки
        plot(t, self.errors_list_without_correction, label="Ошибка без комплексирования")
        xlabel("Время")
        ylabel("Ошибка")
        legend()
        show()

# --------------------------------------------------------------
# Класс plane моделирует движение самолета с учетом ветра,
# угла атаки и навигационных ошибок
# --------------------------------------------------------------
class plane():
    def __init__(self):
        # Основные параметры полёта и среды
        self.air_speed          = 300          # скорость самолета, м/с
        self.wind_speed         = 25           # скорость ветра, м/с
        self.aircraft_heading   = radians(90)  # курс самолета (в радианах)
        self.wind_direction     = radians(45)  # направление ветра (в радианах)
        self.angle_of_attack    = radians(5)   # угол атаки (в радианах)
        self.flight_duration    = 16000        # длительность полета (в шагах)
        self.GPS_period         = 1000         # период GPS-коррекции
        self.GPS_duration       = 10           # длительность коррекции

        # Создание объекта симулятора ошибок
        self.es = error_simulator(self.flight_duration,
                                  self.GPS_period,
                                  self.GPS_duration)
        # Координаты полета
        self.x_coords = list()
        self.y_coords = list()
    
    # ----------------------------------------------------------
    # Моделирование траектории полета
    # ----------------------------------------------------------
    def simulate_flight(self):
        self.x_coords.clear()
        self.y_coords.clear()
        # Начальные координаты (точка старта)
        self.x_coords.append(0)
        self.y_coords.append(0)
        # Интегрирование пути с учетом ветра и угла атаки
        for t in range(1, self.flight_duration):
            self.x_coords.append(self.x_coords[-1] + 
                (self.air_speed * cos(self.aircraft_heading) 
               + self.wind_speed * cos(self.wind_direction)) * cos(self.angle_of_attack))
            self.y_coords.append(self.y_coords[-1] + 
                (self.air_speed * sin(self.aircraft_heading) 
               + self.wind_speed * sin(self.wind_direction)) * cos(self.angle_of_attack))

    # ----------------------------------------------------------
    # Визуализация координат полета и влияния ошибок
    # ----------------------------------------------------------
    def show_plots(self):
        t = [i for i in range(self.flight_duration)]    
        fg, axs = subplots(3, 1)

        # Координаты с ошибками (с коррекцией и без)
        x_coords_with_error = [self.x_coords[i] + self.es.get_errors()[i] for i in range(self.flight_duration)]
        x_coords_with_error_without_correction = [self.x_coords[i] + self.es.get_errors_without_correction()[i] for i in range(self.flight_duration)] 
        y_coords_with_error = [self.y_coords[i] + self.es.get_errors()[i] for i in range(self.flight_duration)]
        y_coords_with_error_without_correction = [self.y_coords[i] + self.es.get_errors_without_correction()[i] for i in range(self.flight_duration)] 
        
        # --- График изменения координаты X ---
        axs[0].plot(t, self.x_coords, color='blue', label="Координата x (широта)")
        axs[0].plot(t, x_coords_with_error, color='orange', label="Координата x (широта) с комплексированием", linestyle='--')
        axs[0].plot(t, x_coords_with_error_without_correction, color='red', label="Координата x (широта) без комплексирования")
        axs[0].legend()
        axs[0].set_xlabel("t")
        axs[0].set_ylabel("x")
        
        # --- График изменения координаты Y ---
        axs[1].plot(t, self.y_coords, color='blue', label="Координата y (долгота)")
        axs[1].plot(t, y_coords_with_error, color='orange', label="Координата y (долгота) с комплексированием", linestyle='--')
        axs[1].plot(t, y_coords_with_error_without_correction, color='red', label="Координата y (долгота) без комплексирования")
        axs[1].legend()
        axs[1].set_xlabel("t")
        axs[1].set_ylabel("y")

        # --- График маршрута полета ---
        axs[2].plot(self.x_coords, self.y_coords, color='blue', label="Маршрут без ошибок")
        axs[2].plot(x_coords_with_error, y_coords_with_error, color='orange', label="Маршрут с комплексированием", linestyle='--')
        axs[2].plot(x_coords_with_error_without_correction, y_coords_with_error_without_correction, color='red', label="Маршрут без комплексирования")
        axs[2].legend()
        axs[2].set_xlabel("x")
        axs[2].set_ylabel("y")
        
        show()      

# --------------------------------------------------------------
# Основная функция: создание объекта самолета, моделирование полета
# и построение всех графиков
# --------------------------------------------------------------
def main():
    p = plane()
    p.simulate_flight()
    p.show_plots()

main()
