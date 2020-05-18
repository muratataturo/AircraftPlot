import numpy as np
import matplotlib.pyplot as plt
from helper import bezier
from mpl_toolkits.mplot3d import Axes3D

# Blended Wing Body has two scenarios about construction
# 1. establishment based on existing normal shape aircraft
# 2. new establishment

# 1 is necessary for completing the value of bottom area

# baseline normal
huc = 1.8  # upper cockpit height
hlc = 1.8  # lower cockpit height
wc = 1.2  # cockpit width

huf = 2.0  # upper fuselage height (radius)
wf = 2.0  # fuselage width (radius)
hlf = 2.1  # lower fuselage height(fuselage), optimize it from cargo volume
upper_r = huf / wf  # the ratio of height and width at upper part
lower_r = hlf / wf  # the ratio of height and width at lower part

hau = 1.5  # height of after cabin upper
wa = 0.3  # after cabin width

l1 = 7  # up to section 1 length
l2 = 25  # up to section 2 length
l3 = 4  # up to section 3 length
l = l1 + l2 + l3  # total fuselage length

# Bottom area
BSn = (wc + wf) * l1 + 2 * wf * l2 + (wa + wf) * l3

# parameters u => width, v = length
u1 = 0.1
v1 = 0.3
u2 = 0.3
v2 = 0.5
u3 = 0.1
v3 = 1.0 - v1 - v2

# Tuning length(if you use 2 case, you skip this process)
lb = l
lb_step = 1.0
diff_s = 0.0
diff_s_old = 0.0
count = 0
while True:
    if count == 100:
        break
    BSb = (u1 * v1 + u2 * v1 + 2 * u2 * v2 + u3 * v3 + u2 * v3) * lb ** 2

    diff_s = (BSb - BSn) / BSn

    # print('residual:', diff_s, 'length bwb:', lb)

    if abs(diff_s) < 1.0e-5:
        # print('ok')
        break

    if diff_s * diff_s_old < 0.0:
        lb_step *= 0.5

    lb += -np.sign(diff_s) * lb_step

    diff_s_old = diff_s
    count += 1

print(lb)
# determine p, m
def rho(p, k2):
    return p ** 2 * ((1 - 2 * p) + 2 * p * k2 - k2 ** 2)

def lho(p, k1):

    return (1 - p) ** 2 * (2 * p * k1 - k1 ** 2)

l1 = v1 * lb
l2 = v2 * lb
k1 = l1 / lb
k2 = (l1 + l2) / lb

# airfoil parameters
pb = v1 / v2
mb = pb ** 2 * huf / (2 * pb * k1 - k1 ** 2)

xk = np.linspace(0, 1, 30)

x = []
z = []

for xi in xk:
    if xi < pb:
        zi = mb * (2 * pb * xi - xi ** 2) / pb ** 2
        xi *= lb

    else:
        zi = mb * ((1 - 2 * pb) + 2 * pb * xi - xi ** 2) / (1 - pb) ** 2
        xi *= lb

    z.append(zi)
    x.append(xi)

# main wing shape
ctip = 1
croot = 3
b = 40
theta = 20  # retreat angle

p = pb
tc = 0.1

jmx = 0.5  # main wing joint poiny

st = [v1 * lb, u2 * lb]

BX = croot * (b / 2 - st[1]) / (croot - ctip)

main_wing_arr = []

y = np.linspace(st[1], b * 0.5, 30)

for yi in y:
    xu = st[0] + (yi - st[1]) * np.tan(theta * np.pi / 180.0)
    cx = croot * (BX + st[1] - yi) / BX
    xl = xu + cx

    x = np.linspace(xu, xl, 30)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl)
        zli = -1 * zui

        main_wing_arr.append([xi, yi, zui])
        main_wing_arr.append([xi, yi, zli])
        main_wing_arr.append([xi, -yi, zui])
        main_wing_arr.append([xi, -yi, zli])

main_wing_arr = np.array(main_wing_arr)

# horizontal face

bezier_y1 = []
qy1 = np.array([[0, 0], [0, u1 * lb], [v1 * lb, u2 * lb],
                [(b * 0.5 - st[1]) * np.tan(theta * np.pi / 180.0) + st[0], b * 0.5]])

bezier_y2 = []
qy2 = np.array([[(b * 0.5 - st[1]) * np.tan(theta * np.pi / 180.0) + st[0] + ctip, b * 0.5],
                [croot + st[0], st[1]], [lb, u3 * lb], [lb, 0]])

for t in np.linspace(0, 1, 50):
    bezier_y1.append(bezier(qy1.shape[0] - 1, t, qy1))
    bezier_y2.append(bezier(qy2.shape[0] - 1, t, qy2))

xs = (b * 0.5 - st[1]) * np.tan(theta * np.pi / 180.0) + st[0]
xf = xs + ctip
interpolates = [np.array([xi, b * 0.5]) for xi in np.linspace(xs, xf, 5)]

# y coordinates
bezier_y = bezier_y1 + interpolates + bezier_y2

fuselage_arr = []
# xz plane
fuselage_line = []

for xi, yu in bezier_y:
    xi /= lb
    if xi < pb:
        zu = mb * (2 * pb * xi - xi ** 2) / pb ** 2

    else:
        zu = mb * ((1 - 2 * pb) + 2 * pb * xi - xi ** 2) / (1 - pb) ** 2

    xi *= lb

    fuselage_line.append([xi, zu])

    y = np.linspace(-yu, yu, 50)
    for yi in y:
        zui = zu * np.sqrt(1.0 - yi ** 2 / yu ** 2)
        zli = -1 * zui

        fuselage_arr.append([xi, yi, zui])
        fuselage_arr.append([xi, yi, zli])


fuselage_arr = np.array(fuselage_arr)
fuselage_line = np.array(fuselage_line)

# engine(core)(main wing down)
lower = -1
rin = 0.8
rout = 0.4
tin = 0.1

len = 4.0

tx = 0.4
ty = 0.4

k = 0.4

# joint point of main wing lower
joint_point_ml = [st[0] + croot * tx, st[1] + (b / 2 - st[1]) * ty, lower * np.max(main_wing_arr[:, 2])]

zcen = joint_point_ml[2] - tin - rin

# engine curve -> z = ax ** 2 + b * x + c
x = np.linspace(joint_point_ml[0] - k * len, joint_point_ml[0] + (1 - k) * len, 30)

az = lower * (rin - rout) / (1 - 2 * k) / len ** 2
bz = -2 * joint_point_ml[0] * az
cz = joint_point_ml[2] + bz ** 2 / (4 * az)

engine_arr_low = []

for xi in x:

    zu = az * xi ** 2 + bz * xi + cz

    zl = 2 * zcen - zu

    z = np.linspace(zl, zu, 30)

    for zi in z:
        target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
        yui = joint_point_ml[1] + target
        yli = joint_point_ml[1] - target

        engine_arr_low.append([xi, yui, zi])
        engine_arr_low.append([xi, yli, zi])
        engine_arr_low.append([xi, -yui, zi])
        engine_arr_low.append([xi, -yli, zi])


engine_arr_low = np.array(engine_arr_low)

# engine(distributed fan)(upper)
nfan = 4
rfin = 0.6
rfout = 0.4
lower = -1

r_afford = 0.1

theta = theta  # retreat angle

tin = 0.1

lfan = 2.0

k = 0.1

joint_point_init = joint_point_ml

engine_arr_dist_up = []

for n in range(nfan):

    diff_r = (1.0 + r_afford) * 2 * (n + 1)
    joint_point = [joint_point_init[0] + diff_r * np.sin(theta * np.pi / 180.0), joint_point_init[1] + diff_r * np.cos(theta * np.pi / 180.0), joint_point_init[2]]
    zcen = joint_point[2] + tin + rin

    # engine curve -> z = ax ** 2 + b * x + c
    x = np.linspace(joint_point[0] - k * lfan, joint_point[0] + (1 - k) * lfan, 30)

    az = (rfin - rfout) / (1 - 2 * k) / lfan ** 2
    bz = -2 * joint_point[0] * az
    cz = joint_point[2] + bz ** 2 / (4 * az)

    for xi in x:

        zu = az * xi ** 2 + bz * xi + cz

        zl = 2 * zcen - zu

        z = np.linspace(zl, zu, 30)

        for zi in z:
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            yui = joint_point[1] + target
            yli = joint_point[1] - target

            engine_arr_dist_up.append([xi, yui, zi])
            engine_arr_dist_up.append([xi, yli, zi])
            engine_arr_dist_up.append([xi, -yui, zi])
            engine_arr_dist_up.append([xi, -yli, zi])

engine_arr_dist_up = np.array(engine_arr_dist_up)

# engine(distributed fan)(fuselage upper)
nfan = 7
rfin = 0.5
rfout = 0.3

lfan = 1.0

r_afford = 0.1

# mounting position coefficient
tx = 0.7
ty = 0.05

# setting angle
set_angle = -10

# fuselage line fitting
res = np.polyfit(fuselage_line[:, 0], fuselage_line[:, 1], 2)

joint_point_init = [tx * lb, ty * lb, np.poly1d(res)(tx * lb)]

engine_arr_dist_fus = []

for n in range(nfan):

    diff_r = (1.0 + r_afford) * 2 * (n + 1)
    joint_point = [joint_point_init[0] + diff_r * np.sin(set_angle * np.pi / 180.0), joint_point_init[1] + diff_r * np.cos(set_angle * np.pi / 180.0), joint_point_init[2]]
    zcen = joint_point[2] + tin + rin

    # engine curve -> z = ax ** 2 + b * x + c
    x = np.linspace(joint_point[0] - k * lfan, joint_point[0] + (1 - k) * lfan, 30)

    az = (rfin - rfout) / (1 - 2 * k) / lfan ** 2
    bz = -2 * joint_point[0] * az
    cz = joint_point[2] + bz ** 2 / (4 * az)

    for xi in x:

        zu = az * xi ** 2 + bz * xi + cz

        zl = 2 * zcen - zu

        z = np.linspace(zl, zu, 30)

        for zi in z:
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            yui = joint_point[1] + target
            yli = joint_point[1] - target

            engine_arr_dist_fus.append([xi, yui, zi])
            engine_arr_dist_fus.append([xi, yli, zi])
            engine_arr_dist_fus.append([xi, -yui, zi])
            engine_arr_dist_fus.append([xi, -yli, zi])

engine_arr_dist_fus = np.array(engine_arr_dist_fus)

# judge feasibility(?)


fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(fuselage_arr[:, 0], fuselage_arr[:, 1], fuselage_arr[:, 2])
ax.scatter(main_wing_arr[:, 0], main_wing_arr[:, 1], main_wing_arr[:, 2])
ax.scatter(engine_arr_low[:, 0], engine_arr_low[:, 1], engine_arr_low[:, 2])
ax.scatter(engine_arr_dist_up[:, 0], engine_arr_dist_up[:, 1], engine_arr_dist_up[:, 2])
# ax.scatter(engine_arr_dist_fus[:, 0], engine_arr_dist_fus[:, 1], engine_arr_dist_fus[:, 2])

ax.set_xlim([-10, 20])
ax.set_ylim([-20, 20])
ax.set_zlim([-15, 15])

plt.show()

