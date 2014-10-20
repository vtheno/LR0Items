import cutest as unittest
import re
import LR0Items

class TestLR0Items(unittest.TestCase):

    def setUp(self):
        self.aug_productions = [
            ("'", '->E'), 
            ('E', 'E+T'), 
            ('E', 'T'), 
            ('T', 'T*F'), 
            ('T', 'F'), 
            ('F', '(E)'), 
            ('F', 'i')
        ]
    def testProductionsProperlyInitialized(self):
        self.assertEqual(self.aug_productions[1][1], 'E+T')
        self.assertEqual(len(self.aug_productions), 7)

if __name__ == '__main__':
	unittest.main()
