import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# create bezier curve for outer line of aircraft
def bernstein(n, i, t):
    ncr = math.factorial(n) / (math.factorial(i) * math.factorial((n - i)))
    return ncr * t**i * (1 - t)**(n-i)


def bezier(n, t, q):
    p = np.zeros(2)
    for i in range(n + 1):
        p += bernstein(n, i, t) * q[i]
    return p


# 3d turnover operation
def turnover_3d(theta, n):

    # theta has already finished converting radians
    t_arr = np.array([[np.cos(theta) + n[0] ** 2 * (1 - np.cos(theta)),
                       n[0] * n[1] * (1 - np.cos(theta)) - n[2] * np.sin(theta),
                       n[2] * n[1] * (1 - np.cos(theta)) + n[1] * np.sin(theta)],
                      [n[0] * n[1] * (1 - np.cos(theta)) + n[2] * np.sin(theta),
                       np.cos(theta) + n[1] ** 2 * (1 - np.cos(theta)),
                       n[1] * n[2] * (1 - np.cos(theta)) - n[0] * np.sin(theta)],
                      [n[2] * n[0] * (1 - np.cos(theta)) - n[1] * np.sin(theta),
                       n[1] * n[2] * (1 - np.cos(theta)) + n[0] * np.sin(theta),
                       np.cos(theta) + n[2] ** 2 * (1 - np.cos(theta))]])

    return t_arr


# draw function
def draw_aircraft(component_dict, axis_bounds):

    fig = plt.figure()
    ax = Axes3D(fig)

    for name, arr in component_dict.items():

        ax.scatter(arr[:, 0], arr[:, 1], arr[:, 2])

    ax.set_xlim(axis_bounds[0])
    ax.set_ylim(axis_bounds[1])
    ax.set_zlim(axis_bounds[2])

    plt.show()
