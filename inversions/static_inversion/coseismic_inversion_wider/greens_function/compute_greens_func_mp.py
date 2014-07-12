import glob

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

subflts_files = \
              sorted(glob.glob('../fault_model/subflts/flt_????'))

com = ComputeGreensFunction(
    epochs = [0],
    file_sites = 'sites_with_seafloor',
    earth_file = '../earth_model_He50km/earth.model_He50km',
    earth_file_dir = '../earth_model_He50km/earth_files/',
    outputs_dir = 'outs',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )
com.run()