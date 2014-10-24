import cutest as unittest
import re
from LR0Items import LR0Items

class TestLR0Items(unittest.TestCase):

    
        
    def testProductionsProperlyInitialized(self):
        lr0Items = LR0Items("input.txt")
        self.assertEqual(lr0Items.aug_productions[1][1], 'E+T')
        self.assertEqual(len(lr0Items.aug_productions), 7)

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
        lr0Items = LR0Items("input.txt")
        self.assertEqual(lr0Items.dotBeforeNonTerminal("@FGaaaa"), 'F')
        self.assertEqual(lr0Items.dotBeforeNonTerminal("aaafa_0-=@K"), 'K')
        self.assertEqual(lr0Items.dotBeforeNonTerminal("aaaaaaaa@FGaaaa"), 'F')
        self.assertEqual(lr0Items.dotBeforeNonTerminal("@M"), 'M')
        self.assertEqual(lr0Items.dotBeforeNonTerminal("@+Gaaaa"), False)
        self.assertEqual(lr0Items.dotBeforeNonTerminal("-FGaaaa@b"), False)
        self.assertEqual(lr0Items.dotBeforeNonTerminal("aaaa@aGaaaa"), False)

    def testClosure(self):
        lr0Items = LR0Items("input.txt")
        closure_result = lr0Items.closure("'", "@E")
        self.assertEqual(closure_result[0], ("'", "@E"))
        self.assertEqual(closure_result[1], ("E", "@E+T"))
        self.assertEqual(closure_result[2], ("E", "@T"))
        self.assertEqual(closure_result[3], ("T", "@T*F"))
        self.assertEqual(closure_result[4], ("T", "@F"))
        self.assertEqual(closure_result[5], ("F", "@(E)"))
        self.assertEqual(closure_result[6], ("F", "@i"))
        

if __name__ == '__main__':
	unittest.main()
