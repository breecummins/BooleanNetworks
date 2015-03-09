import BooleanNetworks.PatternMatching.patternmatch as pm
import doublecyclemodels as dcm

def searchForPatterns(model):
    param=1
    f=open('results.txt','w')
    for pattern in model.patterns:
        print "\n"
        print '-'*25
        print "Pattern {} of {}".format(param,len(model.patterns))
        match=pm.matchCyclicPattern(pattern,model.wallinds,model.walloutedges,model.walldomains,model.varsaffectedatwall,model.allwalllabels,showfirstwall=0)
        if 'None' not in match:
            f.write("Pattern: {}".format(pattern)+'\n')
            f.write("Results: {}".format(match)+'\n')
        param+=1
    f.close()

if __name__=='__main__':
    # model=dcm.oneintermediatenode()
    print "Preprocessing..."
    model=dcm.symmetric5D()
    searchForPatterns(model)
