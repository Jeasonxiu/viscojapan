import glob

import h5py
from pylab import plt
import matplotlib
import numpy as np

import viscojapan as vj

nreses =[]
visMs = []
Hes = []
rakes = []
nroughs = []

files = glob.glob('outs/*')

for file in files:
    with h5py.File(file,'r') as fid:
        nres = fid['misfit/norm_weighted'][...]
        nreses.append(nres)

        m = fid['m'][...]
        visMs.append(m[-3])
        Hes.append(m[-2])
        rakes.append(m[-1])

        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)

xlim = (4,7)
xticks = range(4,7)

plt.subplot(411)    
plt.semilogx(nreses, visMs,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.grid('on')
plt.ylabel('log10(visM/(Pa.s))')

plt.subplot(412)    
plt.semilogx(nreses, 10**(np.asarray(Hes)),'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.grid('on')
plt.ylabel('He/km')

plt.subplot(413)    
plt.semilogx(nreses, rakes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.ylabel('rake')
plt.grid('on')

plt.subplot(414)
vj.plot_L(nreses, nroughs)
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('roughening')
plt.xlabel('Weighted Residual Norm')
plt.grid('on')

plt.savefig('plots/nlin_par_curve.png')
plt.show()
