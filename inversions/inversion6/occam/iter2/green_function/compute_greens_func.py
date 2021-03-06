import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files_rake85 = \
              sorted(glob.glob('../fault_model/subflts_rake85/flt_????'))

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_rake90/flt_????'))

cmd = {}


def add_task_nongravity(mod_str, rake):
    earth_file_dir = join('../earth_model_nongravity/', mod_str)
    subflts_files = globals()['subflts_files_rake%02d'%rake]
    cmd[mod_str + '_Rake%2d'%rake] = ComputeGreensFunction(
        epochs = epochs,
        file_sites = 'stations.in',
        earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
        earth_file_dir = earth_file_dir,
        outputs_dir = 'outs_'+mod_str+'_Rake%2d'%rake,
        subflts_files = subflts_files,
        controller_file = 'pool.config',
        )

add_task_nongravity('He50km_Vis2.8E19', 90)
add_task_nongravity('He50km_Vis4.0E19', 90)
add_task_nongravity('He45km_Vis2.8E19', 90)
add_task_nongravity('He50km_Vis2.8E19', 85)

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute G matrix.')
    parser.add_argument('model', type=str, nargs='+',
                        help='Compute G matrix for indicated model.',
                        )
    args = parser.parse_args()
    for m in args.model:
        assert m in cmd, '%s is not found.'%m
        
    for m in args.model:
        cmd[m]()
