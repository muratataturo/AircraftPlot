import argparse
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from component import compute_cockpit_arr, compute_cabin_arr, compute_after_cabin_arr
from component import compute_main_wing_arr, compute_horizontal_wing, compute_vertical_wing
from component import compute_engine_lower_main_wing, compute_engine_upper_main_wing, compute_engine_upper_cabin


# load arguments
def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cname', default='a320', type=str)

    args = parser.parse_args()

    return args

# function to create database
def insert_args():
    # setting argument class
    parser = argparse.ArgumentParser()

    # add the arguments
    # case name
    parser.add_argument('--cname', default='a320', type=str)
    # aircraft type
    parser.add_argument('--aircraft_type', default='normal', type=str, help='1. normal, 2. drone, 3. distributed fan, 4. blended wing body, 5. hyper sonic, 6. propeller')
    parser.add_argument('--engine_type', default='turbofan', type=str, help='1. turbofan')
    # engine settings
    parser.add_argument('--engine_settings', default='lower_mainwing', type=str, help='1.lower_mainwing, 2.upper_mainwing, 3. upper_cabin')
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
    parser.add_argument('--rein', default=0.8, type=float, help='radius of inlet core engine [m]')
    parser.add_argument('--reout', default=0.4, type=float, help='radius of outlet core engine [m]')
    parser.add_argument('--tein', default=0.1, type=float, help='margin for joint engine to wing [m]')
    parser.add_argument('--le', default=4.0, type=float, help='core engine length [m]')
    parser.add_argument('--tcx', default=0.4, type=float, help='x chord constant for joint engine')
    parser.add_argument('--tcy', default=0.4, type=float, help='y chord constant for joint engine')
    parser.add_argument('--tcz', default=0.4, type=float, help='z chord constant for joint engine')
    # add option (upper fuselage)
    parser.add_argument('--thetae', default=30, type=float, help='turnover angle for setting engine')

    args = parser.parse_args()

    return args


# Argument class(To manage database parameters)
class Arguments(object):

    def __init__(self, args):

        cname = args.cname

        fname = './AircraftData/{}.csv'.format(cname)

        df = pd.read_csv(fname, index_col=0)
        self.aircraft_type = df['aircraft_type'].values[0]
        self.engine_type = df['engine_type'].values[0]
        self.engine_settings = df['engine_settings'].values[0]
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


class AircraftView(object):

    def __init__(self, arg_class):

        self.arg_class = arg_class

        self.component_names = self.pull_component_names()
        self.component_name_idx_dict = {}
        for idx, name in enumerate(self.component_names):
            self.component_name_idx_dict[name] = idx

        # set component geometry
        self.cockpit_arr = self.set_cockpit_arr()
        self.cabin_arr = self.set_cabin_arr()
        self.after_cabin_arr = self.set_after_cabin()
        self.main_wing_arr = self.set_main_wing()
        self.hori_wing_arr = self.set_hori_wing()
        self.vert_wing_arr = self.set_vert_wing()
        self.engine_arr = self.set_engine()

        self.component_geometry = [self.cockpit_arr, self.cabin_arr, self.after_cabin_arr, self.main_wing_arr,
                                   self.hori_wing_arr, self.vert_wing_arr, self.engine_arr]

    def view_unit(self, name, bounds):

        fig = plt.figure()
        ax = Axes3D(fig)

        target_arr = self.component_geometry[self.component_name_idx_dict[name]]

        ax.scatter(target_arr[:, 0], target_arr[:, 1], target_arr[:, 2])

        ax.set_title('{} view'.format(name))

        ax.set_xlim(bounds[0])
        ax.set_ylim(bounds[1])
        ax.set_zlim(bounds[2])

        plt.show()

    def view_all(self, bounds):

        fig = plt.figure()
        ax = Axes3D(fig)

        for target_arr in self.component_geometry:
            if target_arr is not None:
                ax.scatter(target_arr[:, 0], target_arr[:, 1], target_arr[:, 2])

        ax.set_title('total view')

        ax.set_xlim(bounds[0])
        ax.set_ylim(bounds[1])
        ax.set_zlim(bounds[2])

        plt.show()

    def pull_component_names(self):

        component_names = None

        # aircraft type => 1. normal, 2. drone, 3. distributed fan, 4. blended wing body, 5. hyper sonic, 6. propeller
        if self.arg_class.aircraft_type == 'normal':
            component_names = ['cockpit', 'cabin', 'after_cabin', 'main_wing', 'hori_wing', 'vert_wing', 'engine']
        elif self.arg_class.aircraft_type == 'drone':
            component_names = ['cockpit', 'cabin', 'after_cabin', 'propeller', ]

        return component_names

    def set_cockpit_arr(self):

        if 'cockpit' not in self.component_names:

            return None

        return compute_cockpit_arr(self.arg_class)

    def set_cabin_arr(self):

        if 'cabin' not in self.component_names:
            return None

        return compute_cabin_arr(self.arg_class)

    def set_after_cabin(self):

        if 'after_cabin' not in self.component_names:

            return None

        return compute_after_cabin_arr(self.arg_class)

    def set_main_wing(self):

        if 'main_wing' not in self.component_names:

            return None

        return compute_main_wing_arr(self.arg_class)

    def set_hori_wing(self):

        if 'hori_wing' not in self.component_names:

            return None

        return compute_horizontal_wing(self.arg_class)

    def set_vert_wing(self):

        if 'vert_wing' not in self.component_names:

            return None

        return compute_vertical_wing(self.arg_class)

    def set_engine(self):

        if 'engine' not in self.component_names:

            return None

        engine_settings = self.arg_class.engine_settings

        if engine_settings == 'lower_main_wing':

            return compute_engine_lower_main_wing(self.arg_class, self.main_wing_arr)

        elif engine_settings == 'upper_main_wing':

            return compute_engine_upper_main_wing(self.arg_class, self.main_wing_arr)

        elif engine_settings == 'upper_cabin':

            return compute_engine_upper_cabin(self.arg_class, self.cabin_arr)


if __name__ == '__main__':
    mode = 'load'

    if mode == 'insert':
        args = insert_args()

    else:
        l_args = load_args()
        args = Arguments(l_args)

    av = AircraftView(args)

    # change bounds area according to aircraft and engine type
    bounds = [[-10, 40], [-20, 20], [-15, 15]]

    av.view_all(bounds=bounds)

    av.view_unit(name='main_wing', bounds=bounds)






