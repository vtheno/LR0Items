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
        starting_productions.close()
        self.symbols = self.createListOfSymbols()

    def createListOfSymbols(self):
        symbols = []
        for prod in self.aug_productions:
            for char in prod[1]:
                if char != '@' and char != "'" and char not in symbols:
                    symbols.append(char)
        return symbols

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

    def goto(self, set_of_items, symbol):
        goto_result = []
        for item in set_of_items:
            if ("@%s" % symbol) in item[1]:
                new_RHS = item[1].replace("@%s" % symbol, "%s@" % symbol)
                goto_result.extend(self.closure(item[0], new_RHS))
        return goto_result

    def items(self):
        C = []
        C.append(self.closure("'", "@E"))
        added = True
        while(added):
            added = False
            for items in C:
                for symbol in self.symbols:
                    goto_result = self.goto(items, symbol)
                    if goto_result and goto_result not in C:
                        C.append(goto_result)
                        added = True
        return C

lr0Items = LR0Items()
lr0Items.printAugmentedGrammar()
print("\nSets of LR(0) Items\n-------------------")
output = lr0Items.items()

def printOutput(data):
    for set_of_items in range(len(data)):
        print("I%s:" % set_of_items)
        for item in data[set_of_items]:
            print("    %s->%s" % (item[0], item[1]) + '{:>20}'.format('goto(stuff)'))
           
            

printOutput(output)
