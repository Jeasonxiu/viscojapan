import glob
from os.path import join, exists
from os import makedirs

from pylab import show, savefig, close
import h5py

from viscojapan.plots import MapPlotFault, MapPlotSlab, plt
from viscojapan.fault_model import FaultFileIO

from epochs_log import epochs

bno = 10

for ano in range(20):        
    file = glob.glob('outs/ano_%02d_bno_%02d.h5'%(ano,bno))[0]
    fault_file = '../fault_model/fault_bott40km.h5'

    fid = FaultFileIO(fault_file)
    num_subflts = fid.num_subflt_along_strike*fid.num_subflt_along_dip

    with h5py.File(file) as fid:
        Bm = fid['Bm'][...]

    plot_path = 'plots/ano_%02d/'%ano
    if not exists(plot_path):
        makedirs(plot_path)

    for nth, epoch in enumerate(epochs):    
        print(epoch)
        mplt = MapPlotFault(fault_file)
        mplt.plot_slip(Bm[nth*num_subflts:
                          (nth+1)*num_subflts])
        mplt = MapPlotSlab()
        mplt.plot_top()
        
        savefig(join(plot_path, 'incr_slip_%04d.png'%epoch))
        #plt.show()
        plt.close()
