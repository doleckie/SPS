# Eliza Dolecki
# HW 5 Part 1 Fall 2017
# Written in Mac Terminal and Xcode

import sys, re

#----------
# Debugging
debugging = False
def debug(s):
    if debugging: print(s)

#-------------------------
# Operator Stack Function

opStack = []

def opPop():
    #pop the top value of opStack
    return opStack.pop()

def opPush(value):
    #push a value onto the top of opStack
    opStack.append(value)

#---------------------------
# Dictionary stack functions

dictStack = []

def dictPop():
    #pop the top value of dictStack (only used by end() function)
    return dictStack.pop()

def define(name, value):
    #create new dictionary
    d = {name : value}
    if dictStack == []:
        #if there is nothing in the stack push new dictionary
        dictStack.append(d)
    else:
        #pop top dictionary, update the dictionary with the definition, push dictionary back on stack
        curr = dictStack.pop()
        curr.update(d)
        dictStack.append(curr)

def dictPush(hold):
    #push a dictionary onto the top of dictStack (only used by begin() function)
    dictStack.append(hold)

def lookup(name):
    #because names when entered in as a token for calling do not have the '/' character add it
    name = '/' + name
    #if dictStack is empty return false
    if len(dictStack) == 0:
        return False
    #if dictStack is not empty, going from the top dictionary and working backwards look at each dictionary and if the name is in the stack return the value associated with it else return false
    for d in reversed(dictStack):
        if name in d.keys():
            return d[name]
    return False

#----------------------
# Arithmetic Operations

def add():
    #pop top two values of opStack (due to commutative rule doesn't matter order of numbers) and add them
    op1 = opPop()
    op2 = opPop()
    opPush(op2 + op1)

def sub():
    #pop top two values of opStack, the first number is op2 the second number is op1, subtract op1 from op2
    op1 = opPop()
    op2 = opPop()
    opPush(op2 - op1)

def mul():
    #pop top two values of opStack (due to commutative rule doesn't matter order of the numbers) and multiply them
    op1 = opPop()
    op2 = opPop()
    opPush(op1 * op2)

def div():
    #pop top two values of opStack, the first number is op2 the second number is op1 divide op2 by op1
    op1 = opPop()
    op2 = opPop()
    
    #divide by 0 check
    if op1 == 0:
        opPush("Divide by 0 error")
        return
    
    opPush(op2/op1)

def eq():
    #pop top two values of opStack, if op1 is equal to op2 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op1 == op2)

def lt():
    #pop top two values of opStack, if op2 is less than op1 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op2 < op1)

def gt():
    #pop top two values of opStack, if op2 is greater than op1 return True
    op1 = opPop()
    op2 = opPop()
    opPush(op2 > op1)

#------------------
# String Operations

def length():
    str = opPop()
    
    #input fails check
    if str == "" or str == "()":
        opPush("Empty string")
        return
    
    opPush(len(str) - 2)
    #The string length is minus two due to the () surrounding it

def get():
    #pop value and string and return the element value at value in the string
    val = opPop()
    str = opPop()
    
    #Input fails checks
    if str == "" or str == "()":
        opPush("Empty string")
        return
    if val > (len(str) - 1):
        opPush("Index not in string")
        return

    final = ord(str[val + 1]) #add one due to the beginning '('
    opPush(final)

def getInterval():
    #get the number of characters, the starting index and the string, substring is created with the () surrounding and index must have +1 to account for the starting '(' character
    count = opPop()
    index = opPop()
    str = opPop()
    
    #Input fails checks
    if str == "" or str == "()":
        opPush("Empty string")
        return
    if ((index + 1) > (len(str) - 1)):
        opPush("Index not in string")
        return
    if ((index + 1 + count) > (len(str) - 1)):
        opPush("Past end of string")
        return

    substr = '(' + str[(index + 1):((index + 1) + count)] + ')'
    opPush(substr)

#------------------
# Boolean operators

def psAnd():
    #take top two values of opStack and return the boolean value of and (true & true = true, true & false = false, false & true = false, false & false = false)
    op1 = opPop()
    op2 = opPop()
    
    #input fails check
    if type(op1) != bool or type(op2) != bool:
        opPush("One of the values is not a boolean")
        return
    
    opPush(op2 and op1)

def psOr():
    #take top two values of opStack and return the boolean value of or (true or true = true, true or false = true, false or true = true, false or false = false)
    op1 = opPop()
    op2 = opPop()
    
    #input fails check
    if type(op1) != bool or type(op2) != bool:
        opPush("One of the values is not a boolean")
        return
    
    opPush(op2 or op1)

def psNot():
    #take the top value of opStack and return boolean value of not (true = false, false = true)
    op1 = opPop()
    
    #input fails check
    if type(op1) != bool:
        opPush("The value is not a boolean")
        return
    
    opPush(not op1)

#----------------------------
# Operator Stack Manipulation

def dup():
    #take top value of opStack and push it onto stack twice
    val = opPop()
    opPush(val)
    opPush(val)

def exch():
    #take top two values op opStack op2 is the first value op1 is the second value, push op1 on first then op2
    op1 = opPop()
    op2 = opPop()
    opPush(op1)
    opPush(op2)

def pop():
    #pop top value on stack
    opPop()

def roll():
    #pop top two values on the stack, op2 is the number of objects, op1 is the number of shifts
    op1 = opPop()
    op2 = opPop()
    
    #create a stack that starts at length of opStack - the number of objects to the end of the stack
    hold = opStack[len(opStack) - op2:]
    
    if op1 > 0:
        #if number is not negative, then rotate right
        temp = hold[op1:]
        hold[op1:] = []
        hold[:0] = temp
    elif op1 < 0:
        #else if negative rotate left
        temp = hold[0:(-1 * op1)]
        hold[:(-1 * op1)] = []
        hold[len(hold):] = temp
    
    #pop the values off of opStack
    for i in range(0,op2):
        opStack.pop()
    
    #push the new values onto the opStack
    for x in hold:
        opPush(x)

def copy():
    #create a blank stack, take the top value of opStack which is the number of items from opStack to copy and put in hold then add the new items to the end of the stack
    hold = []
    val = opPop()
    hold[:] = opStack[-val:]
    for x in hold:
        opStack.append(x)

def clear():
    #delete all items in opStack
    del opStack[:]

def stack():
    #print the stack
    print("==============")
    for x in reversed(opStack):
        print(x)
    print("==============")

#------------------------------
# Dictionary Stack Manipulation

def psDict():
    #pop value on opStack, ignore it, and push blank dictionary onto opStack
    opPop()
    opPush({})

def begin():
    #pop the blank dictionary on opStack and push a new dictionary onto dictStack
    temp = opPop()
    dictPush(temp)

def end():
    #pop the top dictionary off of dictStack
    dictPop()

def psDef():
    #get the name of the definition and it's value from the opStack and define them in the dictionary
    value = opPop()
    name = opPop()
    define(name, value)

def dictClear():
    #clear the dictionary stack, used between testing only, not a function callable for the interpreter
    del dictStack[:]

#---------------
# Test Functions

#test the add operation
def testAdd():
    #test case 1
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    add()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-1)
    opPush(-3)
    add()
    if opPop() != -4: return False
    
    return True

#test the subtraction operation
def testSub():
    #test case 1
    opPush(3)
    opPush(1)
    sub()
    if opPop() != 2: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    sub()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-2)
    opPush(-3)
    sub()
    if opPop() != 1: return False
    
    return True

#test the multiplication operation
def testMul():
    #test case 1
    opPush(3)
    opPush(4)
    mul()
    if opPop() != 12: return False
    
    #test case 2
    opPush(0)
    opPush(0)
    mul()
    if opPop() != 0: return False
    
    #test case 3
    opPush(-3)
    opPush(-2)
    mul()
    if opPop() != 6: return False
    
    return True

#test the division operation
def testDiv():
    #test case 1
    opPush(12)
    opPush(4)
    div()
    if opPop() != 3: return False
    
    #test case 2
    opPush(10)
    opPush(0)
    div()
    if opPop() != "Divide by 0 error": return False
    
    #test case 3
    opPush(1)
    opPush(1)
    div()
    if opPop() != 1: return False
    
    return True

#test the equal comparison operation
def testEq():
    #test case 1
    opPush(5)
    opPush(5)
    eq()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(3)
    eq()
    if opPop() != False: return False
    
    #test case 3
    opPush(1)
    opPush(4)
    eq()
    if opPop() != False: return False

    return True

#test the less than comparison operation
def testLt():
    #test case 1
    opPush(3)
    opPush(4)
    lt()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(5)
    lt()
    if opPop() != False: return False
    
    #test case 3
    opPush(5)
    opPush(3)
    lt()
    if opPop() != False: return False
    
    return True

#test the greater than comparison operation
def testGt():
    #test case 1
    opPush(5)
    opPush(1)
    gt()
    if opPop() != True: return False
    
    #test case 2
    opPush(5)
    opPush(5)
    gt()
    if opPop() != False: return False
    
    #test case 3
    opPush(1)
    opPush(4)
    gt()
    if opPop() != False: return False
    
    return True

#test the length operation
def testLength():
    #test case 1
    opPush("(This is a test)")
    length()
    if opPop() != 14: return False
    
    #test case 2
    opPush("()")
    length()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("")
    length()
    if opPop() != "Empty string": return False
    
    return True

#test the get operation
def testGet():
    #test case 1
    opPush("(Hello)")
    opPush(3)
    get()
    if opPop() != 108: return False
    
    #test case 2
    opPush("")
    opPush(2)
    get()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("(Testing)")
    opPush(10)
    get()
    if opPop() != "Index not in string": return False
    
    return True

#test the getInterval operation
def testGetInterval():
    #test case 1
    opPush("(This is a test)")
    opPush(0)
    opPush(4)
    getInterval()
    if opPop() != "(This)": return False
    
    #test case 2
    opPush("")
    opPush(0)
    opPush(3)
    getInterval()
    if opPop() != "Empty string": return False
    
    #test case 3
    opPush("(Test this string)")
    opPush(16)
    opPush(5)
    getInterval()
    if opPop() != "Past end of string": return False
    
    #test case 4
    opPush("(Last test)")
    opPush(13)
    opPush(3)
    getInterval()
    if opPop() != "Index not in string": return False
    
    return True

#test the and comparison
def testAnd():
    #test case 1
    opPush(True)
    opPush(False)
    psAnd()
    if opPop() != False: return False
    
    #test case 2
    opPush(False)
    opPush(4)
    psAnd()
    if opPop() != "One of the values is not a boolean": return False
    
    return True

#test the or comparison
def testOr():
    #test case 1
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True: return False
    
    #test case 2
    opPush(0)
    opPush(True)
    psOr()
    if opPop() != "One of the values is not a boolean": return False
    
    return True

#test the not comparison
def testNot():
    #test case 1
    opPush(False)
    psNot()
    if opPop() != True: return False
    
    #test case 2
    opPush(3)
    psNot()
    if opPop() != "The value is not a boolean": return False
    
    return True

#test the duplication operation
def testDup():
    clear()
    opPush(3)
    dup()
    result = [3,3]
    
    #debugging
    if debugging:
        print("\n--Debugging dup--")
        stack()
    debug("^ testDup should be [3,3]")
    
    if opStack != result: return False
    return True

#test the exchange operation
def testExch():
    clear()
    opPush(4)
    opPush(3)
    exch()
    result = [3,4]
    
    #debugging
    if debugging:
        print("\n--Debugging exch--")
        stack()
    debug("^ testExch should be [3,4]")
    
    if opStack != result: return False
    return True

#test the pop operation
def testPop():
    clear()
    opPush(3)
    opPush(4)
    pop()
    result = [3]
    
    #debugging
    if debugging:
        print("\n--Debugging pop--")
        stack()
    debug("^ testPop should be [3]")
    
    if opStack != result: return False
    return True

#test the roll operation
def testRoll():
    clear()
    opPush(5)
    opPush(4)
    opPush(3)
    opPush(2)
    opPush(1)
    opPush(3)
    opPush(1)
    roll()
    result1 = [5,4,2,1,3]
    if opStack != result1: return False
    
    #debugging
    if debugging:
        print("\n--Debugging Roll--")
        stack()
    debug("^ testRoll with 3 items and 1 move should be [5,4,2,1,3]")

    opPush(3)
    opPush(-1)
    roll()
    result2 = [5,4,1,3,2]
    if opStack != result2: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll with 3 items and -1 move should be [5,4,1,3,2]")

    opPush(3)
    opPush(2)
    roll()
    result3 = [5,4,2,1,3]
    if opStack != result3: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll with 3 items and 2 moves should be [5,4,2,1,3]")
    
    opPush(3)
    opPush(-2)
    roll()
    result4 = [5,4,3,2,1]
    if opStack != result4: return False
    
    #debugging
    if debugging: stack()
    debug("^ testRoll wiht 3 items and -2 moves should be [5,4,3,2,1]")
    return True

#test the copy and clear operations
def testCopyandclear():
    clear()
    opPush(3)
    opPush(5)
    opPush(4)
    opPush(2)
    opPush(2)
    copy()
    result = [3,5,4,2,4,2]
    if opStack != result: return False
    
    #debugging
    if debugging:
        print("\n--Debugging copy--")
        stack()
    debug("^ testCopy should be [3,5,4,2,4,2]")
    clear()
    if opStack != []: return False
    
    #debugging
    if debugging:
        print("\n--Debugging clear--")
        stack()
    debug("^ testClear should be blank")
    return True

#test the define operation
def testpsDef():
    clear()
    dictClear()
    opPush(2)
    opPush("/s3")
    opPush(4)
    psDef()
    result = [{'/s3':4}]
    
    #debugging
    if debugging:
        print("\n--Debugging psDef--")
        print(dictStack)
    debug("^ dictionary stack should look like [{'s3':4}]")
    
    if dictStack != result: return False
    return True

#test the dict, begin, and end operations
def testDictBeginEnd():
    clear()
    dictClear()
    opPush(5)
    opPush("/s0")
    opPush(2)
    psDef()
    opPush("/s1")
    opPush(4)
    psDef()
    psDict()
    begin()
    opPush("/s2")
    opPush(5)
    psDef()
    result1 = [{'/s0':2, '/s1':4}, {'/s2':5}]
    if dictStack != result1: return False
    
    #debugging
    if debugging:
        print("\n--Debugging DictBeginEnd--")
        print(dictStack)
    debug("^ Dictionary 1 with '/s0' and '/s1' is the original dictstack, Dictionary 2 should be '/s2'")
    
    end()
    result2 = [{'/s0':2, '/s1':4}]
    
    #debugging
    if debugging: print(dictStack)
    debug("^ Dictionary 2 should be removed")
    
    if dictStack != result2: return False
    return True

#test the lookup operation
def testLookup():
    clear()
    dictClear()
    opPush(2)
    opPush("/s3")
    opPush(4)
    psDef()
    result = lookup("s3")
    
    #debugging
    if debugging:
        print("\n--Debugging lookup--")
        print(result)
    debug("^ lookup('s3') should return 4")
    if result != 4: return False
    return True

#-----
# Main

def main():
    testCases = [('add', testAdd),('sub', testSub), ('mul', testMul), ('div', testDiv), ('eq', testEq), ('lt', testLt), ('gt', testGt), ('length', testLength), ('get', testGet), ('getInterval', testGetInterval), ('and', testAnd), ('or', testOr), ('not', testNot), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('roll', testRoll), ('Copy and clear', testCopyandclear), ('psDef', testpsDef), ('lookup', testLookup), ('Dict, Begin, and End', testDictBeginEnd)]

    failedTests = [testName for (testName, testProc) in testCases if not testProc()]

    if failedTests:
        print('Some tests failed: ', failedTests)
    else:
        print('All tests passed')


if __name__ == "__main__":
    main()


