import BooleanNetworks.PatternMatching.patternmatch as pm
import BooleanNetworks.PatternMatching.preprocess as pp
import BooleanNetworks.PatternMatching.fileparsers as fp
import doublecyclemodels as dcm
import itertools, sys

def searchForPatterns_Generator(model,showsanitycheck):
    perms=0
    print 'Searching...'
    sys.stdout.flush()
    f=open('results.txt','w',0)
    for r in itertools.permutations(model.patternremainder):
        patterns=pm.constructPatternGenerator(model.patternstart+list(r),model.varnames)
        for pattern in patterns:
            match=pm.matchCyclicPattern(pattern,model.origwallinds,model.outedges,model.walldomains,model.varsaffectedatwall,model.allwalllabels,showfirstwall=0,showsanitycheck=showsanitycheck)
            if 'None' not in match:
                f.write("Pattern: {}".format(pattern)+'\n')
                f.write("Results: {}".format(match)+'\n')
            perms+=1
            if perms%10000==0:
                print perms
                sys.stdout.flush()

def searchForPatterns(model,showsanitycheck):
    print 'Searching...'
    sys.stdout.flush()
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.constructCyclicPatterns(model.varnames,patternnames,patternmaxmin)
    f=open('results.txt','w',0)
    for pattern in patterns:
        match=pm.matchCyclicPattern(pattern,model.origwallinds,model.outedges,model.walldomains,model.varsaffectedatwall,model.allwalllabels,showfirstwall=0,showsanitycheck=showsanitycheck)
        if 'None' not in match:
            f.write("Pattern: {}".format(pattern)+'\n')
            f.write("Results: {}".format(match)+'\n')

    

if __name__=='__main__':
    print "Preprocessing..."
    sys.stdout.flush()
    # model=dcm.symmetric5D()
    model=dcm.oneintermediatenode()
    # searchForPatterns(model,0)
    # model=dcm.twointermediatenodesymmetric()
    # model=dcm.fullyconnected()
    # model=dcm.partiallyconnected()
    searchForPatterns_Generator(model,0)
    # model.checkAllChange()