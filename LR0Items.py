# Chris Hogan
# EECS 665
# Project 2
# 3 November 2014

import re
import sys

class LR0Items:

    def __init__(self):
        self.productions = [x.strip() for x in sys.stdin]
        self.aug_productions = [("'", "%s" % self.productions[0])]
        regex = re.compile(r'([A-Z])->(.*)')
        for p in self.productions[1:]:
            m = regex.match(p)
            self.aug_productions.append((m.group(1), m.group(2)))

    def printAugmentedGrammar(self):
        print("\nAugmented Grammar\n-----------------")
        for tup in self.aug_productions:
            print("%s->%s" % (tup[0], tup[1]))


x = LR0Items()
x.printAugmentedGrammar()
print("\nSets of LR(0) Items\n-------------------")