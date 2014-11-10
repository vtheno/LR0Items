# Chris Hogan
# EECS 665
# Project 2
# 3 November 2014

import re
import sys

class LR0Items:

    #Reads the input from stdin, or a file if a fileName is specified.
    #Creates a list of productions as tuples, e.g. [("'",'E'),('E','B'),('B','b')]
    #Also creates a list of all symbols in the grammar.
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

    #Returns a list of symbols in the grammar, e.g. ['E','B','a']
    def createListOfSymbols(self):
        symbols = []
        for prod in self.aug_productions:
            for char in prod[1]:
                if char != '@' and char != "'" and char not in symbols:
                    symbols.append(char)
        return symbols

    #Prints the augmented grammar
    def printAugmentedGrammar(self):
        print("Augmented Grammar\n-----------------")
        for tup in self.aug_productions:
            print("%s->%s" % (tup[0], tup[1]))

    #Returns a symbol that is preceeded by an '@', or False if no such symbol exists
    def dotBeforeSymbol(self, RHS, nonTerminal=False):
        if nonTerminal:
            regex = re.compile(r'@([A-Z])')
        else:
            regex = re.compile(r'@(.)')
        result = regex.search(RHS)
        return False if not result else result.group(1).strip('@')

    #Returns the entire right hand side of a production that contains an '@'
    #but only if the '@' is not the last character.
    def rhsWithSymbol(self, RHS):
        regex = re.compile(r'.*@.+')
        result = regex.search(RHS)
        return False if not result else result.group()

    #Returns the closure of a production as a list of tuples
    def closure(self, LHS, RHS):
        J = [(LHS, RHS)]
        done = []
        added = True
        while(added):
            added = False
            for item in J:
                nextClosureChar = self.dotBeforeSymbol(item[1], True)
                if nextClosureChar and nextClosureChar not in done:
                    done.append(nextClosureChar)
                    for prod in self.aug_productions[1:]:
                        if prod[0] == nextClosureChar:
                            newProd = (prod[0], "@%s" % prod[1])
                            J.append(newProd)
                            added = True
        return J

    #Returns the result of the goto operation as a list of strings
    def goto(self, set_of_items, symbol):
        goto_result = []
        for item in set_of_items:
            if ("@%s" % symbol) in item[1]:
                new_RHS = item[1].replace("@%s" % symbol, "%s@" % symbol)
                goto_result.extend(self.closure(item[0], new_RHS))
        return goto_result

    #The main function to calculate LR(0) items.
    def items(self):
        C = []
        C.append(self.closure("'", "@%s" % self.productions[0]))
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

    #Prints the formatted result of LR(0) item calculation.
    def printOutput(self, data):
        print("\nSets of LR(0) Items\n-------------------")
        for set_of_items in range(len(data)):
            print("I%s:" % set_of_items)
            examinedGotoSymbols = []
            for item in data[set_of_items]:
                itemString = "%s->%s" % (item[0], item[1])
                gotoSymbol = self.dotBeforeSymbol(item[1])
                if gotoSymbol and gotoSymbol not in examinedGotoSymbols:
                    examinedGotoSymbols.append(gotoSymbol)
                    gotoState = self.getGotoState(data, self.rhsWithSymbol(item[1]))
                    print("   %-20s goto(%s)=I%s" % (itemString, gotoSymbol, gotoState))
                else:
                    print("   %-20s" % itemString)
            print()
    
    #Returns the state to goto for the right-hand side rhs.
    def getGotoState(self, data, rhs):
        symbol = self.dotBeforeSymbol(rhs)
        gotoString = rhs.replace("@%s" % symbol, "%s@" % symbol)
        for set_of_items in range(len(data)):
            for item in data[set_of_items]:
                if item[1] == gotoString:
                    return set_of_items


if __name__ == "__main__":
    lr0Items = LR0Items()
    lr0Items.printAugmentedGrammar()
    result = lr0Items.items()
    lr0Items.printOutput(result)
