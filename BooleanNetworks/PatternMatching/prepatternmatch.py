import walllabels as WL

def constructCyclicPatterns(varnames,patternnames,patternmaxmin):
    numvars=len(varnames)
    varinds=[[varnames.index(q) for q in p] for p in patternnames]
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
                        K=(K-1)%P #the mod P means I'm assuming cyclicity
                    wordlist[k][n] = 'd' if wordlist[K][n] in ['M','d'] else 'u'
        wordlist+=[wordlist[0]]
        patterns.append([''.join(w) for w in wordlist])
    return patterns

def varsAtWalls(threshnames,walldomains,wallthresh,varnames):
    varsaffectedatthresh=[-1]*len(threshnames)
    for t in threshnames:
        varsaffectedatthresh[varnames.index(t[0])]=tuple([varnames.index(u) for u in t[1]])
    varsaffectedatwall=[-1]*len(walldomains)
    for k,(j,w) in zip(wallthresh,enumerate(walldomains)): #CHECKME: Must handle boundaries
        if k>-1 and w[k]-int(w[k])<0.25 and 0<w[k]<len(varsaffectedatthresh[k])+1:
            varsaffectedatwall[j]=varsaffectedatthresh[k][int(w[k]-1)]
    return varsaffectedatwall

def filterBoundaryWallsSteadyStatesWhiteWalls(outedges):
    # get rid of boundary walls, steady states, white walls and other non-cyclic walls 
    # (assuming that black walls do not exist in the system) to reduce the number of
    # searchable walls
    # NOTE: This may not be needed if we can get the Morse set directly.
    inedges=WL.getInEdges(outedges)
    interiorinds=[]
    for q,(o,i) in enumerate(zip(outedges,inedges)):
        if i and (o!=(q,)): 
            interiorinds.append(q)
    interioroutedges=[]
    for k in interiorinds:
        interioroutedges.append(tuple([interiorinds.index(j) for j in outedges[k] if j in interiorinds]))
    return interiorinds,interioroutedges

def filterWallProperty(interiorinds,wallproperty):
    return [p for i,p in enumerate(wallproperty) if i in interiorinds]

if __name__=='__main__':
    for p in constructCyclicPatterns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt"):
        print p 
