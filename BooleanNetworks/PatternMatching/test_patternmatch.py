from patternmatch import matchCyclicPattern
import preprocess as PP
import fileparsers as fp
import testcases as tc

def testme(showme=1):

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test0())

    pattern=['md','um','Mu','dM','md']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(3, 5, 10, 13, 11, 6, 3), (8, 10, 13, 11, 8)]

    pattern=['um','md'] #intermediate extrema
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    pattern=['ud','um','Mu'] # only exists as acyclic path, no associated cycle
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test1())

    pattern=['md','um','Mu','dM','md']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(8, 10, 13, 11, 8)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test2())

    pattern=['dM','md','um','Mu','dM']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(6,3,5,8,6),(6,3,5,10,13,11,6)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(8,6,3,5,8),(13,11,6,3,5,10,13)]

    pattern=['um','Mu'] #acyclic
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test3())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    match = matchCyclicPattern(patterns[0],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(0,4,9,10,6,3,0)]
    match = matchCyclicPattern(patterns[1],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test4())
    patternnames,patternmaxmin=fp.parsePatterns()

    pattern=['md','um','Mu','dM','md']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(6,5,7,10,11,9,6),(6,8,11,9,6)]

    pattern=['mdu','umu','Muu','dMu','mdu']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test5())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    match = matchCyclicPattern(patterns[0],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print match==[(8,13,15,18,19,12,4,1,8),(8,16,19,12,4,1,8),(0,7,15,18,19,12,4,1,0)]
    match = matchCyclicPattern(patterns[1],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test6())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    solutions=[[(4, 24, 17, 7, 23, 14, 4), (4, 8, 26, 19, 11, 7, 23, 14, 4), (4, 8, 26, 10, 17, 7, 23, 14, 4), (4, 8, 18, 27, 11, 7, 23, 14, 4)],[(16,9,27,11,7,23,14,4,16)],[(25,9,27,11,25)],None,[(5,9,27,11,7,23,5)],None]
    for p,s in zip(patterns,solutions):
        match=matchCyclicPattern(p,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)
        if s:
            if showme: print match==s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def testtiming(iterates=500):
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges = PP.filterAll(*tc.test6())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    solutions=[[(4, 24, 17, 7, 23, 14, 4), (4, 8, 26, 19, 11, 7, 23, 14, 4), (4, 8, 26, 10, 17, 7, 23, 14, 4), (4, 8, 18, 27, 11, 7, 23, 14, 4)],[(16,9,27,11,7,23,14,4,16)],[(25,9,27,11,25)],None,[(5,9,27,11,7,23,5)],None]
    for _ in range(iterates):
        for p,s in zip(patterns,solutions):
            match=matchCyclicPattern(p,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,showfirstwall=0,cyclewarn=0)

if __name__=='__main__':
    testme()
