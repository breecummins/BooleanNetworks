from patternmatch import matchPattern
import preprocess as pp
import fileparsers as fp
import testcases as tc
import walllabels as wl

def testme(showme=1):
    # find all matches
    test0(showme,findallmatches=1)
    test1(showme,findallmatches=1)
    test2(showme,findallmatches=1)
    test3(showme,findallmatches=1)
    test4(showme,findallmatches=1)
    test5(showme,findallmatches=1)
    test6(showme,findallmatches=1)
    test7(showme,findallmatches=1)
    test8(showme,findallmatches=1)
    # find first match only
    test0(showme,findallmatches=0)
    test1(showme,findallmatches=0)
    test2(showme,findallmatches=0)
    test3(showme,findallmatches=0)
    test4(showme,findallmatches=0)
    test5(showme,findallmatches=0)
    test6(showme,findallmatches=0)
    test7(showme,findallmatches=0)
    test8(showme,findallmatches=0)

def test0(showme=1,findallmatches=1):
    paramDict = wl.makeAllTriples(*tc.test0())

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(0, 1, 4, 6, 5, 2, 0), (3, 4, 6, 5, 3)]
    if showme and not findallmatches: print match==[(0, 1, 4, 6, 5, 2, 0)]

    pattern=['um','md'] #intermediate extrema
    match = matchPattern(pattern,paramDict,cyclic=0,findallmatches=findallmatches)
    if showme: print 'None' in match

    pattern=['ud','um','Mu'] # acyclic 
    match = matchPattern(pattern,paramDict,cyclic=0,findallmatches=findallmatches)
    if showme: print match==[(1,4,6)]

def test1(showme=1,findallmatches=1):
    paramDict = wl.makeAllTriples(*tc.test1())

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print match==[(0, 1, 3, 2, 0)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchPattern(pattern,paramDict,cyclic=0,findallmatches=findallmatches)
    if showme: print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test2(showme=1,findallmatches=1):
    paramDict = wl.makeAllTriples(*tc.test2())

    pattern=['dM','md','um','Mu','dM']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(2,0,1,3,2),(2,0,1,4,6,5,2)]
    if showme and not findallmatches: print match==[(2,0,1,3,2)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(3,2,0,1,3),(6,5,2,0,1,4,6)]
    if showme and not findallmatches: print match==[(3,2,0,1,3)]

    pattern=['um','Mu'] #acyclic
    match = matchPattern(pattern,paramDict,cyclic=0,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(1,4,6),(1,3)]
    if showme and not findallmatches: print match==[(1,3)]

def test3(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0],paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print match==[(0,2,4,5,3,1,0)]
    match = matchPattern(patterns[1],paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test4(showme=1,findallmatches=1):
    paramDict = wl.makeAllTriples(*tc.test4())
    patternnames,patternmaxmin=fp.parsePatterns()

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(1,0,2,5,6,4,1),(1,3,6,4,1)]
    if showme and not findallmatches: print match==[(1,0,2,5,6,4,1)]

    pattern=['mdu','umu','Muu','dMu','mdu']
    match = matchPattern(pattern,paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test5(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0],paramDict,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print match==[(4, 8, 10, 5, 2, 1, 4), (0, 3, 7, 9, 10, 5, 2, 1, 0), (3, 7, 9, 10, 5, 2, 1, 0, 3), (4, 6, 7, 9, 10, 5, 2, 1, 4)]
    if showme and not findallmatches: print match==[(3, 7, 9, 10, 5, 2, 1, 0, 3)]
    match = matchPattern(patterns[1],paramDict,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test6(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(0, 13, 9, 2, 12, 7, 0), (0, 3, 15, 11, 6, 2, 12, 7, 0), (0, 3, 15, 5, 9, 2, 12, 7, 0), (0, 3, 10, 16, 6, 2, 12, 7, 0)],[(8,4,16,6,2,12,7,0,8)],[(14,4,16,6,14)],None,[(1,4,16,6,2,12,1)],None]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,paramDict,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme and findallmatches: print match==s
            if showme and not findallmatches: print match[0] in s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def test7(showme=1,findallmatches=1):
    tc.test7()
    patterns,paramDict = pp.preprocess(cyclic=1)
    solutions=[None,None,[(1,2,3,4,5,0,1)],[(4,5,0,1,2,3,4)]]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,paramDict,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme: print match==s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def test8(showme=1,findallmatches=1):
    tc.test8()
    patterns,paramDict = pp.preprocess(cyclic=1)
    solutions=[[(1,2,6,0,1),(1, 3, 4, 5, 6, 0, 1)]]*4+[None]*4
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,paramDict,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme and findallmatches: print match==s
            if showme and not findallmatches: print match==[s[0]]
        else:
            if showme: print 'None' in match and 'Pattern' in match


if __name__=='__main__':
    testme()
