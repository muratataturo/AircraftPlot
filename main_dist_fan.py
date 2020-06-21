import argparse
import pandas as pd

from component import compute_cockpit_arr, compute_cabin_arr, compute_after_cabin_arr
from component import compute_engine_upper_cabin, compute_engine_lower_main_wing, compute_engine_upper_main_wing
from component import compute_main_wing_arr, compute_horizontal_wing, compute_vertical_wing
from component import compute_distributed_fan_at_main_wing, compute_distributed_fan_upper_cabin

from .helper import draw_aircraft

# load arguments
def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cname', default='a320_dist', type=str)
    parser.add_argument('--aircraft_type', default='normal', type=str,
                        help='1. normal, 2. drone, 3. blended wing body, 4. hyper sonic, 5. propeller')
    parser.add_argument('--engine_type', default='distributed fan', type=str, help='1. turbofan 2. propeller 3. distributed fan(turbofan + electric fan)')
    args = parser.parse_args()

    return args


# function to create database
def insert_args():
    # setting argument class
    parser = argparse.ArgumentParser()

    # add the arguments
    # case name
    parser.add_argument('--cname', default='a320_dist', type=str)
    # engine settings
    parser.add_argument('--aircraft_type', default='normal', type=str)
    parser.add_argument('--engine_type', default='distributed fan', type=str)
    parser.add_argument('--core_engine_settings', default='lower_mainwing', type=str, help='1.lower_mainwing, 2.upper_mainwing, 3. upper_cabin')
    # distributed fan settings
    parser.add_argument('--dist_fan_settings', default='lower_mainwing', type=str, help='1.lower_mainwing, 2.upper_mainwing, 3.upper_cabin')
    # cockpit
    parser.add_argument('--huc', default=1.8, type=float, help='height of upper part of cockpit [m]')
    parser.add_argument('--hlc', default=1.8, type=float, help='height of lower part of cockpit [m]')
    parser.add_argument('--wc', default=1.2, type=float, help='cockpit width')

    # fuselage
    parser.add_argument('--huf', default=2.0, type=float, help='height of upper part of cabin(fuselage) [m]')
    parser.add_argument('--wf', default=2.0, type=float, help='width of cabin(fuselage) [m]')
    parser.add_argument('--hlf', default=2.1, type=float, help='height of lower part of cabin(fuselage) [m]')

    # after cabin
    parser.add_argument('--hau', default=1.5, type=float, help='height of upper part of after cabin [m]')
    parser.add_argument('--wa', default=0.3, type=float, help='width of after cabin')

    # length
    parser.add_argument('--l1', default=7, type=float, help='cockpit length [m]')
    parser.add_argument('--l2', default=25, type=float, help='cabin length [m]')
    parser.add_argument('--l3', default=4, type=float, help='after cabin length [m]')

    # cockpit control
    parser.add_argument('--uk', default=0.5, type=float, help='control coefficient for bezier curve of cockpit')

    # main wing
    parser.add_argument('--ctip', default=1.0, type=float, help='tip chord of main wing [m]')
    parser.add_argument('--croot', default=5.0, type=float, help='root chord of main wing [m]')
    parser.add_argument('--b', default=40, type=float, help='main wing span [m]')
    parser.add_argument('--theta', default=25, type=float, help='retreat angle of main wing')
    parser.add_argument('--jmx', default=0.4, type=float, help='x coord coefficient of joint main wing')
    parser.add_argument('--jmz', default=0.0, type=float, help='z coord coefficient of joint main wing')
    parser.add_argument('--pm', default=0.4, type=float, help='constant for main wing airfoil')
    parser.add_argument('--tcm', default=0.11, type=float, help='the ratio of thickness and chord of main wing')

    # horizontal wing
    parser.add_argument('--chtip', default=0.6, type=float, help='tip chord of horizontal wing [m]')
    parser.add_argument('--chroot', default=5.0, type=float, help='root chord of horizontal wing [m]')
    parser.add_argument('--bh', default=15, type=float, help='horizontal wing span [m]')
    parser.add_argument('--thetah', default=20, type=float, help='retreat angle of horizontal wing')
    parser.add_argument('--jhx', default=0.9, type=float, help='x coord coefficient of joint horizontal wing')
    parser.add_argument('--jhz', default=0.0, type=float, help='z coord coefficient of joint horizontal wing')
    parser.add_argument('--ph', default=0.4, type=float, help='constant for horizontal wing airfoil')
    parser.add_argument('--tch', default=0.11, type=float, help='the ratio of thickness and chord of horizontal wing')

    # vertical wing
    parser.add_argument('--cvtip', default=0.6, type=float, help='tip chord of vertical wing [m]')
    parser.add_argument('--cvroot', default=3.0, type=float, help='root chord of vertical wing [m]')
    parser.add_argument('--bv', default=10, type=float, help='vertical wing span [m]')
    parser.add_argument('--thetav', default=45, type=float, help='retreat angle of vertical wing')
    parser.add_argument('--jvx', default=0.95, type=float, help='x coord coefficient of joint vertical wing')
    parser.add_argument('--jvz', default=0.0, type=float, help='z coord coefficient of joint vertical wing')
    parser.add_argument('--pv', default=0.4, type=float, help='constant for vertical wing airfoil')
    parser.add_argument('--tcv', default=0.1, type=float, help='the ratio of thickness and chord of vertical wing')

    # engine
    parser.add_argument('--rein', default=1.0, type=float, help='radius of inlet core engine [m]')
    parser.add_argument('--reout', default=0.6, type=float, help='radius of outlet core engine [m]')
    parser.add_argument('--tein', default=0.1, type=float, help='margin for joint engine to wing [m]')
    parser.add_argument('--le', default=4.0, type=float, help='core engine length [m]')
    parser.add_argument('--tcx', default=0.4, type=float, help='x chord constant for joint engine')
    parser.add_argument('--tcy', default=0.4, type=float, help='y chord constant for joint engine')
    parser.add_argument('--tcz', default=0.4, type=float, help='z chord constant for joint engine')
    # add option (upper fuselage)
    parser.add_argument('--thetae', default=30, type=float, help='turnover angle for setting engine')

    # distributed fan
    parser.add_argument('--rfin', default=0.6, type=float, help='radius of inlet electric fan')
    parser.add_argument('--rfout', default=0.4, type=float, help='radius of outlet electric fan')
    parser.add_argument('--tfin', default=0.1, type=float, help='margin for connecting engine to wing')
    parser.add_argument('--nfan', default=6, type=float, help='the number of electric fan')
    parser.add_argument('--lfan', default=2.0, type=float, help='overall length of electric fan')
    parser.add_argument('--tfz', default=0.1, type=float, help='z chord constant for joint electric fan')
    # add option (upper fuselage)
    parser.add_argument('--tfx', default=0.7, type=float,
                        help='x chord constant for joint electric fan only in case of upper fuselage option')
    parser.add_argument('--thetaf', default=90, type=float, help='turnover angle for setting electric fan')

    args = parser.parse_args()

    return args


class Arguments(object):

    def __init__(self, args):
        cname = args.cname

        fname = './AircraftData/{}.csv'.format(cname)

        df = pd.read_csv(fname)
        self.aircraft_type = args.aircraft_type
        self.engine_type = args.engine_type
        self.core_engine_settings = df['core_engine_settings'].values[0]
        self.dist_fan_settings = df['dist_fan_settings'].values[0]
        self.huc = df['huc'].values[0]
        self.hlc = df['hlc'].values[0]
        self.wc = df['wc'].values[0]
        self.hlf = df['hlf'].values[0]
        self.huf = df['huf'].values[0]
        self.wf = df['wf'].values[0]
        self.hau = df['hau'].values[0]
        self.wa = df['wa'].values[0]
        self.l1 = df['l1'].values[0]
        self.l2 = df['l2'].values[0]
        self.l3 = df['l3'].values[0]
        self.uk = df['uk'].values[0]
        self.ctip = df['ctip'].values[0]
        self.croot = df['croot'].values[0]
        self.b = df['b'].values[0]
        self.theta = df['theta'].values[0]
        self.jmx = df['jmx'].values[0]
        self.jmz = df['jmz'].values[0]
        self.pm = df['pm'].values[0]
        self.tcm = df['tcm'].values[0]
        self.chtip = df['chtip'].values[0]
        self.chroot = df['chroot'].values[0]
        self.bh = df['bh'].values[0]
        self.thetah = df['thetah'].values[0]
        self.jhx = df['jhx'].values[0]
        self.jhz = df['jhz'].values[0]
        self.ph = df['ph'].values[0]
        self.tch = df['tch'].values[0]
        self.cvtip = df['cvtip'].values[0]
        self.cvroot = df['cvroot'].values[0]
        self.bv = df['bv'].values[0]
        self.thetav = df['thetav'].values[0]
        self.jvx = df['jvx'].values[0]
        self.jvz = df['jvz'].values[0]
        self.pv = df['pv'].values[0]
        self.tcv = df['tcv'].values[0]
        self.rein = df['rein'].values[0]
        self.reout = df['reout'].values[0]
        self.tein = df['tein'].values[0]
        self.le = df['le'].values[0]
        self.tcx = df['tcx'].values[0]
        self.tcy = df['tcy'].values[0]
        self.tcz = df['tcz'].values[0]
        self.thetae = df['thetae'].values[0]
        self.rfin = df['rfin'].values[0]
        self.rfout = df['rfout'].values[0]
        self.tfin = df['tfin'].values[0]
        self.nfan = df['nfan'].values[0]
        self.lfan = df['lfan'].values[0]
        self.tfz = df['tfz'].values[0]
        self.tfx = df['tfx'].values[0]
        self.thetaf = df['thetaf'].values[0]


if __name__ == '__main__':
    # ToDo: test following code after writing a320_dist.csv
    # variables names
    names = ['huc', 'hlc', 'wc',
             'hlf', 'huf', 'wf',
             'hau', 'wa',
             'l1', 'l2', 'l3',
             'uk',
             'ctip', 'croot', 'b', 'theta', 'jmx', 'jmz', 'pm', 'tcm',
             'chtip', 'chroot', 'bh', 'thetah', 'jhx', 'jhz', 'ph', 'tch',
             'cvtip', 'cvroot', 'bv', 'thetav', 'jvx', 'jvz', 'pv', 'tcv',
             'rein', 'reout', 'tein', 'le', 'tcx', 'tcy', 'tcz', 'thetae',
             'rfin', 'rfout', 'tfin', 'nfan', 'lfan', 'tfz', 'tfx', 'thetaf']

    # data type
    mode = 'load'  # 'insert' or 'load'

    if mode == 'insert':
        args = insert_args()

    else:
        l_args = load_args()
        args = Arguments(l_args)

    # cockpit
    cockpit_arr = compute_cockpit_arr(args)
    # cabin(fuselage)
    cabin_arr = compute_cabin_arr(args)
    # after cabin
    after_cabin_arr = compute_after_cabin_arr(args)
    # main wing
    main_wing_arr = compute_main_wing_arr(args)
    # horizontal wing
    hori_wing_arr = compute_horizontal_wing(args)
    # vertical wing
    vert_wing_arr = compute_vertical_wing(args)

    # core engine
    engine_arr = []
    if args.core_engine_settings == 'lower_mainwing':
        engine_arr = compute_engine_lower_main_wing(args, main_wing_arr)
    elif args.core_engine_settings == 'upper_mainwing':
        engine_arr = compute_engine_upper_main_wing(args, main_wing_arr)
    elif args.core_engine_settings == 'upper_cabin':
        engine_arr = compute_engine_upper_cabin(args, cabin_arr)

    # distributed electric fan
    distributed_fan_arr = []
    if args.dist_fan_settings == 'lower_mainwing' or args.dist_fan_settings == 'upper_mainwing':
        distributed_fan_arr = compute_distributed_fan_at_main_wing(args, main_wing_arr)
    elif args.dist_fan_settings == 'upper_cabin':
        distributed_fan_arr = compute_distributed_fan_upper_cabin(args, cabin_arr)

    # component names
    component_names = ['cockpit', 'cabin', 'after_cabin', 'main_wing', 'hori_wing', 'vert_wing', 'engine', 'distributed_fan']
    # component_arrays
    component_arrs = [cockpit_arr, cabin_arr, after_cabin_arr, main_wing_arr, hori_wing_arr, vert_wing_arr, engine_arr, distributed_fan_arr]

    # create component dictionary
    component_dict = {}

    for key, val in zip(component_names, component_arrs):
        component_dict[key] = val

    # description
    axis_bounds = [[-10, 40], [-20, 20], [-15, 15]]
    draw_aircraft(component_dict, axis_bounds)


