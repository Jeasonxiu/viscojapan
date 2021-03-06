import pGMT
import tempfile

import numpy as np

import viscojapan as vj

infile = '../pred_vertical'
outfile = 'codisp_ver.pdf'
cpt_scale = '-4/-0.15/0.01'
if_log_color_scale = False
contours = [-0.6, -0.1, 0, 0.01]

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'COLOR_NAN','white',
           'COLOR_BACKGROUND','white',
           'COLOR_FOREGROUND','white'
           )

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '128/148/30/46',       # region
    J = 'B138/38/30/46/16c', # projection
    B = '4',
    U='20/0/25/Yang', P='', K=''
    )

plt_ver = vj.gmt.GMTXYZ(
    gplt,
    infile,
    cpt_scale = cpt_scale,
    if_log_color_scale = if_log_color_scale,
    )
plt_ver.cpt_file = 'vertical_disp.cpt'
plt_ver.plot_xyz()
plt_ver.plot_scale(scale_interval='0.2')
plt_ver.plot_contour(contours = contours, W='thick')

vj.gmt.plot_plate_boundary(gplt,color='150')

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--',
    W = 'faint,100', L='f145/31/38/200+lkm+jt',
    O = '', K='')

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K=None)

gplt.save(outfile)
gplt.save_shell_script('shell.sh', output_file=' > out.ps')

