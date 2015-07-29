# coding=utf-8

# assemble of some helper function

def incOrSet(dicName,keyName,incBy,initVal):
    if keyName in dicName:
        dicName[keyName]+=incBy
    else:
        dicName[keyName]=initVal
