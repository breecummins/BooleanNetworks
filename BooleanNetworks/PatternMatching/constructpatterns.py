import fileparsers as fp

def constructCyclicPatterns(vname="variables.txt",pname="patterns.txt"):
    varnames=fp.parseVars(vname)
    patternnames,patternmaxmin=fp.parsePatterns(pname)
    varinds = [[varnames.index(q) for q in p] for p in patternnames]
    numvars=len(varnames)
    patterns=[]
    for v,p in zip(varinds,patternmaxmin):
        P=len(p)
        wordlist=[['0' for _ in range(numvars)] for _ in range(P)]
        for i,(k,q) in zip(v,enumerate(p)):
            wordlist[k][i] = 'M' if q=='max' else 'm' 
        for k in range(P):
            for n in range(numvars):
                if wordlist[k][n]=='0':
                    K=k
                    while wordlist[K][n] == '0':
                        K=(K-1)%P
                    wordlist[k][n] = 'd' if wordlist[K][n] in ['M','d'] else 'u'
        patterns.append([''.join(w) for w in wordlist])
    return patterns

if __name__=='__main__':
    for p in constructCyclicPatterns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt"):
        print p 