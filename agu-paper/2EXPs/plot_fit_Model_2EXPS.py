import pickle

import numpy as np
from pylab import plt
from matplotlib import gridspec

import viscojapan as vj
from viscojapan.tsana.post_fit.post import fit_post

site = 'J550'
cmpt = 'e'
ylim1 = (-0.1, 1)
ylim2 = (-0.06, 0.06)


tsplt = vj.plots.TimeSeriesAndResidualPlotter()

with open('%s_2EXPs.pkl'%site, 'rb') as fid:
    cfs = pickle.load(fid)
cf = cfs[0]
f1 = cf.get_subf('EXP1')
f2 = cf.get_subf('EXP2')

days = np.arange(0, 1344) + 55631
y1 = f1(days)
y2 = f2(days)

ch = cf.data.t > 55631
t_obs = cf.data.t[ch]
y_obs = cf.data.y0[ch] - cf.func.get_subf('TOHOKU').jump

tsplt.plot_on_time_series_axis(t_obs + vj.adjust_mjd_for_plot_date,
              y_obs, '.', color='blue', label='obs.')
tsplt.plot_on_time_series_axis(days + vj.adjust_mjd_for_plot_date,
              y1+y2, '-', lw=2,
              color='red', label='EXP1 + EXP2')
tsplt.plot_on_time_series_axis(days + vj.adjust_mjd_for_plot_date, y1, '-', color=r'green',
              label = 'EXP1')
tsplt.plot_on_time_series_axis(days  + vj.adjust_mjd_for_plot_date, y2, '-', color=r'orange',
              label = 'EXP2')

tsplt.plot_on_residual_axis(cf.data.t[ch] + vj.adjust_mjd_for_plot_date, cf.residual()[ch], '.',
              color=r'blue',
              label = 'residual',
              markersize=1)
tsplt.legend()

plt.savefig('Model_2EXPs_%s-%s.png'%(site, cmpt))
plt.savefig('Model_2EXPs_%s-%s.pdf'%(site, cmpt))
plt.show()
