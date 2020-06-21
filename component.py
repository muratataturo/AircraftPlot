import numpy as np
from helper import bezier, turnover_3d
# helper function for view


# compute cockpit array
def compute_cockpit_arr(arg_class):
    """
    compute cockpit numpy array(3D)

    :param arg_class: argument class
    :return: cockpit_arr(numpy ndarray)
    """
    # set required parameters
    l1 = arg_class.l1  # section 1 length(cockpit)
    huc = arg_class.huc  # height of upper at cockpit
    huf = arg_class.huf  # height of upper at cabin(fuselage)
    hlc = arg_class.hlc  # height of lower at cockpit
    hlf = arg_class.hlf  # height of lower at cabin(fuselage)
    uk = arg_class.uk  # constant for bezier curve
    wc = arg_class.wc  # width of cockpit
    wf = arg_class.wf  # width of cabin(fuselage)

    # array for bezier curve
    qzu = np.array([[0, 0], [l1 * uk, huc], [l1, huf]])
    qzl = np.array([[0, 0], [l1 * uk, -hlc], [l1, -hlf]])
    qy = np.array([[0, 0], [l1 * uk, wc], [l1, wf]])

    # compute bezier curve
    bezier_zu = []  # z coords of upper line
    bezier_zl = []  # z coord of lower line
    bezier_y = []  # y coord
    for t in np.linspace(0, 1, 50):
        bezier_zu.append(bezier(qzu.shape[0] - 1, t, qzu)[1])
        bezier_zl.append(bezier(qzl.shape[0] - 1, t, qzl)[1])
        bezier_y.append(bezier(qy.shape[0] - 1, t, qy)[1])

    # compute cockpit array
    cockpit_arr = []
    # set x range
    x = np.linspace(0.0, l1, 50)

    for xi, bzl, bzu, by in zip(x, bezier_zl, bezier_zu, bezier_y):
        # set y range
        y = np.linspace(-by, by, 30)

        for yi in y:
            # eclipse
            if by == 0:
                zui, zli = 0, 0
            else:
                zui = bzu * np.sqrt(1.0 - yi ** 2 / by ** 2)
                zli = bzl * np.sqrt(1.0 - yi ** 2 / by ** 2)

            cockpit_arr.append([xi, yi, zui])
            cockpit_arr.append([xi, yi, zli])

    cockpit_arr = np.array(cockpit_arr)

    return cockpit_arr


# compute cabin arr
def compute_cabin_arr(arg_class):
    """
    compute cabin numpy array(3D)

    :param arg_class: argument class
    :return: cabin_arr(numpy ndarray)
    """
    # set required parameters
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    huf = arg_class.huf  # height of upper at cabin(fuselage)
    hlf = arg_class.hlf  # height of lower at cabin(fuselage)
    wf = arg_class.wf  # width of cabin(fuselage)

    # compute cabin arr
    # set x range
    x = np.linspace(l1, l1 + l2, 50)
    cabin_arr = []

    for xi in x:
        # set parameters for eclipse curve
        z_u = huf
        z_l = hlf

        b_u = z_u
        a_u = wf

        a_l = a_u
        b_l = z_l

        # set y range
        y = np.linspace(-a_u, a_u, 30)

        for yi in y:
            # eclipse curve
            zui = b_u * np.sqrt(1.0 - (yi / a_u) ** 2)
            zli = -1 * b_l * np.sqrt(1.0 - (yi / a_l) ** 2)

            cabin_arr.append([xi, yi, zui])
            cabin_arr.append([xi, yi, zli])

    cabin_arr = np.array(cabin_arr)

    return cabin_arr


# compute after cabin arr
def compute_after_cabin_arr(arg_class):
    """
    compute after cabin numpy array

    :param arg_class: argument class
    :return: after_cabin_arr(numpy ndarray)
    """
    # set required parameters
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)
    huf = arg_class.huf  # height of upper at cabin(fuselage)
    hau = arg_class.hau  # height of upper at after cabin
    hlf = arg_class.hlf  # height of lower at cabin(fuselage)
    hlc = arg_class.hlc  # height of lower at cockpit
    wa = arg_class.wa  # width of after cabin
    wf = arg_class.wf  # width of cabin(fuselage)

    # create bezier curve
    bezier_zu = []  # z coord for upper line
    bezier_zl = []  # z coord for lower line
    bezier_y = []  # y coord for y line

    # set array for bezier curve
    qzu = np.array([[l1 + l2, huf], [l1 + l2 + 0.5 * l3, hau], [l1 + l2 + l3, hau]])
    qzl = np.array([[l1 + l2, -hlf], [l1 + l2 + l3, -hlc], [l1 + l2 + l3, 0]])
    qy = np.array([[l1 + l2, wf], [l1 + l2 + l3, wa], [l1 + l2 + l3, 0]])

    # compute bezier curve
    for t in np.linspace(0, 1, 50):
        bezier_zu.append(bezier(qzu.shape[0] - 1, t, qzu)[1])
        bezier_zl.append(bezier(qzl.shape[0] - 1, t, qzl)[1])
        bezier_y.append(bezier(qy.shape[0] - 1, t, qy)[1])

    # compute after cabin array
    after_cabin_arr = []
    x = np.linspace(l1 + l2, l1 + l2 + l3, 50)

    for xi, bzl, bzu, by in zip(x, bezier_zl, bezier_zu, bezier_y):
        # set y range
        y = np.linspace(-by, by, 30)

        for yi in y:
            zui = bzu * np.sqrt(1.0 - yi ** 2 / by ** 2)
            zli = bzl * np.sqrt(1.0 - yi ** 2 / by ** 2)

            # exception
            if np.isnan(zui):
                zui, zli = 0, 0

            after_cabin_arr.append([xi, yi, zui])
            after_cabin_arr.append([xi, yi, zli])

    after_cabin_arr = np.array(after_cabin_arr)

    return after_cabin_arr


# compute main wing array
def compute_main_wing_arr(arg_class):
    """
    compute main wing numpy array

    :param arg_class: argument class
    :return: main_wing_arr
    """
    # set required parameters
    ctip = arg_class.ctip  # tip chord of main wing
    croot = arg_class.croot  # hub chord of main wing
    b = arg_class.b  # wing span
    theta = arg_class.theta  # retreat angle
    jmx = arg_class.jmx  # constant for x coord of mounting point
    jmz = arg_class.jmz  # constant for z coord of mounting point
    wf = arg_class.wf  # width of cabin(fuselage)
    pm = arg_class.pm  # constant for airfoil
    tcm = arg_class.tcm  # the ratio of thickness and chord
    l1 = arg_class.l1  # section 1 length
    l2 = arg_class.l2  # section 2 length
    l3 = arg_class.l3  # section 3 length

    # total fuselage length
    l = l1 + l2 + l3

    # start point of mounting point
    st = [l * jmx, wf, l * jmz]

    # set y range
    y = np.linspace(wf, 0.5 * b, 30)

    # helper constant for chord
    BX = croot * (0.5 * b - wf) / (croot - ctip)

    # compute main wing array
    main_wing_arr = []

    for yi in y:
        # x coord of upper line of main wing
        xu = np.tan(theta * np.pi / 180) * (yi - wf) + st[0]
        # chord of x axis
        cx = (1.0 - (yi - wf) / BX) * croot
        # x coord of lower line of main wing
        xl = xu + cx

        # set x range
        x = np.linspace(xu, xl, 30)

        for xi in x:
            # z coord of upper line of main wing
            zui = -tcm / (pm * (1 - pm) * cx) * (xi - xu) * (xi - xl)
            # z coord of lower line of main wing
            zli = -1 * zui

            main_wing_arr.append([xi, yi, zui])
            main_wing_arr.append([xi, yi, zli])
            # symmetric
            main_wing_arr.append([xi, -yi, zui])
            main_wing_arr.append([xi, -yi, zli])

    main_wing_arr = np.array(main_wing_arr)

    return main_wing_arr


# compute horizontal wing
def compute_horizontal_wing(arg_class):
    """
    compute horizontal wing numpy array

    :param arg_class: argument class
    :return: hori_wing_arr(numpy ndarray)
    """
    # set required parameters
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)
    chtip = arg_class.chtip  # tip chord of horizontal wing
    chroot = arg_class.chroot  # hub chord of horizontal wing
    bh = arg_class.bh  # horizontal wing span
    thetah = arg_class.thetah  # retreat angle of horizontal wing
    jhx = arg_class.jhx  # constant for x chord of mounting point
    jhz = arg_class.jhz  # constant for z chord of mounting point
    ph = arg_class.ph  # constant for airfoil
    tch = arg_class.tch  # the ratio of thickness and chord
    wf = arg_class.wf  # width of cabin(fuselage)

    # total fuselage length
    l = l1 + l2 + l3

    # helper constant for calculating horizontal wing's chord
    BXh = chroot * (0.5 * bh - wf) / (chroot - chtip)

    # start point of horizontal wing
    sth = [l * jhx, wf, l * jhz]
    # set y range
    y = np.linspace(wf, 0.5 * bh, 30)
    # Initialize horizontal wing array
    hori_wing_arr = []

    for yi in y:
        # upper line of horizontal wing
        xu = np.tan(thetah * np.pi / 180.0) * (yi - wf) + sth[0]
        # calculate chord length
        cx = (1.0 - (yi - wf) / BXh) * chroot
        # lower line of horizontal wing
        xl = xu + cx

        # set x range
        x = np.linspace(xu, xl, 30)

        for xi in x:
            # parabola
            zui = -tch / (ph * (1 - ph) * cx) * (xi - xu) * (xi - xl)
            zli = -1 * zui

            # add (x, y, z) to the array
            hori_wing_arr.append([xi, yi, zui])
            hori_wing_arr.append([xi, yi, zli])

            # symmetric
            hori_wing_arr.append([xi, -yi, zui])
            hori_wing_arr.append([xi, -yi, zli])

    hori_wing_arr = np.array(hori_wing_arr)

    return hori_wing_arr


# compute vertical wing
def compute_vertical_wing(arg_class):
    """
    compute vertical wing numpy array

    :param arg_class: argument class
    :return: vert_wing_arr(numpy ndarray)
    """
    # set required parameters
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)
    cvtip = arg_class.cvtip  # tip chord of vertical wing
    cvroot = arg_class.cvroot  # hub chord of vertical wing
    bv = arg_class.bv  # vertical wing span
    thetav = arg_class.thetav  # retreat angle of vertical wing
    jvx = arg_class.jvx  # constant for x chord of mounting point
    jvz = arg_class.jvz  # constant for z chord of mounting point
    pv = arg_class.ph  # constant for airfoil
    tcv = arg_class.tch  # the ratio of thickness and chord
    hau = arg_class.hau  # upper height of after cabin
    wf = arg_class.wf  # width of cabin(fuselage)

    # total fuselage length
    l = l1 + l2 + l3

    # helper constant for calculating vertical wing's chord
    BXv = cvroot * (0.5 * bv - hau) / (cvroot - cvtip)

    # start point of vertical wing
    sth = [l * jvx, wf, l * jvz]
    # set z range
    z = np.linspace(hau, 0.5 * bv, 30)
    # Initialize vertical wing array
    vert_wing_arr = []

    for zi in z:
        # upper line of horizontal wing
        xu = np.tan(thetav * np.pi / 180.0) * (zi - hau) + sth[0]
        # calculate chord length
        cx = (1.0 - (zi - hau) / BXv) * cvroot
        # lower line of horizontal wing
        xl = xu + cx

        # set x range
        x = np.linspace(xu, xl, 30)

        for xi in x:
            # parabola
            yui = -tcv / (pv * (1 - pv) * cx) * (xi - xu) * (xi - xl)
            yli = -1 * yui

            # add (x, y, z) to the array
            vert_wing_arr.append([xi, yui, zi])
            vert_wing_arr.append([xi, yli, zi])

    vert_wing_arr = np.array(vert_wing_arr)

    return vert_wing_arr


# compute engine
# engine which is equipped at lower part of main wing
def compute_engine_lower_main_wing(arg_class, main_wing_arr):
    """
    compute core engine array, which is equipped at lower main wing

    :param arg_class: argument class
    :param main_wing_arr: array of main wing
    :return: engine_arr(numpy ndarray)
    """
    # set required parameters
    rein = arg_class.rein  # inlet radius of engine
    reout = arg_class.reout  # nozzle radius of engine
    tein = arg_class.tein  # joint margin
    le = arg_class.le  # engine length
    tcx = arg_class.tcx  # coefficient of x to root chord
    tcy = arg_class.tcy  # coefficient of y to wing span
    tcz = arg_class.tcz  # coefficient of z to cabin height
    jmx = arg_class.jmx  # constant for x coord of mounting point
    croot = arg_class.croot  # root chord of main wing
    wf = arg_class.wf  # width of cabin(fuselage)
    b = arg_class.b  # main wing span
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)

    # total cabin length
    l = l1 + l2 + l3

    # joint point chords
    joint_point = [l * jmx + croot * tcx, wf + (0.5 * b - wf) * tcy, -1 * np.max(main_wing_arr[:, 2])]

    # the center coordinates of engine(z coord)
    zcen = joint_point[2] - tein - rein

    # consider the outer curve of engine as parabola curve(z = a * x ** 2 + b * x + c)
    # set x range
    x = np.linspace(joint_point[0] - tcz * le, joint_point[0] + (1.0 - tcz) * le, 30)

    # compute constant of outer line
    az = -1 * (rein - reout) / (1 - 2 * tcz) / le ** 2
    bz = -2 * joint_point[0] * az
    cz = joint_point[2] + bz ** 2 / (4 * az)

    # Initialize engine arr
    engine_arr_low = []

    for xi in x:
        # outer engine curve
        # upper line
        zu = az * xi ** 2 + bz * xi + cz
        # lower line
        zl = 2 * zcen - zu

        # set z range
        z = np.linspace(zl, zu, 30)

        for zi in z:
            # eclipse cross section
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            # upper line
            yui = joint_point[1] + target
            # lower line
            yli = joint_point[1] - target

            # add (x, y, z) to array
            engine_arr_low.append([xi, yui, zi])
            engine_arr_low.append([xi, yli, zi])
            # symmetric
            engine_arr_low.append([xi, -yui, zi])
            engine_arr_low.append([xi, -yli, zi])

    engine_arr_low = np.array(engine_arr_low)

    return engine_arr_low


# engine which is equipped with upper part of main wing
def compute_engine_upper_main_wing(arg_class, main_wing_arr):
    """
    compute upper main wing engine array

    :param arg_class: argument class
    :param main_wing_arr: array of main wing
    :return: engine_arr_up(numpy ndarray)
    """

    # set required parameters
    rein = arg_class.rein  # inlet radius of engine
    reout = arg_class.reout  # nozzle radius of engine
    tein = arg_class.tein  # joint margin
    le = arg_class.le  # engine length
    tcx = arg_class.tcx  # coefficient of x to root chord
    tcy = arg_class.tcy  # coefficient of y to wing span
    tcz = arg_class.tcz  # coefficient of z to cabin height
    jmx = arg_class.jmx  # constant for x coord of mounting point
    croot = arg_class.croot  # root chord of main wing
    wf = arg_class.wf  # width of cabin(fuselage)
    b = arg_class.b  # main wing span
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)

    # total cabin length
    l = l1 + l2 + l3

    # set engine joint point
    joint_point = [l * jmx + croot * tcx, wf + (0.5 * b - wf) * tcy, np.max(main_wing_arr[:, 2])]
    # z coord at the center of engine
    zcen = joint_point[2] + tein + rein

    # set x range
    x = np.linspace(joint_point[0] - tcz * le, joint_point[0] + (1 - tcz) * le, 30)

    # compute constant for describing engine outer line
    az = (rein - reout) / (1 - 2 * tcz) / le ** 2
    bz = -2 * joint_point[0] * az
    cz = joint_point[2] + bz ** 2 / (4 * az)

    # Initialize engine array
    engine_arr_up = []

    for xi in x:
        # lower line
        zl = az * xi ** 2 + bz * xi + cz
        # upper line
        zu = 2 * zcen - zl
        # set z range
        z = np.linspace(zl, zu, 30)

        for zi in z:
            # eclipse curve(cross section)
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            yui = joint_point[1] + target
            yli = joint_point[1] - target

            # add engine array
            engine_arr_up.append([xi, yui, zi])
            engine_arr_up.append([xi, yli, zi])

            # symmetric
            engine_arr_up.append([xi, -yui, zi])
            engine_arr_up.append([xi, -yli, zi])

    engine_arr_up = np.array(engine_arr_up)

    return engine_arr_up


# engine which is equipped with upper part of cabin(fuselage)
def compute_engine_upper_cabin(arg_class, cabin_arr):
    """
    compute engine upper cabin array

    :param arg_class: argument class
    :param cabin_arr: cabin array
    :return: engine_fus_arr_up(numpy ndarray)
    """
    # set required parameters
    rein = arg_class.rein  # inlet radius of engine
    reout = arg_class.reout  # nozzle radius of engine
    tein = arg_class.tein  # joint margin
    le = arg_class.le  # engine length
    thetae = arg_class.thetae  # angle for engine equipment
    tcx = arg_class.tcx  # coefficient of x to root chord
    tcz = arg_class.tcz  # coefficient of z to cabin height
    l1 = arg_class.l1  # section 1 length(cockpit)
    l2 = arg_class.l2  # section 2 length(cabin)
    l3 = arg_class.l3  # section 3 length(after cabin)

    # total cabin length
    l = l1 + l2 + l3

    # max cabin y coords
    eca = np.max(cabin_arr[:, 1])
    # max cabin z coords
    ecb = np.max(cabin_arr[:, 2])

    # convert radians
    thetae = thetae * np.pi / 180.0

    # calculate distance between cabin center and engine center at yz plane
    # original point is considered as cabin center and assume polar coordnates
    r = np.sqrt((eca * np.cos(thetae)) ** 2 + (ecb * np.cos(thetae)) ** 2)

    # set engine joint point
    joint_point = [l * tcx, r * np.cos(thetae), r * np.sin(thetae)]
    # z coord of center of engine
    zcen = (r + rein + tein) * np.sin(thetae)

    # compute constant for outer engine line
    az = (rein - reout) * np.cos(thetae) / (1 - 2 * tcz) / le ** 2
    bz = (tcz * le - 2 * joint_point[0]) * az - tein * np.cos(thetae) / (tcz * le)
    cz = joint_point[2] - (rein + tein) * np.cos(thetae) - az * joint_point[0] ** 2 - bz * joint_point[0]

    # set x range
    x = np.linspace(joint_point[0] - tcz * le, joint_point[0] + (1 - tcz) * le, 30)

    # Initialize engine arr
    engine_fus_arr_up = []

    for xi in x:
        # engine lower line
        zl = az * xi ** 2 + bz * xi + cz
        # engine upper line
        zu = 2 * zcen - zl
        # set z range
        z = np.linspace(zl, zu, 30)

        for zi in z:
            # eclipse line
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            yui = joint_point[1] + target
            yli = joint_point[1] - target

            engine_fus_arr_up.append([xi, yui, zi])
            engine_fus_arr_up.append([xi, yli, zi])

            # symmetric
            engine_fus_arr_up.append([xi, -yui, zi])
            engine_fus_arr_up.append([xi, -yli, zi])

    engine_fus_arr_up = np.array(engine_fus_arr_up)

    return engine_fus_arr_up


# compute distributed electric fan
# distributed electric fan equipping with some parts of main wing(upper or lower)
def compute_distributed_fan_at_main_wing(arg_class, main_wing_arr):
    # distributed fan parameters
    nfan = arg_class.nfan  # the number of distributed electric fan
    rfin = arg_class.rfin  # radius of distributed electric fan
    rfout = arg_class.rfout  # radius of distributed electric fan
    r_margin = 0.1  # margin for radius of electric fan
    theta = arg_class.theta * np.pi / 180.0  # retreat angle
    tfin = arg_class.tfin  # margin for connecting a distributed electric fan to wing
    lfan = arg_class.lfan  # overall length of distributed electric fan
    tfz = arg_class.tfz  # z coord constant for joint

    # core engine and main wing parameters
    jmx = arg_class.jmx  # x coord coefficient of joint main wing
    tcx = arg_class.tcx  # x chord constant for joint core engine
    tcy = arg_class.tcy  # y chord constant for joint core engine
    wf = arg_class.wf  # width of cabin(fuselage)
    b = arg_class.b  # width of main wing
    croot = arg_class.croot  # root chord of main wing
    l = arg_class.l1 + arg_class.l2 + arg_class.l3  # fuselage(cabin) length

    # sign which indicates where to joint
    if arg_class.dist_fan_settings == 'lower_mainwing':
        sign = -1
    else:
        sign = 1

    # joint point's coords
    joint_point_init = [l * jmx + croot * tcx, wf + (b / 2 - wf) * tcy, sign * np.max(main_wing_arr[:, 2])]
    # distributed fan array
    distributed_fan_arr = []

    for n in range(nfan):
        diff_r = (1.0 + r_margin) * 2 * (n + 1)  # determine setting point
        joint_point = [joint_point_init[0] + diff_r * np.sin(theta),
                       joint_point_init[1] + diff_r * np.cos(theta),
                       joint_point_init[2]]
        # center of z coord
        zcen = joint_point_init[2] - tfin - rfin

        # x range
        x = np.linspace(joint_point[0] - tfz * lfan, joint_point[0] + (1.0 - tfz) * lfan, 30)

        # parabola curve parameters => z = a * x** 2 + b * x + c
        az = sign * (rfin - rfout) / (1 - 2 * tfz) / lfan ** 2
        bz = -2 * joint_point[0] * az
        cz = joint_point[2] + bz ** 2 / (4 * az)

        for xi in x:
            # upper line coords
            zu = az * xi ** 2 + bz * xi + cz
            # lower line coords
            zl = 2 * zcen - zu

            # z range
            z = np.linspace(zl, zu, 30)

            # eclipse curve
            for zi in z:
                target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
                yui = joint_point[0] + target
                yli = joint_point[0] - target

                distributed_fan_arr.append([xi, yui, zi])
                distributed_fan_arr.append([xi, yli, zi])
                # symmetric
                distributed_fan_arr.append([xi, -yui, zi])
                distributed_fan_arr.append([xi, -yli, zi])

    distributed_fan_arr = np.array(distributed_fan_arr)

    return distributed_fan_arr


# distributed electric fan equipping with upper cabin(fuselage)
def compute_distributed_fan_upper_cabin(arg_class, cabin_arr):
    # distributed fan parameters
    nfan = arg_class.nfan  # the number of distributed electric fan
    rfin = arg_class.rfin  # radius of distributed electric fan
    rfout = arg_class.rfout  # radius of distributed electric fan
    theta = arg_class.theta * np.pi / 180.0  # retreat angle
    tfin = arg_class.tfin  # margin for connecting a distributed electric fan to wing
    lfan = arg_class.lfan  # overall length of distributed electric fan
    tfz = arg_class.tfz  # z coord constant for joint
    tfx = arg_class.tfx  # x coord constant for joint at cabin
    thetaf = arg_class.thetaf * np.pi / 180.0  # joint angle of distributed electric fan

    l = arg_class.l1 + arg_class.l2 + arg_class.l3  # cabin length

    eca = np.max(cabin_arr[:, 1])
    ecb = np.max(cabin_arr[:, 2])

    # distance between cabin center and distributed electric fan center
    r = np.sqrt((eca * np.cos(thetaf)) ** 2 + (ecb * np.sin(thetaf)) ** 2)

    # joint point
    joint_point = [l * tfx, r * np.cos(thetaf), r * np.sin(thetaf)]

    # center of z coords
    zcen = (r + rfin + tfin) * np.sin(thetaf)

    # parabola curve parameters
    az = (rfin - rfout) * np.cos(thetaf) / (1 - 2 * tfz) / lfan ** 2
    bz = (tfz * lfan - 2 * joint_point[0]) * az - tfin * np.cos(thetaf) / (tfz * lfan)
    cz = joint_point[2] - (rfin + tfin) * np.cos(thetaf) - az * joint_point[0] ** 2 - bz * joint_point[0]

    # x range
    x = np.linspace(joint_point[0] - tfz * lfan, joint_point[0] + (1.0 - tfz) * lfan, 30)

    distributed_fan_upp_arr = []

    for xi in x:
        # distributed fan outer line
        zl = az * xi ** 2 + bz * xi + cz
        zu = zl + (zcen - zl) * 2

        # z range
        z = np.linspace(zl, zu, 30)

        for zi in z:
            target = np.sqrt((zu - zcen) ** 2 - (zi - zcen) ** 2)
            yui = joint_point[1] + target
            yli = joint_point[1] - target

            distributed_fan_upp_arr.append([xi, yui, zi])
            distributed_fan_upp_arr.append([xi, yli, zi])

            if thetaf * 180 / np.pi == 90:
                distributed_fan_upp_arr.append([xi, -yui, zi])
                distributed_fan_upp_arr.append([xi, -yli, zi])

    distributed_fan_upp_arr = np.array(distributed_fan_upp_arr)

    return distributed_fan_upp_arr


# compute propeller
# propeller engine with standard position
def compute_propeller_with_normal_position(arg_class, cabin_arr):
    """
    compute propeller array and connected arm array

    :param cabin_arr: numpy array of cabin
    :param arg_class: argument class
    :return: propeller_arr, arm_arr
    """

    l1 = arg_class.l1
    l2 = arg_class.l2
    l3 = arg_class.l3

    # fuselage length
    l = l1 + l2 + l3

    # propeller setting ratio
    txs = arg_class.txs  # the ratio of setting position corresponding to overall length
    angles = arg_class.angles  # angle of arm which is connected with a propeller

    # outer line of the collection of propeller
    radius = arg_class.radius
    # the radius of each propeller
    pr = arg_class.pr
    # the arm length
    lp = arg_class.lp
    # setting shift
    zdiffp = arg_class.zdiffp

    # setting coefficient for arm on z axis
    k = arg_class.k

    # argm radius
    arm_r = arg_class.arm_r

    # propeller number(because of symmetric, get the half number of propellers)
    half_propeller_number = len(txs)

    # coords of joint point
    joint_points = []
    for idx in range(half_propeller_number):
        point = [l * txs[idx], np.max(cabin_arr[:, 1]), idx * zdiffp]
        joint_points.append(point)

    # coords of propellers at left side
    propeller_arr_l = []
    # coords of propellers at right side
    propeller_arr_r = []

    for angle, joint_point in zip(angles, joint_points):
        angle = 180 - angle
        angle = angle * np.pi / 180.0
        # get center coords
        center = np.array([joint_point[0] + (radius + pr) * np.cos(angle),
                           joint_point[1] + (radius + pr) * np.sin(angle),
                           joint_point[2]])

        # z range
        z = np.linspace(-k * lp + joint_point[2], (1 - k) * lp + joint_point[2], 30)

        for zi in z:

            # x range(create circle)
            x = np.linspace(center[0] - pr, center[0] + pr, 30)

            for xi in x:
                target = np.sqrt(pr ** 2 - (xi - center[0]) ** 2)
                yui = center[1] + target
                yli = center[1] - target

                # left side
                plu = [xi, yui, zi]
                pll = [xi, yli, zi]
                propeller_arr_l.append(plu)
                propeller_arr_l.append(pll)

                # right side
                pru = [xi, -yui, zi]
                prl = [xi, -yli, zi]
                propeller_arr_r.append(pru)
                propeller_arr_r.append(prl)


    propeller_arr_r = np.array(propeller_arr_r)
    propeller_arr_l = np.array(propeller_arr_l)

    # put together propeller arr
    propeller_arr = np.concatenate([propeller_arr_l, propeller_arr_r], axis=0)

    # create arm
    arm_arr = []
    # right part
    x = np.linspace(0, radius + pr, 30)
    for xi in x:
        y = np.linspace(-arm_r, arm_r, 30)

        for yi in y:
            target = np.sqrt(arm_r ** 2 - yi ** 2)
            zui = target
            zli = -target

            pu = [xi, yi, zui]
            pl = [xi, yi, zli]

            for idx in range(half_propeller_number):
                rep_j = joint_points[idx]
                angle = angles[idx]

                # turn over 3d on z axis against upper part
                angle_u = -1 * (180 - angle) * np.pi / 180.0
                t_arr_u = turnover_3d(angle_u, np.array([0, 0, 1]))

                # turn over 3d on z axis against left part
                angle_l = 180 * np.pi / 180.0
                t_arr_l = turnover_3d(angle_l, np.array([0, 0, 1]))

                puu = np.dot(t_arr_u.T, np.array(pu)) + np.array(rep_j)
                pll = np.dot(t_arr_l.T, puu) + np.array([l, 0, -2 * zdiffp * idx + (half_propeller_number - 1) * zdiffp])

                arm_arr.append(puu.tolist())
                arm_arr.append(pll.tolist())

    arm_arr = np.array(arm_arr)

    return propeller_arr, arm_arr













