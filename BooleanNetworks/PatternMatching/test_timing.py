from patternmatch import matchPattern
import preprocess as pp
import fileparsers as fp
import testcases as tc
import walllabels as wl
from cProfile import runctx

def testtiming(iterates=5000):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    for _ in range(iterates):
        for p in patterns:
            match = matchPattern(p,paramDict,cyclic=1,findallmatches=1)

if __name__=='__main__':
    runctx('testtiming()',globals(),locals())
