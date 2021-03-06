import unittest
from os.path import join

import numpy as np

import viscojapan as vj

class Test_PollitzOutputsToEpochalData(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.clean_outs_dir()

    def test(self):
        visM = 1E19
        visK = 5E17
        rake = 90
        sites =  np.loadtxt(join(self.share_dir, 'sites'),'4a', usecols=(0,))
        model = vj.pollitz.PollitzOutputsToEpochalData(
            epochs = [0, 60],
            G_file = join(self.outs_dir, 'G.h5'),
            num_subflts = 10,
            pollitz_outputs_dir = join(self.share_dir, 'pollitz_outs'),
            sites = sites,
            extra_info ={
            'He':50,
            'visM':visM,
            'log10(visM)':np.log10(visM),
            'visK':visK,
            'log10(visK)':np.log10(visK),
            'rake':rake
            },
            extra_info_attrs ={
            'He':{'unit':'km'},
            'visM':{'unit':'Pa.s'},
            'visK':{'unit':'Pa.s'},
            }
            )
        model()
            
if __name__ == '__main__':
    unittest.main()
