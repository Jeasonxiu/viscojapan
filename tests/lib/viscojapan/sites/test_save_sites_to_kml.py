import unittest
from os.path import join

import viscojapan as vj

class Test_save_sites_to_kml(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_save_sites_to_kml(self):
        sites = ['J550', 'J551', '_FUK']
        sites = vj.sites_db.SitesDB().gets(sites)

        vj.sites.save_sites_to_kml(
            sites,
            fn = join(self.outs_dir, 'sites.kml')
            )


if __name__=='__main__':
    unittest.main()
