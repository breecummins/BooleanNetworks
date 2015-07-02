from patternmatch import matchPattern
import preprocess as PP
import fileparsers as fp
import testcases as tc
import walllabels as WL
from cProfile import runctx

def testtiming(iterates=5000):
    paramDict = WL.makeAllTriples(*tc.test6())
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    for _ in range(iterates):
        for p in patterns:
            match = matchPattern(p,paramDict,cyclic=1,showfirstwall=0)

if __name__=='__main__':
    runctx('testtiming()',globals(),locals())
