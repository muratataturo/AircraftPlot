import argparse
import pandas as pd
from component import compute_cockpit_arr, compute_cabin_arr, compute_after_cabin_arr
from component import compute_propeller_with_normal_position
from helper import draw_aircraft

# load arguments
def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cname', default='drone', type=str)

    args = parser.parse_args()

    return args


# function to create database
def insert_args():
    # setting argument class
    parser = argparse.ArgumentParser()

    # add the arguments
    # case name
    parser.add_argument('--cname', default='drone', type=str)

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

    # propeller
    tp_float = lambda x: list(map(float, x.split('/')))  # to get list which some variables(format type is float) includes
    tp_int = lambda x: list(map(int, x.split('/')))  # to get list which some variables(format type is int) includes
    parser.add_argument('--txs', default='0.2/0.5/0.8', type=tp_float,
                        help='each value is within 0 to 1, and you have to put half of required number of propeller(if you need 6 propellers, you will have to put such command as "0.2/0.5/0.8"')
    parser.add_argument('--angles', default='30/90/150', type=tp_int,
                        help='angle of propeller settings, the number of value is same as the number of txs')
    parser.add_argument('--radius', default=1.0, type=float, help='radius of propeller curve(collection of propellers)')
    parser.add_argument('--pr', default=0.5, type=float, help='radius of each propeller')
    parser.add_argument('--lp', default=0.5, type=float, help='length of arm for connecting both propeller and cabin')
    parser.add_argument('--zdiffp', default=0.4, type=float, help='shift setting point of each propeller')
    parser.add_argument('--k', default=0.3, type=float, help='setting coefficient of arm corresponding to propeller on x axis')

    # propeller arm
    parser.add_argument('--arm_r', default=0.1, type=float, help='radius of arm')

    args = parser.parse_args()

    return args

# Argument class(To manage database parameters)
class Arguments(object):

    def __init__(self, args):

        cname = args.cname

        fname = './AircraftData/{}.csv'.format(cname)

        df = pd.read_csv(fname)
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
        txs = [float(a) for a in df['txs'].values[0].split('/')]
        self.txs = txs
        angles = [int(a) for a in df['angles'].values[0].split('/')]
        self.angles = angles

        self.radius = df['radius'].values[0]
        self.pr = df['pr'].values[0]
        self.lp = df['lp'].values[0]
        self.zdiffp = df['zdiffp'].values[0]
        self.k = df['k'].values[0]
        self.arm_r = df['arm_r'].values[0]


if __name__ == '__main__':

    # variables names
    names = ['huc', 'hlc', 'wc',
             'hlf', 'huf', 'wf',
             'hau', 'wa',
             'l1', 'l2', 'l3',
             'uk',
             'txs', 'angles', 'radius', 'pr', 'lp', 'zdiffp', 'k',
             'arm_r']

    # data type
    mode = 'load'  # 'insert' or 'load'

    if mode == 'insert':
        args = insert_args()

    else:
        l_args = load_args()
        args = Arguments(l_args)

    # cockpit arr
    cockpit_arr = compute_cockpit_arr(args)
    # cabin arr
    cabin_arr = compute_cabin_arr(args)
    # after cabin arr
    after_cabin_arr = compute_after_cabin_arr(args)

    # propeller
    propeller_arr, arm_arr = compute_propeller_with_normal_position(cabin_arr, args)

    # component names
    component_names = ['cockpit', 'cabin', 'after_cabin', 'propeller', 'arm']
    # component_arrays
    component_arrs = [cockpit_arr, cabin_arr, after_cabin_arr, propeller_arr, arm_arr]

    # create component dictionary
    component_dict = {}

    for key, val in zip(component_names, component_arrs):
        component_dict[key] = val

    # draw aircraft
    axis_bounds = [[-2, 8], [-5, 5], [-5, 5]]
    draw_aircraft(component_dict, axis_bounds)

        



