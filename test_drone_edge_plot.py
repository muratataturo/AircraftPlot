import numpy as np
import matplotlib.pyplot as plt
from helper import bezier
from mpl_toolkits.mplot3d import Axes3D

# ToDo: arrange the arguments and split the module based on function
# cockpit
huc = 0.8
hlc = 0.1
wc = 1.0
# cabin(fuselage)
huf = 1.5
hlf = 0.2
wf = 1.2

# after cabin
hau = 1.5
wa = 0.5

upper_r = huf / wf
upper_l = hlf / wf

l1 = 2
l2 = 5
l3 = 6

l = l3

# cockpit part(bezier curve)
x = np.linspace(0, l1, 50)

lower_sign = -1

cockpit_arr = []

bezier_zu = []
bezier_zl = []


qzu = np.array([[0, 0], [0, huc], [l1, huf]])
qzl = np.array([[0, 0], [0, -hlc], [l1, -hlf]])

bezier_y = []

qy = np.array([[0, 0], [0, wc], [l1, wf]])

for t in np.linspace(0, 1, 50):
    bezier_zu.append(bezier(2, t, qzu)[1])
    bezier_zl.append(bezier(2, t, qzl)[1])
    bezier_y.append(bezier(2, t, qy)[1])

for xi, bzl, bzu, by in zip(x, bezier_zl, bezier_zu, bezier_y):

    y = np.linspace(-by, by, 30)

    for yi in y:
        zui = bzu * np.sqrt(1 - yi ** 2 / by ** 2)
        zli = bzl * np.sqrt(1 - yi ** 2/ by ** 2)

        cockpit_arr.append([xi, yi, zui])
        cockpit_arr.append([xi, yi, zli])


cockpit_arr = np.array(cockpit_arr)

"""
# cockpit part(parabola curve)
x = np.linspace(0, l1, 30)

cockpit_arr = []
zupper = []
zlower = []

lower_sign = -1

for xi in x:
    z_u = huf * np.sqrt(xi / l1)
    z_l = lower_sign * hlf * np.sqrt(xi / l1)

    b_u = z_u
    a_u = b_u / upper_r

    a_l = a_u
    b_l = z_l

    y = np.linspace(-a_u, a_u, 30)

    for yi in y:
        zui = b_u * np.sqrt(1.0 - (yi / a_u) ** 2)
        zli = b_l * np.sqrt(1.0 - (yi / a_l) ** 2)
        cockpit_arr.append([xi, yi, zui])
        cockpit_arr.append([xi, yi, zli])

cockpit_arr = np.array(cockpit_arr)
"""

# cabin part
cabin_arr = []
x = np.linspace(l1, l2, 30)

for xi in x:
    z_u = huf
    z_l = hlf

    b_u = z_u
    a_u = b_u / upper_r

    a_l = a_u
    b_l = z_l

    y = np.linspace(-a_u, a_u, 30)

    for yi in y:
        zui = b_u * np.sqrt(1.0 - (yi / a_u) ** 2)
        zli = b_l * np.sqrt(1.0 - (yi / a_l) ** 2)

        cabin_arr.append([xi, yi, zui])
        cabin_arr.append([xi, yi, -zli])

cabin_arr = np.array(cabin_arr)

# after cabin part(Bezier)
x = np.linspace(l2, l3, 50)
after_cabin_arr = []
bezier_zu = []
bezier_zl = []

qzu = np.array([[l2, huf], [l3, hau], [l3, hau]])
qzl = np.array([[l2, -hlf], [l3, -hlc], [l3, 0]])

bezier_y = []

qy = np.array([[l2, wf], [l3, wa], [l3, 0]])

for t in np.linspace(0, 1, 50):
    bezier_zu.append(bezier(2, t, qzu)[1])
    bezier_zl.append(bezier(2, t, qzl)[1])
    bezier_y.append(bezier(2, t, qy)[1])

for xi, bzl, bzu, by in zip(x, bezier_zl, bezier_zu, bezier_y):

    y = np.linspace(-by, by, 30)

    for yi in y:
        zui = bzu * np.sqrt(1 - yi ** 2 / by ** 2)
        zli = bzl * np.sqrt(1 - yi ** 2/ by ** 2)

        after_cabin_arr.append([xi, yi, zui])
        after_cabin_arr.append([xi, yi, zli])


after_cabin_arr = np.array(after_cabin_arr)

"""
# after cabin part(parabola curve)
after_cabin_arr = []
x = np.linspace(l2, l3, 30)

# upper coefficient
a1 = (huf - hau) / (np.sqrt(l2) - np.sqrt(l3))
b1 = huf - np.sqrt(l2) * a1

# lower coefficient
a2 = (hau + hlf) / (np.sqrt(l3) - np.sqrt(l2))
b2 = hau - a2 * np.sqrt(l3)

for xi in x:

    z_u = a1 * np.sqrt(xi) + b1
    z_l = a2 * np.sqrt(xi) + b2
    z_l = lower_sign * z_l

    b_u = z_u
    a_u = b_u / upper_r

    a_l = a_u
    b_l = z_l

    y = np.linspace(-a_u, a_u, 30)

    for yi in y:
        if a_u == 0:
            zui, zli = 0, 0
        else:
            zui = b_u * np.sqrt(1.0 - (yi / a_u) ** 2)
            zli = b_l * np.sqrt(1.0 - (yi / a_l) ** 2)

        if zui == 0 or zli == 0:
            continue

        after_cabin_arr.append([xi, yi, zui])
        after_cabin_arr.append([xi, yi, -zli])

after_cabin_arr = np.array(after_cabin_arr)
"""

# propeller(4)
def turnover_3d(theta, n):
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

# ToDo: I have to implement horizontal version for propeller
# propeller settings(vertical)
# txs = [0.3, 0.4, 0.6, 0.7]
# thetas = [40, 70, 110, 140]

txs = [0.2, 0.5, 0.8]
thetas = [30, 90, 150]

radius = 1.0  # radius of propeller curve(the collection of propellers)
pr = 0.5  # radius of each propeller
lp = 0.5  # length of arm
zdiffp = 0.4  # shift setting position ratio

k = 0.3

half_propeller_number = len(txs)

joint_points = []

for idx in range(half_propeller_number):
    point = [l * txs[idx], np.max(cabin_arr[:, 1]), idx * zdiffp]
    joint_points.append(point)


propeller_arr_l = []
propeller_arr_r = []

unit_vec = np.array([1, 0, 0])

for theta, joint_point in zip(thetas, joint_points):
    theta = 180 - theta
    center = np.array([joint_point[0] + (radius + pr) * np.cos(theta * np.pi / 180.0), joint_point[1] + (radius + pr) * np.sin(theta * np.pi / 180.0), joint_point[2]])

    z = np.linspace(-k * lp + joint_point[2], (1 - k) * lp + joint_point[2], 30)

    for zi in z:

        x = np.linspace(center[0] - pr, center[0] + pr, 30)

        for xi in x:
            target = np.sqrt(pr ** 2 - (xi - center[0]) ** 2)
            yui = center[1] + target
            yli = center[1] - target

            plu = [xi, yui, zi]
            pll = [xi, yli, zi]
            propeller_arr_l.append(plu)
            propeller_arr_l.append(pll)

            pru = [xi, -yui, zi]
            prl = [xi, -yli, zi]
            propeller_arr_r.append(pru)
            propeller_arr_r.append(prl)


propeller_arr_l = np.array(propeller_arr_l)
propeller_arr_r = np.array(propeller_arr_r)

# z axis 3d turnover
propeller_arr = np.concatenate([propeller_arr_l, propeller_arr_r], axis=0)

# pole
poll_r = 0.1  # arm radius

poll_arr = []

# right part
x = np.linspace(0, radius + pr, 30)
for xi in x:
    y = np.linspace(-poll_r, poll_r, 30)

    for yi in y:
        target = np.sqrt(poll_r ** 2 - yi ** 2)
        zui = target
        zli = - target

        pu = [xi, yi, zui]
        pl = [xi, yi, zli]

        for idx in range(half_propeller_number):
            rep_j = joint_points[idx]

            theta = thetas[idx]

            theta_u = -1 * (180 - theta) * np.pi / 180.0

            t_arr_u = turnover_3d(theta_u, np.array([0, 0, 1]))

            theta_l = 180 * np.pi / 180.0

            t_arr_l = turnover_3d(theta_l, np.array([0, 0, 1]))

            puu = np.dot(t_arr_u.T, np.array(pu)) + np.array([rep_j[0], rep_j[1], rep_j[2]])
            pll = np.dot(t_arr_l.T, puu) + np.array([l, 0, -2 * zdiffp * idx + (half_propeller_number - 1) * zdiffp])
            poll_arr.append(puu.tolist())
            poll_arr.append(pll.tolist())


"""
theta_l = 180 * np.pi / 180.0
t_arr_l = turnover_3d(theta_l, np.array([1, 0, 0]))

poll_arr_l = []
for idx, p in enumerate(poll_arr):
    pl = np.dot(t_arr_l.T, np.array(p)) + np.array([0, 0, 0])
    poll_arr_l.append(pl.tolist())


poll_arr.extend(poll_arr_l)
"""




poll_arr = np.array(poll_arr)

# 3D plot
fig = plt.figure()

ax = Axes3D(fig)

ax.scatter(cockpit_arr[:, 0], cockpit_arr[:, 1], cockpit_arr[:, 2])
ax.scatter(cabin_arr[:, 0], cabin_arr[:, 1], cabin_arr[:, 2])
ax.scatter(after_cabin_arr[:, 0], after_cabin_arr[:, 1], after_cabin_arr[:, 2])
ax.scatter(propeller_arr[:, 0], propeller_arr[:, 1], propeller_arr[:, 2])
ax.scatter(poll_arr[:, 0], poll_arr[:, 1], poll_arr[:, 2])

ax.set_xlim([-2, 8])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])

# plt.savefig('./Pictures/drone_edge.png')

plt.show()




