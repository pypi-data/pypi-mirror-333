import unittest
from modlamp.sequences import Centrosymmetric


class TestCentrosymmetric(unittest.TestCase):
    S = Centrosymmetric(1)
    S.generate_sequences(symmetry='symmetric')
    
    def test_block_symmetry(self):
        self.assertEqual(self.S.sequences[0][0], self.S.sequences[0][6])
        self.assertEqual(self.S.sequences[0][1], self.S.sequences[0][5])
        self.assertEqual(self.S.sequences[0][2], self.S.sequences[0][4])
    
    def test_whole_symmetry(self):
        self.assertEqual(self.S.sequences[0][0:6], self.S.sequences[0][7:13])
    
    def test_length(self):
        self.assertIn(len(self.S.sequences[0]), (14, 21))


class TestCentroAsymmetric(unittest.TestCase):
    AS = Centrosymmetric(1)
    AS.generate_sequences(symmetry='asymmetric')
    
    def test_whole_symmetry(self):
        self.assertNotEqual(self.AS.sequences[0][0:6], self.AS.sequences[0][7:13])

if __name__ == '__main__':
    unittest.main()
