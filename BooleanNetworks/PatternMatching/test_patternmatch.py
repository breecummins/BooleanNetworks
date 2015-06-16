# from patternmatch import matchPattern
from patternmatch_triples import matchPattern
import preprocess as PP
import fileparsers as fp
import testcases as tc

def testme(showme=1):

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test0())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print match==[(3, 5, 10, 13, 11, 6, 3), (8, 10, 13, 11, 8)]

    pattern=['um','md'] #intermediate extrema
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    pattern=['ud','um','Mu'] # only exists as acyclic path, no associated cycle
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0,)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test1())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print match==[(8, 10, 13, 11, 8)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test2())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}

    pattern=['dM','md','um','Mu','dM']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print match==[(6,3,5,8,6),(6,3,5,10,13,11,6)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print match==[(8,6,3,5,8),(13,11,6,3,5,10,13)]

    pattern=['um','Mu'] #acyclic
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test3())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructAcyclicPatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0],inds,paramDict,showfirstwall=0)
    if showme: print match==[(0,4,9,10,6,3,0)]
    match = matchPattern(patterns[1],inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test4())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    patternnames,patternmaxmin=fp.parsePatterns()

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print match==[(6,5,7,10,11,9,6),(6,8,11,9,6)]

    pattern=['mdu','umu','Muu','dMu','mdu']
    match = matchPattern(pattern,inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test5())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructAcyclicPatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0],inds,paramDict,showfirstwall=0)
    if showme: print match==[(8,13,15,18,19,12,4,1,8),(8,16,19,12,4,1,8),(0,7,15,18,19,12,4,1,0)]
    match = matchPattern(patterns[1],inds,paramDict,showfirstwall=0)
    if showme: print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test6())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructAcyclicPatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(4, 24, 17, 7, 23, 14, 4), (4, 8, 26, 19, 11, 7, 23, 14, 4), (4, 8, 26, 10, 17, 7, 23, 14, 4), (4, 8, 18, 27, 11, 7, 23, 14, 4)],[(16,9,27,11,7,23,14,4,16)],[(25,9,27,11,25)],None,[(5,9,27,11,7,23,5)],None]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,inds,paramDict,showfirstwall=0)
        if s:
            if showme: print match==s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def testtiming(iterates=500):
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test6())
    paramDict = {'walldomains':walldomains,'outedges':outedges,'varsaffectedatwall':varsaffectedatwall,'allwalllabels':allwalllabels,'inedges':inedges,'triples':triples,'sortedwalllabels':sortedwalllabels}
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructAcyclicPatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(4, 24, 17, 7, 23, 14, 4), (4, 8, 26, 19, 11, 7, 23, 14, 4), (4, 8, 26, 10, 17, 7, 23, 14, 4), (4, 8, 18, 27, 11, 7, 23, 14, 4)],[(16,9,27,11,7,23,14,4,16)],[(25,9,27,11,25)],None,[(5,9,27,11,7,23,5)],None]
    for _ in range(iterates):
        for p in patterns:
            match = matchPattern(p,inds,paramDict,showfirstwall=0)

if __name__=='__main__':
    testme()
