import numpy as np

import viscojapan as vj

def load_lons_lats():
    tp = np.loadtxt('../stations_large_scale.in', '4a,f,f')
    lons = [ii[1] for ii in tp]
    lats = [ii[2] for ii in tp]
    return lons, lats

lons, lats = load_lons_lats()

epochs = range(0,1344,20)

reader = vj.inv.DeformPartitionResultReader(
    '../../deformation_partition_large_scale.h5')

Ecumu = reader.Ecumu


contours = [0.1, 0.5, 1,5,9,20]

cmpt = 'Raslip'

obj = getattr(reader, cmpt)
for epoch in epochs:
    print(cmpt, epoch)
    if epoch == 0:
        continue
    mags = obj.get_velocity_hor_mag_at_epoch(epoch)
    mags = mags*100*365 # m/day => cm/yr
        
    plt = vj.displacement.plot.MagnitudeContoursPlotter()
    plt.plot(lons, lats, mags,
             'plots/%s_day%04d.pdf'%(cmpt,epoch),
             contours = contours,
             if_topo = False,
             unit_label = 'cm/yr'
             )
