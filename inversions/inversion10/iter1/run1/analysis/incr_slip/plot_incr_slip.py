from os.path import basename, splitext, join, exists
import glob

import viscojapan as vj

files = glob.glob('../../outs/nco_06_naslip_10.h5')

for file in files:
    fn, _ = splitext(basename(file))
    output_file = join('plots/', fn+'.pdf',)
    print(output_file)
##    if exists(output_file):
##        continue
    plt = vj.gmt.PlotSlipResult(
        fault_file = '../../../fault_model/fault_bott80km.h5',
        result_file = file,
        subplot_width = 3.2,
        subplot_height = 5.2,
        num_plots_per_row = 5,
        earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18',
        color_label_interval_aslip = .3,
        max_aslip = 1.,
        )
    
    plt.plot(output_file)
    plt.clean()
