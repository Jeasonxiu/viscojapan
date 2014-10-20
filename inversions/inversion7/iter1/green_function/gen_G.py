from glob import glob
import argparse

from numpy import inf, log10

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

cmd = {}

def add_task(mod_str, visK, visM, He, rake, model_num):        
    num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))
    model = PollitzOutputsToEpochalData(
        epochs = sorted(epochs),
        G_file = 'G%d_'%model_num + mod_str + '.h5',
        num_subflts = num_subflts,
        pollitz_outputs_dir = 'outs_' + mod_str,
        sites_file = 'stations.in',
        extra_info ={
        'He':He,
        'visM':visM,
        'log10(visM)':log10(visM),
        'visK':visK,
        'log10(visK)':log10(visK),
        'rake':rake
        },
        extra_info_attrs ={
        'He':{'unit':'km'},
        'visM':{'unit':'Pa.s'},
        'visK':{'unit':'Pa.s'},
        },       
        )    
    cmd[model_num] = model

add_task('He50km_VisK5.0E17_VisM1.0E19_Rake90',
         5E17, 1E19, 50, 90., 0)
add_task('He50km_VisK6.0E17_VisM1.0E19_Rake90',
         6E17, 1E19, 50, 90., 1)
add_task('He50km_VisK5.0E17_VisM2.0E19_Rake90',
         5E17, 2E19, 50, 90., 2)
add_task('He50km_VisK5.0E17_VisM1.0E19_Rake90',
         5E17, 1E19, 55, 90., 3)
add_task('He50km_VisK5.0E17_VisM1.0E19_Rake90',
         5E17, 1E19, 50, 80., 4)

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Generate G matrix for indicated model.',
                        )
    args = parser.parse_args()
    model = args.model[0]

    if model == 'all':
        for s,c in cmd.items():
            print(s)
            c()
    else:
        cmd[model]()

