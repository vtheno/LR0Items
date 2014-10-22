import cutest as unittest
import re
from LR0Items import LR0Items

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

    def testListOfTuples(self):
        L = [("E", "@E")]
        self.assertEqual(L[0][0], "E")
        self.assertEqual(L[0][1], "@E")

    def testListOfTuplesIteration(self):
        L = [('E', 'E+T'), ('E', 'T'), ('T', 'T*F')]
        M = []
        for item in L:
            M.append(item)
        self.assertEqual(M[0], ('E', 'E+T'))
        self.assertEqual(M[1], ('E', 'T'))
        self.assertEqual(M[2], ('T', 'T*F'))
        self.assertEqual(len(M), 3)

    def testDotBeforeNonTerminalRegex(self):
        regex = re.compile(r'@([A-Z])')
        self.assertTrue(regex.search('aaaaa@E'))
        self.assertEqual(regex.search('aaaa'), None)

    def testDotBeforeNonTerminal(self):
        self.assertEqual(LR0Items.dotBeforeNonTerminal("@FGaaaa"), 'F')
        self.assertEqual(LR0Items.dotBeforeNonTerminal("aaafa_0-=@K"), 'K')
        self.assertEqual(LR0Items.dotBeforeNonTerminal("aaaaaaaa@FGaaaa"), 'F')
        self.assertEqual(LR0Items.dotBeforeNonTerminal("@M"), 'M')
        self.assertEqual(LR0Items.dotBeforeNonTerminal("@+Gaaaa"), False)
        self.assertEqual(LR0Items.dotBeforeNonTerminal("-FGaaaa@b"), False)
        self.assertEqual(LR0Items.dotBeforeNonTerminal("aaaa@aGaaaa"), False)

if __name__ == '__main__':
	unittest.main()
