import h5py
from pylab import plt
import matplotlib
from numpy import arange

import viscojapan as vj

nreses =[]
visMs = []
Hes = []
rakes = []
nroughs = []

for ano in range(20):
    with h5py.File('outs/ano_%02d_bno_00.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)

        m = fid['m'][...]
        visMs.append(m[-3])
        Hes.append(m[-2])
        rakes.append(m[-1])

        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)

xlim = [560.4, 561.2]
xticks = arange(560.4,561,0.1)
plt.subplot(411)    
plt.semilogx(nreses, visMs,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.grid('on')
plt.ylabel('log10(visM/(Pa.s))')

plt.subplot(412)    
plt.semilogx(nreses, Hes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.grid('on')
plt.ylabel('He/km')

plt.subplot(413)    
plt.semilogx(nreses, rakes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('rake')
plt.grid('on')

plt.subplot(414)
vj.plot_L(nreses, nroughs)
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('roughening')
plt.xlabel('Residual Norm')
plt.grid('on')


plt.show()