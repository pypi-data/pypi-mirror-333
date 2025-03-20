import unittest
from os.path import dirname, join

from modlamp.wetlab import CD


class TestCD(unittest.TestCase):
    cd = CD(join(dirname(__file__), 'files/wetlab'), 180, 260, amide=True)
    
    def test_init(self):
        self.assertIsNotNone(self.cd.filenames)
        self.assertIsInstance(self.cd.filenames[0], str)
    
    def test_read_header(self):
        self.assertEqual(self.cd.sequences[1], 'GLFDIVKKVLKLLK')
        self.assertEqual(self.cd.sequences[0], 'GLFDIVKKVLKLLK')
        self.assertEqual(self.cd.conc_umol[1], 33.)
        self.assertAlmostEqual(self.cd.conc_mgml[1], 0.05323197, 5)
        self.assertAlmostEqual(self.cd.meanres_mw[1], 124.08384615, 4)

    # commented out because test don't work on travis
    # def test_molar_ellipticity(self):
    #     self.cd.calc_molar_ellipticity()
    #     self.assertAlmostEqual(self.cd.molar_ellipticity[1][0, 1], -1172.7787878787878, 5)
    
    # def test_meanres_ellipticity(self):
    #     self.cd.calc_meanres_ellipticity()
    #     self.assertAlmostEqual(self.cd.meanres_ellipticity[1][38, 1], -1990.3473193473196, 5)
    
    # def test_helicity(self):
    #     self.cd.calc_meanres_ellipticity()
    #     self.cd.helicity()
    #     self.assertEqual(float(self.cd.helicity_values.iloc[0]['Helicity']), 79.68)

    # def test_plot(self):
    #     self.cd.plot()


if __name__ == '__main__':
    unittest.main()
