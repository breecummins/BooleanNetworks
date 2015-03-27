def posHillFunction(U,L,T,n,X):
    return (U-L) * X**n / (X**n + T**n) + L
    
def negHillFunction(U,L,T,n,X):
    return (U-L) * T**n / (X**n + T**n) + L

def makeHillStrs(U,L,T,n,j):
    scalar = "("+U+"-"+L+")"
    Xn = "X["+j+"]**"+n
    Tn = T+"**"+n
    denom = "("+Xn+"+"+Tn+")"
    neghill=scalar+"*"+Tn+"/"+denom+" + "+ L
    poshill=scalar+"*"+Xn+"/"+denom+" + "+ L
    return neghill,poshill

def makeHillEqns(eqnstr,params,vals,n):
    # Cannot use posHillFunction and negHillFunction in this algorithm
    # because X is not yet defined (and we can't multiply or add lambda functions).
    # eval a lambda function instead
    eqns=[]
    for k,e in enumerate(eqnstr):
        K=str(k)
        for j in range(len(eqnstr)):
            J=str(j)
            # if j affects k, find U,L,T in params
            if J+' ' in e: 
                U,L,T=None,None,None
                for p,v in zip(params,vals):
                    if J+','+K in p:
                        exec(p[0]+"= str(v)")
                    if filter(None,[U,L,T])==[U,L,T]: 
                        #quit when U,L,T assigned
                        break
                neghill,poshill=makeHillStrs(U,L,T,str(n),J)
                e=e.replace(J+' n',neghill).replace(J+' p',poshill)
        e="lambda X: -X["+K+"] + " + e
        eqns.append(eval(e))
    return eqns

