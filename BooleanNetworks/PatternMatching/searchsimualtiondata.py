import os, itertools
from patternmatch import callPatternMatch, callPatternMatchJSON, callPatternMatchJSONWriteFile, callPatternMatchJSONWriteFile_Dict

def simdata_5D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_Cycle_1_MGCC_14419_INCC_200/')  
    f=open(basedir+'patterns.txt','w')    
    # patternstart=['X1 max','X2 max','X3 max']
    # remainder=['X1 min','X2 min','X3 min','X4 max','X4 min','X5 max','X5 min']
    patternstart=['X5 min','X3 min','X1 max','X4 min','X2 max','X1 min']
    remainder=['X2 min','X3 max','X4 max','X5 max']
    for r in itertools.permutations(remainder):
        f.write(' '.join(patternstart+list(r))+'\n')
    f.close()
    callPatternMatchJSONWriteFile(basedir,'5D Cycle 1, MGCC 14419')

def simdata_4D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/4D_cycle_1/MGCC_1286/INCC_56/')  
    f=open(os.path.join(basedir+'patterns.txt'),'w')    
    patternstart=['X1 max']
    remainder=['X1 min','X2 min','X3 min','X4 min','X2 max','X3 max','X4 max']
    for r in itertools.permutations(remainder):
        f.write(' '.join(patternstart+list(r))+'\n')
    f.close()
    callPatternMatchJSONWriteFile(basedir,'4D Cycle 1, MGCC 1286, INCC 56')

def analyze_4D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/4D_cycle_1/MGCC_1286/INCC_56/') 
    f=open(os.path.join(basedir+'results.txt'),'r')  
    nummatches=-1
    paramsets=[]
    patterns=[]  
    for l in f.readlines():
        if l=='\n':
            nummatches+=1
        elif 'Parameter' in l:
            paramsets.append(int(l[14:16]))
        elif 'Pattern' in l:
            patterns.append(eval(l[9:-1]))
    patterns=[' '.join(p) for p in patterns]
    return nummatches,set(paramsets), set(patterns)

def simdata_4D_Cycle1_Haase():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/4D_cycle_1/MGCC_1286/INCC_56/')  
    f=open(os.path.join(basedir+'patterns.txt'),'w')    
    next1 = [['X1 max','X4 max','X3 min'],['X2 max'],['X1 min'],['X3 max']]
    next2 = [['X1 max','X3 min'],['X2 max','X4 max'],['X1 min'],['X3 max']]
    next3 = [['X1 max','X3 min'],['X4 max'],['X1 min'],['X2 max','X3 max']]
    patternstart=[['X4 min','X2 min'],['X2 min','X4 min']]
    def makepatterns(patternstart,next):
        patterns=patternstart
        for n in next:
            newpatterns=[]
            for r in itertools.permutations(n):
                newpatterns.extend([p+list(r) for p in patterns])
            patterns=newpatterns
        return patterns
    patterns=makepatterns(patternstart,next1)+makepatterns(patternstart,next2)+makepatterns(patternstart,next3)
    for p in patterns:
        f.write(' '.join(p)+'\n')
    f.close()
    callPatternMatchJSONWriteFile_Dict(basedir,'4D Cycle 1, MGCC 1286, INCC 56')

def makeParamSubGraphKonstantin():
    # one-off code
    nummatches,paramsets,patterns=analyze_4D_Cycle1()

    paramnums=[ 108873, 108875, 108876, 108878, 108879, 108881, 108882, 108943, 108948, 108952, 108971, 109592, 109616, 109617, 109618, 109619, 110455, 110460, 111967, 111972, 139122, 139857, 139858, 290313, 290315, 290316, 290318, 290319, 290321, 290322, 290383, 290388, 290392, 290411, 291032, 291056, 291057, 291058, 291059, 291825, 291827, 291828, 291830, 291831, 291833, 291834, 291895, 291900, 292568, 292570, 292571, 293337, 293339, 293340, 293342, 293343, 293345, 293346, 294082, 320553, 320555, 320556, 320558, 320559, 320561, 320562, 320623, 320628, 320632, 320651, 321272, 321296, 321297, 321298, 321299, 322065, 322067, 322068, 322070, 322071, 322073, 322074, 322135, 322140, 322808, 322810, 322811, 323577, 323579, 323580, 323582, 323583, 323585, 323586, 323647, 323652, 324320, 324322, 324323 ]

    paramswithmatches=[]
    for p in paramsets:
        paramswithmatches.append(paramnums[p])
    # notthere=sorted(list(set(paramnums).difference(paramswithmatches)))
    # nottherestrs=[str(p) for p in notthere]
    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/4D_cycle_1/MGCC_1286/INCC_56/') 
    # f=open(basedir+'parameterSubGraph.gv','w')
    # g=open(basedir+'parameterGraphForaGivenMGCC.gv','r')
    # for l in g.readlines():
    #     if any([n in l for n in nottherestrs]):
    #         pass
    #     else:
    #         f.write(l)
    # f.close()
    # g.close()

    colors=''
    graphparams=[324323,324322,324320,291834,291058,291830,291827,291831,323647,321296,290411,290388,320555,290383,290322,290319,322135,290318,290315,322810,323586,322808,291057,139858,290316,322811,108943,293340,108879,291059,109592,108882,108881,320632,290392,108878,108876,108971,291056,291833,108952,320559,109619,323585,293337,108875,110460,320562,291032,291828,110455,109617,111967,111972,321298,322074,290321,108948,293345,139122,291895,322067,292568,292570,108873,293346,292571,293339,293342,293343,139857,294082,320553,109616,291900,320556,109618,320558,290313,320561,320623,320628,320651,321297,291825,322073,321299,322065,321272,322068,322070,322071,322140,323577,323579,323580,323582,323583,323652]
    for g in graphparams:
        if g in paramswithmatches:
            colors=colors+' [color=red]\n'
        else:
            colors=colors+' [color=black]\n'
    print colors


def simdata_3D_Example():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Example/MGCC_5/')    
    callPatternMatch(basedir,'3D Example, MGCC 5')

def simdata_3D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_50/INCC_12/')    
    callPatternMatchJSONWriteFile(basedir,'3D Cycle 1, MGCC 50, INCC 12')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_30/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 30')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_31/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 31')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_32/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 32')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_43/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 43')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_45/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 45')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_50/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 50')

    # basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_54/')    
    # callPatternMatch(basedir,'3D Cycle 1, MGCC 54')


if __name__=='__main__':
    # simdata_3D_Example()
    # simdata_3D_Cycle1()
    simdata_4D_Cycle1()
    # simdata_4D_Cycle1_Haase()
    # simdata_5D_Cycle1()
    # nummatches,paramsets,patterns=analyze_4D_Cycle1()
    # print nummatches
    # print len(paramsets)
    # print len(patterns)

