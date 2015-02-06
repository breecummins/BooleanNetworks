from patternmatch import matchCyclicPattern
import preprocess as PP
import fileparsers as fp
import testcases as tc

def testme():

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test0())

    pattern=['md','um','Mu','dM','md']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print match==[(3, 5, 10, 13, 11, 6, 3), (8, 10, 13, 11, 8)]

    pattern=['um','md'] #intermediate extrema
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match

    pattern=['ud','um','Mu'] # only exists as acyclic path, no associated cycle
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test1())

    pattern=['md','um','Mu','dM','md']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print match==[(8, 10, 13, 11, 8)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test2())

    pattern=['dM','md','um','Mu','dM']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print match==[(6,3,5,8,6),(6,3,5,10,13,11,6)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print match==[(8,6,3,5,8),(13,11,6,3,5,10,13)]

    pattern=['um','Mu'] #acyclic
    match = matchCyclicPattern(pattern,inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match

    #################################

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test3())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    match = matchCyclicPattern(patterns[0],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print match==[(0,4,9,10,6,3,0)]
    match = matchCyclicPattern(patterns[1],inds,outedges,walldomains,varsaffectedatwall,allwalllabels,showfirstwall=0,cyclewarn=0)
    print 'None' in match

if __name__=='__main__':
	testme()
