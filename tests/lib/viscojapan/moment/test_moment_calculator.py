import unittest

import viscojapan as vj

__author__ = 'zy'


class TestMomentCalculator(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_MomentCalculator(self):
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5'

        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip()

        earth_file = '/home/zy/workspace/viscojapan/tests/share/earth.model_He50km_VisM6.3E18'

        cal = vj.moment.MomentCalculator(fault_file, earth_file)

        cal.get_cumu_slip_Mos_Mws(slip)

        mos, mws = cal.get_afterslip_Mos_Mws(slip)
        print(mos, mws)


if __name__ == '__main__':
    unittest.main()
