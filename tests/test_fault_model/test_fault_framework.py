import unittest
from os.path import join
import warnings

from numpy import arange
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault_model.fault_framework import FaultFramework
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class TestFaultFramework(unittest.TestCase):
    def setUp(self):
        self.fm = FaultFramework()

    def test_Y_GC_vs_DEP(self):
        plt.plot(self.fm.Y_GC, self.fm.DEP, '-o')
        plt.axis('equal')
        plt.axhline(0, color='black')
        plt.gca().set_yticks(self.fm.DEP)
        plt.gca().set_xticks(self.fm.Y_GC)
        plt.grid('on')
        plt.title('Ground x versus depth')
        plt.xlabel('Ground X (km)')
        plt.ylabel('depth (km)')

        for xi, yi, dip in zip(self.fm.Y_GC, self.fm.DEP, self.fm.DIP_D):
            plt.text(xi, yi, 'dip = %.1f'%dip)

        plt.gca().invert_yaxis()
        
        plt.savefig(join(this_test_path,'~dep_Y_GC.png'))
        plt.close()

    def test_dip(self):
        xf = arange(0, 425)
        dips = self.fm.get_dip(xf)
        plt.plot(xf,dips)
        plt.grid('on')
        plt.gca().set_xticks(self.fm.Y_GC)
        plt.ylim([0, 30])
        plt.gca().invert_yaxis()
        plt.savefig(join(this_test_path, '~y_fc_dips.png'))
        plt.close()

    def test_dep(self):
        xf = arange(0, 425)
        deps = self.fm.get_dep(xf)
        plt.plot(xf,deps)

        plt.gca().set_yticks(self.fm.DEP)
        plt.gca().set_xticks(self.fm.Y_GC)
        
        plt.grid('on')
        plt.title('Ground x versus depth')
        plt.xlabel('Ground X (km)')
        plt.ylabel('depth (km)')
        plt.axis('equal')
        plt.gca().invert_yaxis()
        plt.savefig(join(this_test_path, '~Y_GC_vs_deps.png'))
        plt.close()

    def test_yfc_to_ygc(self):
        self.assertRaises(AssertionError,
                          self.fm.yfc_to_ygc, [500])
        self.assertRaises(AssertionError,
                          self.fm.yfc_to_ygc, [-0.1])
        xf = arange(0, 425)
        xg = self.fm.yfc_to_ygc(xf)

    def test_ygc_to_yfc(self):
        self.assertRaises(AssertionError,
                          self.fm.ygc_to_yfc, [500])
        self.assertRaises(AssertionError,
                          self.fm.ygc_to_yfc, [-0.1])
        xg = arange(0, 393)
        xf = self.fm.ygc_to_yfc(xg)

    def test_ygc_yfc_conversion(self):
        xf = arange(0, 425)
        xg = self.fm.yfc_to_ygc(xf)
        xf1 = self.fm.ygc_to_yfc(xg)

        assert_almost_equal(xf, xf1)

    def test_get_yfc_by_dep_scalar(self):
        for nth, dep in enumerate(self.fm.DEP):
            xf = self.fm.get_yfc_by_dep_scalar(dep)
            assert_almost_equal(xf, self.fm.Y_FC[nth])


if __name__ == '__main__':
    unittest.main()
