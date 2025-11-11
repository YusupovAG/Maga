from matplotlib.pyplot import subplots, show

def getData():
    return {
    "coords": [
            [0.932429389, 0.936934096, 0.945943511, 0.968467048, 0.972971755, 0.986485878, 1],
            [0.647058824, 0.588235294, 0.852941176, 0.647058824, 0.588235294, 1, 0.647058824]
        ],
    "max": [False, True]
}

def show_pareto_cone_plot(points, maximization):
    fig, ax = subplots(1, 2)
    for i, point in enumerate(points):
        brd = dict(linewidth=1, facecolor="white", edgecolor="white")
        ax[0].text(point[0] + 0.002, point[1], str(i + 1), bbox=brd)
        ax[0].scatter(point[0], point[1], color='black')
    ax[0].set_xlabel("f_1")
    ax[0].set_ylabel("f_2")

    for i, point in enumerate(points):
        if point[2]:
            brd = dict(linewidth=1, facecolor="white", edgecolor="red")
        else:
            brd = dict(linewidth=1, facecolor="white", edgecolor="white")
        ax[1].text(point[0] + 0.002, point[1], str(i + 1), bbox=brd)
        ax[1].quiver(point[0], point[1], (1 if maximization[0] else -1), 0, color='blue')
        ax[1].quiver(point[0], point[1], 0, (1 if maximization[1] else -1), color='red')
        ax[1].scatter(point[0], point[1], color='black')
    ax[1].set_xlabel("f_1")
    ax[1].set_ylabel("f_2")
    show()

def find_optimal_points(points, maximization):
    dimensions_count = len(points[0])
    for i, point in enumerate(points):
        optimal = True
        for j, other_point in enumerate(points):
            if i == j:
                continue
            
            k = [1 if maximization[d] else -1 for d in range(dimensions_count)]
            if all(point[d] * k[d] <= other_point[d] * k[d] for d in range(dimensions_count)):
                optimal = False
                break
       
        points[i].append(optimal)
    return points

def to_points(coords):
    n, m = len(coords), len(coords[0])
    return [[coords[j][i] for j in range(n)] for i in range(m)]

def find_pareto_cone_optimal(coords, maximization):
    points = to_points(coords)
    points = find_optimal_points(points, maximization)
    for point in points:
        print(point)
    if len(coords) == 2:
        show_pareto_cone_plot(points, maximization)
         
def main():
    data = getData()
    find_pareto_cone_optimal(data['coords'], data['max'])
    
main()