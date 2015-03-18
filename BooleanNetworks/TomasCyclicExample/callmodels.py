import BooleanNetworks.PatternMatching.patternmatch as pm
import doublecyclemodels as dcm
import itertools, sys

def searchForPatterns(model):
    perms=0
    print 'Searching...'
    sys.stdout.flush()
    f=open('results.txt','w')
    for r in itertools.permutations(model.patternremainder):
        patterns=pm.constructPatternGenerator(model.patternstart+list(r),model.varnames)
        for pattern in patterns:
            match=pm.matchCyclicPattern(pattern,model.origwallinds,model.outedges,model.walldomains,model.varsaffectedatwall,model.allwalllabels,showfirstwall=0)
            if 'None' not in match:
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
            perms+=1
            if perms%10000==0:
                print perms
                sys.stdout.flush()
    

if __name__=='__main__':
    print "Preprocessing..."
    sys.stdout.flush()
    # model=dcm.symmetric5D()
    model=dcm.oneintermediatenode()
    # model=dcm.twointermediatenodesymmetric()
    # model=dcm.fullyconnected()
    # model=dcm.partiallyconnected()
    searchForPatterns(model)
    # model.checkAllChange()