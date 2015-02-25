import BooleanNetworks.PatternMatching.patternmatch as pm
import doublecyclemodels as dcm

def searchForPatterns(model):
    print "Preprocessing..."
    for pattern in model.patterns:
        print "\n"
        print '-'*25
        print "Pattern: {}".format(pattern)
        match=pm.matchCyclicPattern(pattern,model.wallinds,model.walloutedges,model.walldomains,model.varsaffectedatwall,model.allwalllabels,showfirstwall=0)
        print "Results: {}".format(match)
        print '-'*25
        # sys.stdout.flush()

if __name__=='__main__':
    # model=dcm.oneintermediatenode()
    model=dcm.symmetric5D()
    searchForPatterns(model)
