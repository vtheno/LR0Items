# Chris Hogan
# EECS 665
# Project 2
# 3 November 2014

import re
import sys

class LR0Items:

    def __init__(self, fileName=False):
        starting_productions = sys.stdin
        if fileName:
            starting_productions = open(fileName)
        self.productions = [x.strip() for x in starting_productions]
        self.aug_productions = [("'", "%s" % self.productions[0])]
        regex = re.compile(r'([A-Z])->(.*)')
        for p in self.productions[1:]:
            m = regex.match(p)
            self.aug_productions.append((m.group(1), m.group(2)))

    def printAugmentedGrammar(self):
        print("\nAugmented Grammar\n-----------------")
        for tup in self.aug_productions:
            print("%s->%s" % (tup[0], tup[1]))

    def dotBeforeNonTerminal(self, RHS):
        regex = re.compile(r'@([A-Z])')
        result = regex.search(RHS)
        return False if not result else result.group(1).strip('@')

    def closure(self, LHS, RHS):
        J = [(LHS, RHS)]
        done = []
        added = True
        while(added):
            added = False
            for item in J:
                nextClosureChar = self.dotBeforeNonTerminal(item[1])
                if nextClosureChar and nextClosureChar not in done:
                    done.append(nextClosureChar)
                    for prod in self.aug_productions[1:]:
                        if prod[0] == nextClosureChar:
                            newProd = (prod[0], "@%s" % prod[1])
                            J.append(newProd)
                            added = True
        return J

    def items(self):
        C = self.closure("'", "@E")
        print(C)

lr0Items = LR0Items()
lr0Items.printAugmentedGrammar()
print("\nSets of LR(0) Items\n-------------------")
print(lr0Items.items())
