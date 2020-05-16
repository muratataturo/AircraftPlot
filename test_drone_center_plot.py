import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

huf = 1.5
hlf = 0.2
wf = 1.2

hau = 0.3

upper_r = huf / wf
upper_l = hlf / wf

l1 = 3
l2 = 6
l3 = 7

l = l3

# cockpit part
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


# after cabin part
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

joint_radius = 3.0
joint_angle = 30
diff_angle = 90
pr = 0.8  # propeller radius
lp = 0.8

tx = 0.1

joint_point = [l1 + (l2 - l1) * tx, 0, 0]

pr_cen = [joint_point[0] - (joint_radius + pr) * np.sin(joint_angle * np.pi / 180.0),
          joint_point[1] + (joint_radius + pr) * np.cos(joint_angle * np.pi / 180.0),
          joint_point[2]]

k = 0.3  # joint coefficient

z = np.linspace(-(1 - k) * lp, k * lp, 30)

propeller_arr = []

for zi in z:

    x = np.linspace(pr_cen[0] - pr, pr_cen[0] + pr, 30)

    for xi in x:
        target = np.sqrt(pr ** 2 - (xi - pr_cen[0]) ** 2)
        yui = pr_cen[1] + target
        yli = pr_cen[1] - target

        propeller_arr.append([xi, yui, zi])
        propeller_arr.append([xi, yli, zi])
        lr = (joint_radius + pr) / np.sin(45 * np.pi / 180.0)
        propeller_arr.append([xi + lr * np.cos((45 - joint_angle) * np.pi / 180.0), yui - lr * np.sin((45 - joint_angle) * np.pi / 180.0), zi])
        propeller_arr.append([xi + lr * np.cos((45 - joint_angle) * np.pi / 180.0), yli - lr * np.sin((45 - joint_angle) * np.pi / 180.0), zi])

propeller_arr = np.array(propeller_arr)

# 3D turnover array
theta = 180
theta = theta * np.pi / 180.0
n = np.array([1, 0, 0])  # z axis unit vector

propeller_arr1 = []

for p_arr in propeller_arr:
    t_arr = turnover_3d(theta, n)
    target_vec = np.dot(t_arr.T, p_arr) - np.array([0, 0, 0.5 * lp])
    propeller_arr1.append(target_vec)


propeller_arr1 = np.array(propeller_arr1)

# poll
poll_r = 0.1
x = np.linspace(joint_point[0] - joint_radius - pr, joint_point[0], 30)

poll_arr = []

for xi in x:

    y = np.linspace(-poll_r, poll_r, 30)

    for yi in y:
        zui = np.sqrt(poll_r ** 2 - yi ** 2)
        zli = -zui

        poll_arr.append([xi, yi, zui])
        poll_arr.append([xi, yi, zli])


# 3D turnover
# 3D turnover array
thetas = np.array([joint_angle, joint_angle + diff_angle])
# thetas = np.array([60, 120, 180, 240, 300, 360])
thetas = thetas * np.pi / 180.0
n = np.array([0, 0, 1])  # z axis unit vector

poll_cen = [joint_point[0], joint_point[1], joint_point[2]]
poll_cen = np.array(poll_cen)

poll_arr1 = []
for p_arr in poll_arr:

    for theta in thetas:
        t_arr = turnover_3d(theta, n)
        p = np.dot(t_arr.T, p_arr) + poll_cen
        poll_arr1.append(p)


poll_arr1 = np.array(poll_arr1)

# horizontal flip
poll_arr2 = []

for p_arr in poll_arr1:
    t_arr = turnover_3d(180 - diff_angle / 2, np.array([1, 0, 0]))
    p = np.dot(t_arr.T, p_arr) - np.array([0, 0, 0.5 * poll_r])
    poll_arr2.append(p)

poll_arr2 = np.array(poll_arr2)




# 3D plot
fig = plt.figure()

ax = Axes3D(fig)

ax.scatter(cockpit_arr[:, 0], cockpit_arr[:, 1], cockpit_arr[:, 2])
ax.scatter(cabin_arr[:, 0], cabin_arr[:, 1], cabin_arr[:, 2])
ax.scatter(after_cabin_arr[:, 0], after_cabin_arr[:, 1], after_cabin_arr[:, 2])
ax.scatter(propeller_arr[:, 0], propeller_arr[:, 1], propeller_arr[:, 2])
ax.scatter(propeller_arr1[:, 0], propeller_arr1[:, 1], propeller_arr1[:, 2])
ax.scatter(poll_arr1[:, 0], poll_arr1[:, 1], poll_arr1[:, 2])
ax.scatter(poll_arr2[:, 0], poll_arr2[:, 1], poll_arr2[:, 2])

ax.set_xlim([-2, 8])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])

# plt.savefig('./Pictures/drone_center.png')

plt.show()




