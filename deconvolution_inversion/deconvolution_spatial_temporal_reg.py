from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists

from epochs_even import epochs as epochs_even


project_path = '/home/zy/workspace/viscojapan/'

dtest = DeconvolutionTestFromFakeObs()
dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_fake_d = 'simulated_disp.h5'
dtest.sites_filter_file = 'sites'
dtest.epochs = epochs_even

dtest.init()
dtest.load_data()

alphas = logspace(-4,2,20)
betas = logspace(-4,2,20)

for ano, alpha in enumerate(alphas):
    for bno, beta in enumerate(betas):
        dtest.invert(alpha, beta)
        dtest.res_writer.save_results('outs_alpha_beta/res_%02d.h5'%ano)
        dtest.res_writer.save_results_incr_slip('outs_alpha_beta/incr_slip_%02d.h5'%ano)
        dtest.res_writer.save_results_slip('outs_alpha_beta/slip_%02d.h5'%ano)
        dtest.res_writer.save_results_pred_disp('outs_alpha_beta/pred_disp_%02d.h5'%ano)
