from numpy import logspace
import numpy as np

from os.path import exists
import sys

import viscojapan as vj

from epochs import epochs

reg_roughes = logspace(-3,1,20)

fault_file = '../fault_model/fault_bott80km.h5'

#epochs = epochs[0:3]
num_epochs = len(epochs)

basis = vj.inv.basis.BasisMatrixBSpline.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = vj.inv.OccamDeconvolution(
    file_G0 = '../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    files_Gs = ['../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                '../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','log10(He)','rake'],

    file_d = '../obs/cumu_post_with_seafloor.h5',
    file_sd = '../sd/sd_uniform.h5', 
    file_incr_slip0 = 'slip0/v1/slip0.h5',
    filter_sites_file = 'sites_Yamagiwa',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )

inv.set_data_except(excepts=['L'])

outfname = 'outs/result_no_reg.h5'%(nrough, naslip)
print(outfname)
inv.regularization = \
       reg = vj.inv.reg.create_rough_aslip_boundary_regularization(
           fault_file, num_epochs,
           0.,
           0.,
           0.)

inv.set_data_L()
inv.run()
inv.save(outfname, overwrite=True)

        
                
