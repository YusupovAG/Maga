import matplotlib.pyplot as plt
import numpy as np  # <-- добавили numpy

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
h, w, l = 4, 5, 2

voxels = np.array([[[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]]], dtype=np.int8)



ax.voxels(voxels, edgecolor='black', facecolors='red')
ax.set(xlabel='Z', ylabel='Y', zlabel='X')
plt.show()