#!/usr/bin/env python3
import sys

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.inversion import Inversion
from days import days as epochs

inv = Inversion()

inv.sites_file = 'sites'
inv.file_G1 = '../greensfunction/050km-vis02/G.h5'
inv.file_G2 = '../greensfunction/050km-vis01/G.h5'
inv.f_d = 'cumu_post.h5'
inv.f_slip0 = 'slip0.h5'
inv.epochs = epochs

alpha = 100
inv.init()
inv.invert(alpha)
inv.save_raw('test.pkl')

import pickle
with open('inversion')
pickle.dump()


