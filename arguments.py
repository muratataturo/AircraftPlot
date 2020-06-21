import pandas as pd


# Normal Type Argument class(To manage database parameters)
class NormalArguments(object):

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


# Drone Type Argument class
class DroneArguments(object):

    def __init__(self, args):
        cname = args.cname
        fname = './AircraftData/{}.csv'.format(cname)

        df = pd.read_csv(fname)
        self.aircraft_type = args.aircraft_type
        self.engine_type = args.engine_type
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
