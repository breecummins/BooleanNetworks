def parseEqns(fname='equations.txt'):
    f=open(fname,'r')
    varnames=[]
    eqns=[]
    for l in f:
        L=l.split(' : ')
        varnames.append(L[0])
        eqns.append(L[1])
    f.close()
    eqnstr=[]
    for e in eqns:
        for k,v in enumerate(varnames):
            e=e.replace('~'+v,str(k)+' n').replace(v,str(k)+' p').replace(')(',')*(')
        eqnstr.append(e)
    return eqnstr,varnames

def parseSamples(varnames,fname='samples.txt'):
    f=open(fname,'r')
    params=[]
    vals=[]
    for l in f:
        L=l.split()
        params.append(L[0])
        vals.append(L[1])
    f.close()
    intparams=[]
    for p in params:
        for k,v in enumerate(varnames):
            p=p.replace(v,str(k))
        intparams.append(p)
    return intparams,vals

