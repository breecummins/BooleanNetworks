from patternmatch import matchPattern_Dict, matchPattern
import fileparsers as fp
import testcases as tc
import walllabels as WL
import preprocess as PP

def testme(showme=1):
    test0(showme)
    test1(showme)
    test2(showme)
    test3(showme)
    test4(showme)
    test5(showme)
    test6(showme)

def test0(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test0())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}

    pattern=['md','um','Mu','dM','md']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(0, 1, 4, 6, 5, 2, 0), (3, 4, 6, 5, 3)]

    pattern=['um','md'] # intermediate extrema
    match = matchPattern_Dict(pattern,paramDict,cyclic=0,showfirstwall=0)
    if showme: print 'None' in match

    pattern=['ud','um','Mu'] # acyclic
    match = matchPattern_Dict(pattern,paramDict,cyclic=0,showfirstwall=0)
    if showme: print match==[(1,4,6)]

def test1(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test1())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}

    pattern=['md','um','Mu','dM','md']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(0, 1, 3, 2, 0)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchPattern_Dict(pattern,paramDict,cyclic=0,showfirstwall=0)
    if showme: print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print 'None' in match

def test2(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test2())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}

    pattern=['dM','md','um','Mu','dM']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(2,0,1,3,2),(2,0,1,4,6,5,2)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(3,2,0,1,3),(6,5,2,0,1,4,6)]

    pattern=['um','Mu'] #acyclic
    match = matchPattern_Dict(pattern,paramDict,cyclic=0,showfirstwall=0)
    if showme: print match==[(1,4,6),(1,3)]

def test3(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test3())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern_Dict(patterns[0],paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(0,2,4,5,3,1,0)]
    match = matchPattern_Dict(patterns[1],paramDict,cyclic=1,showfirstwall=0)
    if showme: print 'None' in match

def test4(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test4())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}
    patternnames,patternmaxmin=fp.parsePatterns()

    pattern=['md','um','Mu','dM','md']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(1,0,2,5,6,4,1),(1,3,6,4,1)]

    pattern=['mdu','umu','Muu','dMu','mdu']
    match = matchPattern_Dict(pattern,paramDict,cyclic=1,showfirstwall=0)
    if showme: print 'None' in match

def test5(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test5())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern_Dict(patterns[0],paramDict,cyclic=1,showfirstwall=0)
    if showme: print match==[(4,6,7,9,10,5,2,1,4),(4,8,10,5,2,1,4),(0,3,7,9,10,5,2,1,0)]
    match = matchPattern_Dict(patterns[1],paramDict,cyclic=1,showfirstwall=0)
    if showme: print 'None' in match

def test6(showme=1):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test6())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(0, 13, 9, 2, 12, 7, 0), (0, 3, 15, 11, 6, 2, 12, 7, 0), (0, 3, 15, 5, 9, 2, 12, 7, 0), (0, 3, 10, 16, 6, 2, 12, 7, 0)],[(8,4,16,6,2,12,7,0,8)],[(14,4,16,6,14)],None,[(1,4,16,6,2,12,1)],None]
    for p,s in zip(patterns,solutions):
        match = matchPattern_Dict(p,paramDict,cyclic=1,showfirstwall=0)
        if s:
            if showme: print match==s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def testtiming(iterates=500):
    numwalls,walllabels=WL.makeDictOfWallLabels(*tc.test6())
    paramDict = {'walllabels':walllabels,'numwalls':numwalls}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(0, 13, 9, 2, 12, 7, 0), (0, 3, 15, 11, 6, 2, 12, 7, 0), (0, 3, 15, 5, 9, 2, 12, 7, 0), (0, 3, 10, 16, 6, 2, 12, 7, 0)],[(8,4,16,6,2,12,7,0,8)],[(14,4,16,6,14)],None,[(1,4,16,6,2,12,1)],None]
    for _ in range(iterates):
        for p in patterns:
            match = matchPattern_Dict(p,paramDict,cyclic=1,showfirstwall=0)

if __name__=='__main__':
    testme()