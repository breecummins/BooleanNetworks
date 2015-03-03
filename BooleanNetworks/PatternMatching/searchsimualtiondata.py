import os, itertools
from patternmatch import callPatternMatch, callPatternMatchJSON, callPatternMatchJSONWriteFile

def simdata_5D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/INCC')  
    f=open(basedir+'patterns.txt','w')    
    patternstart=['X1 max','X2 max','X3 max']
    remainder=['X1 min','X2 min','X3 min','X4 max','X4 min','X5 max','X5 min']
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

def simdata_3D_Example():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Example/MGCC_5/')    
    callPatternMatch(basedir,'3D Example, MGCC 5')

def simdata_3D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_50/INCC_12/')    
    callPatternMatchJSON(basedir,'3D Cycle 1, MGCC 50, INCC 12')

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
    # simdata_4D_Cycle1()
    # simdata_5D_Cycle1()
    nummatches,paramsets,patterns=analyze_4D_Cycle1()
    print nummatches
    print len(paramsets)
    print len(patterns)