from random import uniform, seed
from pandas import read_excel
from math import exp

class data_manager():
    def __init__(self, file_name):
        self.renormalized_X = list()
        self.renormalized_Y = list()
        self.normalized_X = list()
        self.normalized_Y = list()

        self.read_file(file_name)
        
    def read_file(self, file_name):
        self.renormalized_X = [list(line[2 : -1]) for line in read_excel('file.xls').values]
        self.renormalized_Y = [[line[-1]] for line in read_excel('file.xls').values]
 
        self.normalized_X = self.normalize_table(self.renormalized_X)
        self.normalized_Y = self.normalize_table(self.renormalized_Y)

    def get_renormalized_X(self):
        return self.renormalized_X

    def get_renormalized_Y(self):
        return self.renormalized_Y
    
    def get_normalized_X(self):
        return self.normalized_X
    
    def get_normalized_Y(self):
        return self.normalized_Y
    
    def transpare(self, x):
        t_x = list()
        for i in range(len(x[0])):
            t_x.append(list())
            for j in range(len(x)):
                t_x[i].append(x[j][i])
        return t_x

    def normalize(self, v):
        return [n / max(v) for n in v]

    def normalize_table(self, t):
        t_table = self.transpare(t)
        for i in range(len(t_table)):
            t_table[i] = self.normalize(t_table[i])
        return self.transpare(t_table)

class NN():
    def __init__(self, dm):
        self.data = dm
        self.w = list()
        self.b = list()

    def f(self, x):
        return 1 / (1 + exp(-x)) 

    def deriv_f(self, x):
        return self.f(x) * (1 - self.f(x))

    def init_W(self, n, m):
        seed(1)
        return [[uniform(0, 1) for _ in range(m)] for _ in range(n)]

    def layers_sizes(self, X):
        count_of_input = len(X[0])
        count_of_hidden = 2 * count_of_input + 1
        count_of_output = 1
        return [count_of_input, count_of_hidden, count_of_output]

    def learn(self):
        X = self.data.get_normalized_X()
        d = self.data.get_normalized_Y()

        l_sizes = self.layers_sizes(X)
        l_count = len(l_sizes)

        W = list()
        for i in range(1, l_count):
            W.append(self.init_W(l_sizes[i - 1], l_sizes[i]))

        B = []
        for i in range(1, l_count):
            B.append([uniform(0, 1) for _ in range(l_sizes[i])])

        for epoch in range(1000):
            total_error = 0
            for t in range(len(X)):
                y = [X[t]]
                for layer in range(1, l_count):
                    input_layer = y[-1]
                    y.append([self.f(sum([W[layer - 1][i][j] * input_layer[i] for i in range(l_sizes[layer - 1])]) + B[layer - 1][j])  for j in range(l_sizes[layer])])
                
                delta = [None] * l_count
                delta[-1] = [None] * l_sizes[-1]
                for j in range(l_sizes[-1]):
                    delta[-1][j] = y[-1][j] * (1 - y[-1][j]) * (d[t][j] - y[-1][j])

                for n in range(l_count - 2, -1, -1):
                    delta[n] = [None] * l_sizes[n]
                    for j in range(l_sizes[n]):
                        delta[n][j] = y[n][j] * (1 - y[n][j]) * sum([W[n][j][k] * delta[n + 1][k] for k in range(l_sizes[n + 1])])

                eta = 0.1
                for n in range(len(W)):
                    for i in range(l_sizes[n]):
                        for j in range(l_sizes[n + 1]):
                            W[n][i][j] += eta * delta[n + 1][j] * y[n][i]
                    for j in range(l_sizes[n + 1]):
                        B[n][j] += eta * delta[n + 1][j]
                
                total_error += sum((d[t][j] - y[-1][j]) ** 2 for j in range(l_sizes[-1]))

            if epoch % 100 == 0:
                print(f"Эпоха {epoch}, ошибка = {total_error:.6f}")

        self.w = W
        self.b = B

    def test(self, n_samples=5):
        X = self.data.get_normalized_X()
        Y = self.data.get_normalized_Y()
        renorm_Y = self.data.get_renormalized_Y()
        W = self.w
        B = self.b
        print("\nТестирование сети")
        for t in range(min(n_samples, len(X))):
            y = X[t]
            for n in range(len(W)):
                y = [self.f(sum(W[n][i][j] * y[i] for i in range(len(W[n]))) + B[n][j])
                     for j in range(len(W[n][0]))]
            
            y_norm = y[0]
            y_pred = y_norm * max([yy[0] for yy in renorm_Y])
            y_true = renorm_Y[t][0]

            print(f"\nОбразец {t+1}:")
            print(f"  Вход (X): {self.data.get_renormalized_X()[t]}")
            print(f"  Истинное значение (Y): {y_true:.4f}")
            print(f"  Предсказанное (Y_pred): {y_pred:.4f}")
            print(f"  Ошибка: {abs(y_true - y_pred):.4f}")

def main():
    dm = data_manager('file.xls')
    nn = NN(dm)
    nn.learn()
    nn.test()

main()