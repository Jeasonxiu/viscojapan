import pGMT
import tempfile

import numpy as np

import viscojapan as vj

__doc__='''Observed Coseismic disp. This plot models Ozawa 2011.'''

##def gen_codisp_ver_file():
##    reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
##    co_disp = reader[0].reshape([-1,3])
##    sites = vj.Sites([ii.decode() for ii in reader['sites']])
##
##    text = tempfile.NamedTemporaryFile(mode='w+t')
##    _text = '# lon lat ver\n'
##    for ci, site in zip(co_disp, sites):
##        _text += '%f %f %f \n'%\
##                 (site.lon, site.lat, ci[2])
##    text.write(_text)
##    text.seek(0,0)
##    return text
##
##def gen_codisp_ver_mag_file():
##    reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
##    co_disp = reader[0].reshape([-1,3])
##    sites = vj.Sites([ii.decode() for ii in reader['sites']])
##
##    text = tempfile.NamedTemporaryFile(mode='w+t')
##    _text = '# lon lat ver\n'
##    for ci, site in zip(co_disp, sites):
##        _text += '%f %f %f \n'%\
##                 (site.lon, site.lat, np.abs(ci[2]))
##    text.write(_text)
##    text.seek(0,0)
##    return text
##    
##def plot_hor_mag(gplt):
##    text = gen_codisp_ver_mag_file()
##    gmt = pGMT.GMT()
##    gmt.nearneighbor(
##        text.name,
##        G='~ver_mag.grd', I='1k', N='8', R='', S='60k'
##        )
##
##    gmt = pGMT.GMT()
##    gmt.makecpt(C='seminf-haxby.cpt',T='-4/-0.1/0.1',Q='',M='')
##    gmt.save_stdout('~hor_mag.cpt')
##
##    gplt.grdimage(
##        '~ver_mag.grd',
##        J='', R='', C='~hor_mag.cpt',O='',K='', Q='',
##        )
##    text.close()
##    
##    # fill water with white color
##    gplt.pscoast(R='', J='', S='white', O='', K='')


######################################
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
    'verticals_abs',
    cpt_scale='-4/-0.15/0.01')
plt_ver.plot_xyz()
plt_ver.plot_scale(scale_interval='1')
plt_ver.plot_contour(contours = [0.001,0.01,0.1], W='thick')


vj.gmt.plot_plate_boundary(gplt,color='150')

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--',
    W = 'faint,100', L='f145/31/38/200+lkm+jt',
    O = '', K='')

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K=None)

gplt.save('codisp_ver.pdf')
gplt.save_shell_script('shell.sh', output_file=' > out.ps')
