import glob
from os.path import basename, exists
import re
from multiprocessing import Pool
import argparse

import h5py

from viscojapan.plots import MapPlotFault, plt, MapPlotSlab
import viscojapan as vj


files = sorted(glob.glob('outs/rough_??.h5'))

sites_seafloor = vj.get_sites_seafloor()

fault_file = '../../fault_model/fault_bott60km.h5'
earth_file = '../../earth_model_nongravity/He63km_VisM1.0E19/earth.model_He63km_VisM1.0E19'

def plot_file(file):
    name = basename(file)
    #fname = 'plots/%s.pdf'%name
    fname = 'plots/%s.png'%name
    if exists(fname):
        print('Skip %s!'%fname)
        return
    print(fname)
    with h5py.File(file,'r') as fid:
        slip = nres = fid['Bm'][...]

    mplt = MapPlotSlab()
    mplt.plot_top()
    
    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(slip)

    mplt = vj.plots.MapPlotDisplacement()
    mplt.plot_sites_seafloor(sites_seafloor = sites_seafloor)

    mo, mw = vj.ComputeMoment(fault_file, earth_file).moment(slip)
    plt.title('Mo=%g, Mw=%.2f'%(mo, mw))
    #plt.show()
    plt.savefig(fname)

    

    plt.close()

for file in files:
    plot_file(file)

    
