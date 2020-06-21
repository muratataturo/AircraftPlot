import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# for normal aircraft
from component import compute_cockpit_arr, compute_cabin_arr, compute_after_cabin_arr
from component import compute_main_wing_arr, compute_horizontal_wing, compute_vertical_wing
from component import compute_engine_lower_main_wing, compute_engine_upper_main_wing, compute_engine_upper_cabin
from arguments import NormalArguments
# for drone
from component import compute_propeller_with_normal_position
from arguments import DroneArguments


# load arguments
def load_args():
    parser = argparse.ArgumentParser()

    ## normal case
    parser.add_argument('--cname', default='a320', type=str)
    parser.add_argument('--aircraft_type', default='normal', type=str,
                        help='1. normal, 2. drone, 3. blended wing body, 4. hyper sonic, 5. propeller')
    parser.add_argument('--engine_type', default='turbofan', type=str,
                        help='1. turbofan 2. propeller 3. distributed fan(turbofan + electric fan)')

    """
    ## drone case
    parser.add_argument('--cname', default='drone', type=str)
    parser.add_argument('--aircraft_type', default='drone', type=str,
                        help='1. normal, 2. drone, 3. blended wing body, 4. hyper sonic, 5. propeller')
    parser.add_argument('--engine_type', default='propeller', type=str, help='1. turbofan 2. propeller')
    """

    ## distributed fan case
    parser.add_argument('--cname', default='a320', type=str)
    parser.add_argument('--aircraft_type', default='normal', type=str,
                        help='1. normal, 2. drone, 3. blended wing body, 4. hyper sonic, 5. propeller')
    parser.add_argument('--engine_type', default='distributed fan', type=str,
                        help='1. turbofan 2. propeller 3. distributed fan(turbofan + electric fan)')

    args = parser.parse_args()


    return args


class AircraftView(object):

    def __init__(self, arg_class):

        self.arg_class = arg_class

        self.component_names = self.pull_component_names()
        if self.component_names is not None:
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
            self.propeller_arr, self.arm_arr = self.set_propeller()

            self.component_geometry = [self.cockpit_arr, self.cabin_arr, self.after_cabin_arr, self.main_wing_arr,
                                       self.hori_wing_arr, self.vert_wing_arr, self.engine_arr, self.propeller_arr,
                                       self.arm_arr]
        else:
            self.component_geometry = []

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
            component_names = ['cockpit', 'cabin', 'after_cabin', 'propeller', 'arm']

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

    def set_propeller(self):
        if 'propeller' not in self.component_names:

            return None, None

        return compute_propeller_with_normal_position(self.arg_class, self.cabin_arr)


if __name__ == '__main__':
    l_args = load_args()
    if l_args.aircraft_type == 'normal':
        args = NormalArguments(l_args)
    elif l_args.aircraft_type == 'drone':
        args = DroneArguments(l_args)
    else:
        args = None

    if args is not None:
        # create viewer class
        av = AircraftView(args)

        # change bounds area according to aircraft and engine type
        if args.aircraft_type == 'normal':
            bounds = [[-10, 40], [-20, 20], [-15, 15]]  # normal case
        elif args.aircraft_type == 'drone':
            bounds = [[-2, 8], [-5, 5], [-5, 5]]  # drone case
        else:
            bounds = [[-10, 40], [-20, 20], [-15, 15]]

        av.view_all(bounds=bounds)

        av.view_unit(name='cabin', bounds=bounds)






