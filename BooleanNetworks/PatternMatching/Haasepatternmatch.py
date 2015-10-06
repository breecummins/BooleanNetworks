import malariapatternmatch as useDSGRN
from itertools import permutations
import findmorsegraph as fmg

def model5D_Model_B(smallestparam=211895,largestparam=212541,paramsstored=1,resultsfile='results_5D_B.txt'):
    def setPattern():
        f=open('patterns.txt','w')
        for s1 in permutations(['Y1 max','Y2 max','Z max']):
            patternstr1='X max, ' + ', '.join(s1) + ', Y3 max, X min, '
            for s2 in permutations(['Y1 min','Y2 min','Z min']):
                patternstr2=patternstr1 + ', '.join(s2) + ', Y3 min, X max \n'
                f.write(patternstr2)
        f.close()
    setPattern()
    useDSGRN.patternSearch(fname="networks/5D_Model_B.txt",smallestparam=smallestparam,largestparam=largestparam,getMorseSet=fmg.is_FC,paramsstored=paramsstored,resultsfile=resultsfile)

def collectPatterns(fname='results_5D_B.txt'):
    f=open(fname,'r')
    patternsuccess=[]
    for l in f.readlines():
        if l.startswith('Pattern: '):
            patternsuccess.append(l[9:])
    print set(patternsuccess)
    f.close()

if __name__=='__main__':
    model5D_Model_B(670267,675000,0,'results_5D_B_6.txt')
    collectPatterns('results_5D_B_6.txt')