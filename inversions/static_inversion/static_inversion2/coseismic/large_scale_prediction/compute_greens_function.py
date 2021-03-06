from os.path import join
import glob

import viscojapan as vj

earth_file_dir = '../../earth_model_nongravity/He63km_VisM1.0E19/'
earth_file = join(earth_file_dir, 'earth.model_He63km_VisM1.0E19')

subflts_files = glob.glob('subflts/flt_????')

cmd = vj.pollitz.ComputeGreensFunction(
    epochs = [0],
    file_sites = 'sites.in',
    earth_file = earth_file,
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs',
    subflts_files = subflts_files,
    controller_file = 'pool.config',)

if __name__ == '__main__':
    cmd()
    
