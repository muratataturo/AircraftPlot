import numpy as np
import matplotlib.pyplot as plt
from helper import bezier
from mpl_toolkits.mplot3d import Axes3D

# arguments
huc = 0.4  # upper cockpit height
hlc = 0.4  # lower cockpit height
wc = 1.0  # cockpit width

huf = 2.0  # upper fuselage height (radius)
wf = 2.0  # fuselage width (radius)
hlf = 0.8  # lower fuselage height(fuselage), optimize it from cargo volume
upper_r = huf / wf  # the ratio of height and width at upper part
lower_r = hlf / wf  # the ratio of height and width at lower part

hau = 2.2  # height of after cabin upper
wa = 0.3  # after cabin width

l1 = 7  # up to section 1 length
l2 = 40  # up to section 2 length
l3 = 45  # up to section 3 length
l = l3  # total fuselage length

# cockpit
x = np.linspace(0.0, l1, 50)

lower_sign = -1

cockpit_arr = []

bezier_zu = []
bezier_zl = []

uk = 0.5

qzu = np.array([[0, 0], [l1 * uk, huc], [l1, huf]])
qzl = np.array([[0, 0], [l1 * uk, -hlc], [l1, -hlf]])

bezier_y = []

qy = np.array([[0, 0], [l1 * uk, wc], [l1, wf]])

for t in np.linspace(0, 1, 50):
    bezier_zu.append(bezier(2, t, qzu)[1])
    bezier_zl.append(bezier(2, t, qzl)[1])
    bezier_y.append(bezier(2, t, qy)[1])

for xi, bzl, bzu, by in zip(x, bezier_zl, bezier_zu, bezier_y):

    y = np.linspace(-by, by, 30)

    for yi in y:
        zui = bzu * np.sqrt(1 - yi ** 2 / by ** 2)
        zli = bzl * np.sqrt(1 - yi ** 2 / by ** 2)

        cockpit_arr.append([xi, yi, zui])
        cockpit_arr.append([xi, yi, zli])


cockpit_arr = np.array(cockpit_arr)

# cabin
cabin_arr = []
x = np.linspace(l1, l2, 30)

for xi in x:
    z_u = huf
    z_l = hlf

    b_u = z_u
    a_u = wf

    a_l = a_u
    b_l = z_l

    y = np.linspace(-a_u, a_u, 30)

    for yi in y:
        zui = b_u * np.sqrt(1.0 - (yi / a_u) ** 2)
        zli = b_l * np.sqrt(1.0 - (yi / a_l) ** 2)

        cabin_arr.append([xi, yi, zui])
        cabin_arr.append([xi, yi, -zli])

cabin_arr = np.array(cabin_arr)

# after cabin
after_cabin_arr = []
x = np.linspace(l2, l3, 50)
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
        zli = bzl * np.sqrt(1 - yi ** 2 / by ** 2)

        after_cabin_arr.append([xi, yi, zui])
        after_cabin_arr.append([xi, yi, zli])


after_cabin_arr = np.array(after_cabin_arr)


# main wing(delta wing)
croot = 14
b = 30
retreat_angle = 40
ctip = croot - b / 2 * np.tan(retreat_angle * np.pi / 180.0)
# feasibility check(?) => ctip < 0 false

st = [l * 0.5, 0]

y = np.linspace(wf, b / 2, 30)

# airfoil
p = 0.5
tc = 0.08

bezier_yu = []
bezier_yl = []

theta = retreat_angle * np.pi / 180.0

qyu = np.array([[(l1 + st[0]) * 0.5, wf],
                [st[0] + wf * np.tan(theta), wf],
                [0.5 * b * np.tan(theta) + st[0], 0.5 * b]])
qyl = np.array([[0.5 * b * np.tan(theta) + st[0] + ctip, 0.5 * b],
                [st[0] + croot, wf], [l2, wf]])

for t in np.linspace(0, 1, 50):
    bezier_yu.append(bezier(2, t, qyu))
    bezier_yl.append(bezier(2, t, qyl))


bezier_yl = bezier_yl[::-1]
main_wing_arr = []

for setu, setl in zip(bezier_yu, bezier_yl):
    xu, yu = setu
    xl, yl = setl
    cx = xl - xu

    x = np.linspace(xu, xl, 50)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl)
        zli = -1 * zui

        main_wing_arr.append([xi, yu, zui])
        main_wing_arr.append([xi, yu, zli])

        main_wing_arr.append([xi, -yu, zui])
        main_wing_arr.append([xi, -yu, zli])

"""
for yi in y:
    xu = np.tan(retreat_angle * np.pi / 180) * (yi - wf) + st[0]
    cx = croot - (yi - wf)
    xl = xu + cx

    x = np.linspace(xu, xl, 30)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl)
        zli = -1 * zui

        main_wing_arr.append([xi, yi, zui])
        main_wing_arr.append([xi, yi, zli])
        main_wing_arr.append([xi, -yi, zui])
        main_wing_arr.append([xi, -yi, zli])
        
"""

main_wing_arr = np.array(main_wing_arr)


"""
# main wing (normal)
croot = 10
b = 40
retreat_angle = 30
ctip = 1

BX = croot * (b / 2 - wf) / (croot - ctip)

st = [l * 0.4, wf]

# airfoil
p = 0.4
tc = 0.08

main_wing_arr = []

# bezier curve
bezier_yu = []
bezier_yl = []

theta = retreat_angle * np.pi / 180.0

qyu = np.array([[0.5 * (l1 + st[0]), wf], [st[0] + wf * np.tan(retreat_angle * np.pi / 180.0), wf], [st[0] + b * 0.5 * np.tan(retreat_angle * np.pi / 180.0), b * 0.5]])
qyl = np.array([[0.5 * b * np.tan(retreat_angle * np.pi / 180.0) + st[0] + ctip, 0.5 * b],
                [st[0] + wf * np.tan(retreat_angle * np.pi / 180.0) + (1.0 - wf / BX) * croot, wf],
                [l2, wf]])

for t in np.linspace(0, 1, 50):
    bezier_yu.append(bezier(2, t, qyu))
    bezier_yl.append(bezier(2, t, qyl))

# match y coordinates
bezier_yl = bezier_yl[::-1]

for setu, setl in zip(bezier_yu, bezier_yl[::-1]):
    xu, yu = setu
    xl, yl = setl
    cx = xl - xu

    x = np.linspace(xu, xl, 50)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl)
        zli = -1 * zui

        main_wing_arr.append([xi, yu, zui])
        main_wing_arr.append([xi, yu, zli])

        main_wing_arr.append([xi, -yu, zui])
        main_wing_arr.append([xi, -yu, zli])

main_wing_arr = np.array(main_wing_arr)
"""

# engine(upper fuselage)
rin = 1.2
rout = 0.8
tin = 0.1

k = 0.4
len = 5.0

theta = 45
tx = 0.7

eca = np.max(cabin_arr[:, 1])
ecb = np.max(cabin_arr[:, 2])

r = np.sqrt((eca * np.cos(theta * np.pi / 180.0)) ** 2 + (ecb * np.cos(theta * np.pi / 180.0) ** 2))

joint_point = [l * tx, r * np.cos(theta * np.pi / 180.0), r * np.sin(theta * np.pi / 180.0)]

zcen = (r + rin + tin) * np.sin(theta * np.pi / 180.0)

az = (rin - rout) * np.cos(theta * np.pi / 180.0) / (1 - 2 * k) / len ** 2
bz = (k * len - 2 * joint_point[0]) * az - tin * np.cos(theta * np.pi / 180.0) / (k * len)
cz = joint_point[2] - (rin + tin) * np.cos(theta * np.pi / 180.0) - az * joint_point[0] ** 2 - bz * joint_point[0]

x = np.linspace(joint_point[0] - k * len, joint_point[0] + (1 - k) * len, 30)

engine_fus_arr_up = []

for xi in x:
    zl = az * xi ** 2 + bz * xi + cz
    zu = zl + (zcen - zl) * 2

    z = np.linspace(zl, zu, 30)

    for zi in z:
        target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
        yui = joint_point[1] + target
        yli = joint_point[1] - target

        engine_fus_arr_up.append([xi, yui, zi])
        engine_fus_arr_up.append([xi, yli, zi])
        engine_fus_arr_up.append([xi, -yui, zi])
        engine_fus_arr_up.append([xi, -yli, zi])

engine_fus_arr_up = np.array(engine_fus_arr_up)

# engine(main wing bottom)
lower = -1
rin = 0.8
rout = 0.4
tin = 0.1

len = 4.0

tx = 0.4
ty = 0.4

k = 0.4

joint_point = [l * 0.5 + croot * tx, wf + (b / 2 - wf) * ty, lower * np.max(main_wing_arr[:, 2])]

zcen = joint_point[2] - tin - rin


# engine curve -> z = ax ** 2 + b * x + c
x = np.linspace(joint_point[0] - k * len, joint_point[0] + (1 - k) * len, 30)

az = lower * (rin - rout) / (1 - 2 * k) / len ** 2
bz = -2 * joint_point[0] * az
cz = joint_point[2] + bz ** 2 / (4 * az)

engine_arr_low = []

for xi in x:

    zu = az * xi ** 2 + bz * xi + cz

    zl = 2 * zcen - zu

    z = np.linspace(zl, zu, 30)

    for zi in z:
        target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
        yui = joint_point[1] + target
        yli = joint_point[1] - target

        engine_arr_low.append([xi, yui, zi])
        engine_arr_low.append([xi, yli, zi])
        engine_arr_low.append([xi, -yui, zi])
        engine_arr_low.append([xi, -yli, zi])


engine_arr_low = np.array(engine_arr_low)

# engine(main wing upper)
joint_point = [l * 0.5 + croot * tx, wf + (b / 2 - wf) * ty, np.max(main_wing_arr[:, 2])]

zcen = joint_point[2] + tin + rin

# engine curve -> z = ax ** 2 + b * x + c
x = np.linspace(joint_point[0] - k * len, joint_point[0] + (1 - k) * len, 30)

az = (rin - rout) / (1 - 2 * k) / len ** 2
bz = -2 * joint_point[0] * az
cz = joint_point[2] + bz ** 2 / (4 * az)

engine_arr_up = []

for xi in x:

    zl = az * xi ** 2 + bz * xi + cz

    zu = 2 * zcen - zl

    z = np.linspace(zl, zu, 30)

    for zi in z:
        target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
        yui = joint_point[1] + target
        yli = joint_point[1] - target

        engine_arr_up.append([xi, yui, zi])
        engine_arr_up.append([xi, yli, zi])
        engine_arr_up.append([xi, -yui, zi])
        engine_arr_up.append([xi, -yli, zi])


engine_arr_up = np.array(engine_arr_up)

# horizontal wing
chroot = 3
bh = 5
retreat_angleh = 40
chtip = chroot - b / 2 * np.tan(retreat_angleh * np.pi / 180.0)
# feasibility check(?) => ctip < 0 false

st = [l, 0, hau]

# airfoil
p = 0.5
tc = 0.08

bezier_yu = []
bezier_yl = []

theta = retreat_angle * np.pi / 180.0

qyu = np.array([[(l2 + st[0]) * 0.5, 0],
                [st[0] + 0 * np.tan(theta), 0],
                [0.5 * bh * np.tan(theta) + st[0], 0.5 * bh]])
qyl = np.array([[0.5 * bh * np.tan(theta) + st[0] + chtip, 0.5 * bh],
                [st[0] + chroot, 0], [l3, 0]])

for t in np.linspace(0, 1, 50):
    bezier_yu.append(bezier(2, t, qyu))
    bezier_yl.append(bezier(2, t, qyl))


bezier_yl = bezier_yl[::-1]
hori_wing_arr = []

for setu, setl in zip(bezier_yu, bezier_yl):
    xu, yu = setu
    xl, yl = setl
    cx = xl - xu

    x = np.linspace(xu, xl, 50)

    for xi in x:
        zui = -tc / (p * (1 - p) * cx) * (xi - xu) * (xi - xl) + st[2]
        zli = -1 * zui + st[2] * 2

        hori_wing_arr.append([xi, yu, zui])
        hori_wing_arr.append([xi, yu, zli])

        hori_wing_arr.append([xi, -yu, zui])
        hori_wing_arr.append([xi, -yu, zli])

hori_wing_arr = np.array(hori_wing_arr)


# 3D description
fig = plt.figure()
ax = Axes3D(fig)

transparency = 0.1

ax.scatter(cockpit_arr[:, 0], cockpit_arr[:, 1], cockpit_arr[:, 2], c='b', alpha=transparency)
ax.scatter(cabin_arr[:, 0], cabin_arr[:, 1], cabin_arr[:, 2], c='b', alpha=transparency)
ax.scatter(after_cabin_arr[:, 0], after_cabin_arr[:, 1], after_cabin_arr[:, 2], c='b',alpha=transparency)
ax.scatter(main_wing_arr[:, 0], main_wing_arr[:, 1], main_wing_arr[:, 2], c='b', alpha=transparency)
ax.scatter(hori_wing_arr[:, 0], hori_wing_arr[:, 1], hori_wing_arr[:, 2], c='b', alpha=transparency)
ax.scatter(engine_fus_arr_up[:, 0], engine_fus_arr_up[:, 1], engine_fus_arr_up[:, 2], c='r', alpha=transparency)
ax.scatter(engine_arr_up[:, 0], engine_arr_up[:, 1], engine_arr_up[:, 2], c='r', alpha=transparency)
ax.scatter(engine_arr_low[:, 0], engine_arr_low[:, 1], engine_arr_low[:, 2], c='r', alpha=transparency)


# set bound
ax.set_xlim([-10, 50])
ax.set_ylim([-20, 20])
ax.set_zlim([-15, 15])

plt.show()






