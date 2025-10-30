import argparse
import yfinance as yf
import matplotlib.pyplot as plt
from math import exp, log, log10, sqrt
from datetime import timedelta, datetime
import sys

def MSE(f_x, y):
    n = len(f_x)
    return sum([(f_x[i] - y[i]) ** 2 for i in range(n)]) / n

def correlation_coefficient(x, y):
    n = len(x)
    avg_x = sum(x) / len(x)
    avg_y = sum(y) / len(y)
    d1 = sum([(x[i] - avg_x) * (y[i] - avg_y) for i in range(n)])
    d2 = sqrt(sum([(x[i] - avg_x) ** 2 for i in range(n)]) * sum([(y[i] - avg_y) ** 2 for i in range(n)]))
    return d1 / d2

def coefficient_of_determination(f_x, y):
    n = len(y)
    avg_y = sum(y) / len(y)
    S_full = sum([(y[i] - avg_y) ** 2 for i in range(n)])
    S_residual = sum([(y[i] - f_x[i]) ** 2 for i in range(n)])
    return 1 - S_residual / S_full

def gaussian_elimination(a, y):
    M = len(y)
    N = len(a)
    
    for k in range(N):
        y[k] = y[k] / a[k][k]
        a[k] = [a[k][j] / a[k][k] for j in range(N)]
        for i in range(k + 1, M):
            y[i] = y[i] / a[i][k] - y[k]
            for j in range(k + 1, N):
                if not (a[i][k] == 0):
                    a[i][j] = a[i][j] / a[i][k] - a[k][j]
            a[i][k] = a[i][k] / a[i][k] - a[k][k]
    res = {}
    res[f'x_{N - 1}'] = y[N - 1]

    for i in range(M - 2, -1, -1):
        sum = 0
        for j in range(N - 1, i, -1):
            sum += a[i][j] * res[f'x_{j}']
        res[f'x_{i}'] = y[i] - sum
    return res

def normal_equation_matrix(x, y, degree):
    A = [[sum(xi**(i+j) for xi in x) for j in range(degree + 1)] for i in range(degree + 1)]
    B = [sum(y[i] * x[i]**j for i in range(len(x))) for j in range(degree + 1)]
    return A, B

def polynomial_regression_coefficients(x, y, degree=6):
    try:
        A, B = normal_equation_matrix(x, y, degree)
        result = gaussian_elimination(A, B)
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов полиномиальной регрессии: {e}")
        return {f'a_{i + 1}': 0 for i in range(len(result))}
    return {f'a_{i + 1}': result[f'x_{i}'] for i in range(len(result))}

def linear_regression_coefficients(x, y):    
    try:
        A, B = normal_equation_matrix(x, y, degree=1)
        result = gaussian_elimination(A, B)
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов линейной регрессии: {e}")
        return {'a_1': 0, 'a_2': 0}
    
    return {'a_1': result['x_0'], 'a_2': result['x_1']}

def parabolic_regression_coefficients(x, y):
    try:
        A, B = normal_equation_matrix(x, y, degree=2)
        result = gaussian_elimination(A, B)
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов параболической регрессии: {e}")
        return {'a_1': 0, 'a_2': 0, 'a_3': 0}
    
    return {'a_1': result['x_0'], 'a_2': result['x_1'], 'a_3': result['x_2']}

def exponential_regression_coefficients(x, y):
    try:
        M = len(y)
        y_logs = [log(y[i]) for i in range(M)]
        linear_coefs = linear_regression_coefficients(x, y_logs)
        a_2, a_1 = linear_coefs['a_2'], exp(linear_coefs['a_1']) 
        
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов эксп регрессии: {e}")
        return {'a_1': 1, 'a_2': 1}
    return {'a_1': a_1, 'a_2': a_2}

def power_regression_coefficients(x, y):
    try:
        N = len(x)
        y_log10s = [log10(y[i]) for i in range(N)]
        x_log10s = [log10(x[i]) for i in range(N)]
        linear_coefs = linear_regression_coefficients(x_log10s, y_log10s)    
        A_1, A_2 = linear_coefs['a_1'], linear_coefs['a_2']
        a_1 = 10 ** A_1 
        a_2 = A_2
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов степ регрессии: {e}")
        return {'a_1': 1, 'a_2': 1}
    return {'a_1': a_1, 'a_2': a_2}

def log_regression_coefficients(x, y):
    try:
        N = len(x)
        x_logs = [x[i] for i in range(N)]
        linear_coefs = linear_regression_coefficients(x_logs, y)    
        a_1, a_2 = linear_coefs['a_1'], linear_coefs['a_2']
    except Exception as e:
        print(f"Ошибка вычисления коэффициентов степ регрессии: {e}")
        return {'a_1': 1, 'a_2': 1}
    return {'a_1': a_1, 'a_2': a_2}


def main():
    parser = argparse.ArgumentParser(description="USD/JPY regression analysis")
    parser.add_argument("start_date", type=str, help="Начальная дата в формате YYYY-MM-DD")
    parser.add_argument("end_date", type=str, help="Конечная дата в формате YYYY-MM-DD")
    parser.add_argument("new_date", type=str, help="Новая дата в формате YYYY.MM.DD")

    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date
    new_date = args.new_date

    ticker = "JPY=X"
    yf_data = yf.download(ticker, start=start_date, end=end_date)

    if len(yf_data) < 2:
        print("Данные не загружены")
        sys.exit()
    print(yf_data)

    data = {
        'Index': [i for i in range(1, len(yf_data.index) + 1)],
        'Date': list(yf_data.index),
        'Close': list(yf_data['Close']['JPY=X'])
    }

    date_obj_2 = data['Date'][-1]
    date_obj_1 = datetime.strptime(new_date, '%Y-%m-%d')
    d_dates = date_obj_1 - date_obj_2

    data['Date new'] = [date_obj_2 + timedelta(days=d) for d in range(d_dates.days + 1) if (date_obj_2 + timedelta(days=d)).weekday() <= 4]
    data['Index new'] = [data['Index'][-1] + i for i in range(0, len(data['Date new']))]

    linear_coefs = linear_regression_coefficients(data['Index'], data['Close'])
    data['Linear'] = [linear_coefs['a_2'] * x + linear_coefs['a_1'] for x in data['Index']]
    data['Linear new'] = [linear_coefs['a_2'] * x + linear_coefs['a_1'] for x in data['Index new']]

    parabolic_coefs = parabolic_regression_coefficients(data['Index'], data['Close'])
    data['Parabolic'] = [parabolic_coefs['a_1'] + parabolic_coefs['a_2'] * x + parabolic_coefs['a_3'] * x ** 2 for x in data['Index']]
    data['Parabolic new'] = [parabolic_coefs['a_1'] + parabolic_coefs['a_2'] * x + parabolic_coefs['a_3'] * x ** 2 for x in data['Index new']]

    exponential_coefs = exponential_regression_coefficients(data['Index'], data['Close'])
    data['Exponential'] = [exponential_coefs['a_1'] * exp(exponential_coefs['a_2'] * x) for x in data['Index']]
    data['Exponential new'] = [exponential_coefs['a_1'] * exp(exponential_coefs['a_2'] * x) for x in data['Index new']]

    power_coefs = power_regression_coefficients(data['Index'], data['Close'])
    data['Power'] = [power_coefs['a_1'] * x ** power_coefs['a_2'] for x in data['Index']]
    data['Power new'] = [power_coefs['a_1'] * x ** power_coefs['a_2'] for x in data['Index new']]

    log_coefs = log_regression_coefficients(data['Index'], data['Close'])
    data['Log'] = [log_coefs['a_1'] + log_coefs['a_2'] * log(x) for x in data['Index']]
    data['Log new'] = [log_coefs['a_1'] + log_coefs['a_2'] * log(x) for x in data['Index new']]

    degree = 16
    polynomial_coefs = polynomial_regression_coefficients(data['Index'], data['Close'], degree)
    data['Polynomial'] =  [sum(polynomial_coefs[f'a_{i + 1}'] * x ** (i) for i in range(degree + 1)) for x in data['Index']]
    data['Polynomial new'] =  [sum(polynomial_coefs[f'a_{i + 1}'] * x ** (i) for i in range(degree + 1)) for x in data['Index new']]

    print("Формула линейной регрессии:")
    print(f"y = {linear_coefs['a_2']:.6f}*x + {linear_coefs['a_1']:.6f}\n")

    print("Формула параболической регрессии:")
    print(f"y = {parabolic_coefs['a_1']:.6f} + {parabolic_coefs['a_2']:.6f}*x + {parabolic_coefs['a_3']:.6f}*x^2\n")

    print("Формула экспоненциальной регрессии:")
    print(f"y = {exponential_coefs['a_1']:.6f} * e^({exponential_coefs['a_2']:.6f}*x)\n")

    print("Формула степенной регрессии:")
    print(f"y = {power_coefs['a_1']:.6f} * x^{power_coefs['a_2']:.6f}\n")

    print("Формула полиномиальной регрессии (степень {}):".format(degree))
    formula = "y = "
    for i in range(0, degree + 1):
        coef = polynomial_coefs[f'a_{i + 1}']
        if i == 0:
            formula += f"{coef:.6f}"
        else:
            sign = " + " if coef >= 0 else " - "
            formula += f"{sign}{abs(coef):.16f}*x"
            if i > 1:
                formula += f"^{i}"
    print(formula + "\n")
    print("Формула логарифмической регрессии:")
    print(f"y = {log_coefs['a_1']:.6f} + {log_coefs['a_2']:.6f}*ln(x)\n")

    fig, axs = plt.subplots(3, 2, layout="constrained")
    fig.suptitle(f"Курс USD/JPY {str(data['Date'][0])[: -9]} - {str(data['Date'][-1])[: -9]}", fontsize=8)
    axs[0, 0].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)
    axs[0, 1].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)
    axs[1, 0].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)
    axs[1, 1].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)
    axs[2, 0].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)
    axs[2, 1].plot(data['Date'], data["Close"], label="USD/JPY",  marker='o', linestyle='', ms = 1)

    label_text = (
        f"USD/JPY log\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Log'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Log'], data['Close']):.4f}"
    )
    axs[0, 0].plot(data['Date'], data["Log"], label=label_text, linestyle='-', color='red')
    axs[0, 0].plot(data['Date new'], data["Log new"], label=f'USD/JPY log new \nПредсказание на {new_date}: {data["Log new"][-1]:.4f}', linestyle='-', color='green')

    label_text = (
        f"USD/JPY linear\n"
        f"Коэф. коррел.: ρ = {correlation_coefficient(data['Index'], data['Close']):.4f}\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Linear'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Linear'], data['Close']):.4f}"
    )
    axs[0, 1].plot(data['Date'], data["Linear"], label=label_text, linestyle='-', color='red')
    axs[0, 1].plot(data['Date new'], data["Linear new"], label=f'USD/JPY linear new \nПредсказание на {new_date}: {data["Linear new"][-1]:.4f}', linestyle='-', color='green')

    label_text = (
        f"USD/JPY Parabolic\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Parabolic'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Parabolic'], data['Close']):.4f}"
    )
    axs[1, 0].plot(data['Date'], data["Parabolic"], label=label_text, linestyle='-', color='purple')
    axs[1, 0].plot(data['Date new'], data["Parabolic new"], label=f"USD/JPY Parabolic new \nПредсказание на {new_date}: {data["Parabolic new"][-1]:.4f}", linestyle='-', color='green')

    label_text = (
        f"USD/JPY Exponential\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Exponential'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Exponential'], data['Close']):.4f}"
    )
    axs[1, 1].plot(data['Date'], data["Exponential"], label=label_text, linestyle='-', color='yellow')
    axs[1, 1].plot(data['Date new'], data["Exponential new"], label=f"USD/JPY Exponential new\nПредсказание на {new_date}: {data["Exponential new"][-1]:.4f}", linestyle='-', color='green')

    label_text = (
        f"USD/JPY Power\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Power'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Power'], data['Close']):.4f}"
    )
    axs[2, 0].plot(data['Date'], data["Power"], label=label_text, linestyle='-', color='orange')
    axs[2, 0].plot(data['Date new'], data["Power new"], label=f"USD/JPY Power new\nПредсказание на {new_date}: {data["Power new"][-1]:.4f}", linestyle='-', color='green')

    label_text = (
        f"USD/JPY Polynomial ({degree})\n"
        f"Коэф. детер.: r² = {coefficient_of_determination(data['Polynomial'], data['Close']):.4f}\n"
        f"MSE: E = {MSE(data['Polynomial'], data['Close']):.4f}"
    )
    axs[2, 1].plot(data['Date'], data["Polynomial"], label=label_text, linestyle='-', color='black')
    axs[2, 1].plot(data['Date new'], data["Polynomial new"], label=f"USD/JPY Polynomial ({degree}) new\nПредсказание на {new_date}: {data["Polynomial new"][-1]:.4f}", linestyle='-', color='green')

    for row in axs:
        for ax in row:
            ax.tick_params(axis='x', rotation=90, labelsize=6)
            ax.tick_params(axis='y', labelsize=6)
            ax.set_xlabel("Дата", fontsize=8)
            ax.set_ylabel("Цена (JPY за 1 USD)", fontsize=8)
            ax.legend(fontsize=6)
            ax.grid(True)

    plt.show()

main()