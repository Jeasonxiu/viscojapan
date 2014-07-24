from viscojapan.pollitz import gen_subflts_input_for_pollitz

gen_subflts_input_for_pollitz(
    fault_file = 'fault_bottom_limit_50km.h5',
    out_dir = 'subflts_rake90',
    rake = 90.)

gen_subflts_input_for_pollitz(
    fault_file = 'fault_bottom_limit_50km.h5',
    out_dir = 'subflts_rake95',
    rake = 95.)

gen_subflts_input_for_pollitz(
    fault_file = 'fault_bottom_limit_33km.h5',
    out_dir = 'subflts_rake95',
    rake = 95.)
