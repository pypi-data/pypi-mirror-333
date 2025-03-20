import unittest
from os.path import dirname, join
import numpy as np
from modlamp.descriptors import PeptideDescriptor

__author__ = 'modlab'


class TestPeptideDescriptor(unittest.TestCase):
    D = PeptideDescriptor('GLFDIVKKVVGALG', 'pepcats')
    A = PeptideDescriptor('GLFDIVKKVVGALG', 'peparc')
    P = PeptideDescriptor('GLFDIVKKVVGALG', 'eisenberg')
    data_ac = np.array(
        [0.714285714286, 0.0714285714286, 0.0714285714286, 0.142857142857, 0.142857142857, 0.0714285714286,
         0.538461538462, 0.0, 0.0, 0.0769230769231, 0.0769230769231, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.636363636364,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.555555555556, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0,
         0.0, 0.0, 0.0])
    data_cc = np.array([0.714285714286, 0.538461538462, 0.5, 0.636363636364, 0.6, 0.555555555556, 0.5, 0.0714285714286,
                        0.0769230769231, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0769230769231, 0.0833333333333, 0.0, 0.0, 0.0,
                        0.0, 0.142857142857, 0.153846153846, 0.166666666667, 0.0909090909091, 0.1, 0.222222222222,
                        0.125, 0.142857142857, 0.153846153846, 0.166666666667, 0.0909090909091, 0.1, 0.222222222222,
                        0.125, 0.0, 0.0769230769231, 0.0833333333333, 0.0, 0.0, 0.0, 0.0, 0.0714285714286, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0769230769231, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1,
                        0.111111111111, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.111111111111, 0.0, 0.0, 0.0769230769231, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0714285714286, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0909090909091, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0909090909091, 0.1, 0.0, 0.0, 0.0714285714286,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.142857142857, 0.0769230769231, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.142857142857, 0.0769230769231, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.142857142857, 0.0769230769231, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0714285714286, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    data_aa = np.array(
        [0.07142857, 0., 0.07142857, 0., 0.07142857, 0.21428571, 0., 0.07142857, 0.14285714, 0.14285714, 0., 0., 0., 0.,
         0., 0., 0., 0.21428571, 0., 0.])
    data_arc = [200, 60, 30, 30, 0]
    E = PeptideDescriptor('X', 'eisenberg')
    E.read_fasta(join(dirname(__file__), 'files/test.fasta'))
    data_mom = np.array([])
    data_glob = np.array([])

    def test_filereader(self):
        self.assertEqual(self.D.sequences[0], self.E.sequences[0])

    def test_autocorr_size(self):
        self.D.calculate_autocorr(7)
        self.assertEqual(len(self.D.descriptor[0]), 42)

    def test_crosscorr_size(self):
        self.D.calculate_crosscorr(7)
        self.assertEqual(len(self.D.descriptor[0]), 147)

    def test_autocorr_values(self):
        self.D.calculate_autocorr(7)
        for n in range(len(self.D.descriptor[0])):
            self.assertAlmostEqual(self.D.descriptor[0, n], self.data_ac[n], places=8)

    def test_crosscorr_values(self):
        self.D.calculate_crosscorr(7)
        for n in range(len(self.D.descriptor[0])):
            self.assertAlmostEqual(self.D.descriptor[0][n], self.data_cc[n], places=8)

    def test_global_value(self):
        self.D.calculate_global()
        self.assertAlmostEqual(self.D.descriptor[0, 0], 1.21428571)
        self.E.calculate_global()
        self.assertAlmostEqual(self.E.descriptor[0, 0], 0.44714285714285723, places=8)

    def test_moment_value(self):
        self.E.calculate_moment()
        self.assertAlmostEqual(self.E.descriptor[0, 0], 0.49723753135551985, places=8)

    def test_profile(self):
        self.P.calculate_profile()
        self.assertAlmostEqual(self.P.descriptor[0, 1], 0.8665096381516001, places=8)

    def test_count_aa(self):
        self.D.count_aa()
        for n in range(len(self.D.descriptor[0])):
            self.assertAlmostEqual(list(self.D.descriptor[0])[n], self.data_aa[n], places=8)

    def test_arc_size(self):
        self.A.calculate_arc()
        self.assertEqual(self.A.descriptor.tolist()[0], self.data_arc)


if __name__ == '__main__':
    unittest.main()
