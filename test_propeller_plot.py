import numpy as np
import matplotlib.pyplot as plt
from helper import bezier
from mpl_toolkits.mplot3d import Axes3D
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
l2 = 6
l3 = 7

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
qzl = np.array([[l2, -hlf], [l3, -hlc], [l3, hau]])

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
        zli = bzl * np.sqrt(1 - yi ** 2 / by ** 2)

        after_cabin_arr.append([xi, yi, zui])
        after_cabin_arr.append([xi, yi, zli])


after_cabin_arr = np.array(after_cabin_arr)

# main wing
ctip = 0.3
croot = 1
b = 10
theta = 25

BX = croot * (b / 2 - wf) / (croot - ctip)

jmx = 0.4
jmy = 0.0
jmz = 0.8

st = [l * jmx, wf, huf * jmz]

y = np.linspace(wf, b / 2, 30)

# airfoil
p = 0.4
tc = 0.11

main_wing_arr = []

for yi in y:
    xu = np.tan(theta * np.pi / 180) * (yi - wf) + st[0]
    cx = (1.0 - (yi - wf) / BX) * croot
    xl = xu + cx

    x = np.linspace(xu, xl, 30)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl) + st[2]
        zli = -1 * zui + 2 * st[2]

        main_wing_arr.append([xi, yi, zui])
        main_wing_arr.append([xi, yi, zli])
        main_wing_arr.append([xi, -yi, zui])
        main_wing_arr.append([xi, -yi, zli])


main_wing_arr = np.array(main_wing_arr)

# 3d turnover function
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

# propeller(upper)
lower_sign = -1
nprop = 2
rp = 1.0
cproot = 0.3
cptip = 0.2

pp = 0.4
tcp = 0.1

BPX = cproot * rp / (cproot - cptip)

tx = 0.6
ty = 0.1

# joint pole geometry
rj = 0.1
lj = 0.2

joint_point_propeller_init = [st[0] + croot * tx, st[1] + (0.5 * b - st[2]) * ty + st[2], np.max(main_wing_arr[:, 2])]

propeller_center_init = [joint_point_propeller_init[0] - lj, joint_point_propeller_init[1], joint_point_propeller_init[2]]

z = np.linspace(propeller_center_init[2], propeller_center_init[2] + rp, 30)

propeller_arr = []

for zi in z:
    cx = (1.0 - (zi - propeller_center_init[2]) / BPX) * cproot
    xu = propeller_center_init[0] - 0.5 * cx
    xl = propeller_center_init[0] + 0.5 * cx

    x = np.linspace(xu, xl, 30)

    for xi in x:
        yui = -tcp / (pp * (1 - pp) * cx) * (xi - xu) * (xi - xl) + propeller_center_init[1]
        yli = -1 * yui + 2 * propeller_center_init[1]

        propeller_arr.append([xi, yui, zi])
        propeller_arr.append([xi, yli, zi])


propeller_arr = np.array(propeller_arr)

# multi propeller
turn_angles = [60, 120, 180, 240, 300]

propeller_total_arr = []

for turn_angle in turn_angles:

    # 3d turnover 60
    turn_angle = turn_angle * np.pi / 180.0

    # go to (0, 0, 0)
    propeller_arr_base = propeller_arr - np.array(propeller_center_init)

    t_arr = turnover_3d(turn_angle, np.array([1, 0, 0]))

    propeller_arr_turn = []

    for pab in propeller_arr_base:
        target = np.dot(t_arr.T, pab)
        propeller_arr_turn.append(target.tolist())

    propeller_arr_turn = np.array(propeller_arr_turn)

    propeller_arr_turn += np.array(propeller_center_init)

    propeller_total_arr.extend(propeller_arr_turn.tolist())

propeller_total_arr = np.array(propeller_total_arr)


fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(cockpit_arr[:, 0], cockpit_arr[:, 1], cockpit_arr[:, 2])
ax.scatter(cabin_arr[:, 0], cabin_arr[:, 1], cabin_arr[:, 2])
ax.scatter(after_cabin_arr[:, 0], after_cabin_arr[:, 1], after_cabin_arr[:, 2])
ax.scatter(main_wing_arr[:, 0], main_wing_arr[:, 1], main_wing_arr[:, 2])
ax.scatter(propeller_arr[:, 0], propeller_arr[:, 1], propeller_arr[:, 2])
# ax.scatter(propeller_arr_turn[:, 0], propeller_arr_turn[:, 1], propeller_arr_turn[:, 2])
ax.scatter(propeller_total_arr[:, 0], propeller_total_arr[:, 1], propeller_total_arr[:, 2])

ax.set_xlim([-2, 8])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])

plt.show()
