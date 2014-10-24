import unittest
import re
from LR0Items import LR0Items

class TestLR0Items(unittest.TestCase):

    def setUp(self):
        starting_productions = open("input.txt")
        self.lr0Items = LR0Items(starting_productions)
        
    def testProductionsProperlyInitialized(self):
        self.assertEqual(self.lr0Items.aug_productions[1][1], 'E+T')
        self.assertEqual(len(self.lr0Items.aug_productions), 7)

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

    def tearDown(self):
        close(input)

if __name__ == '__main__':
	unittest.main()
