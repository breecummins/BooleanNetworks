def Repress(z,beta=None,K=None):
    if z > 0:
        return -K
    else:
        return beta-K

def Activate(x,alpha=None,K=None):
    if x > 0:
        return alpha-K
    else:
        return -K

def ActivatePlusRepress(y,z,alpha=None,beta=None,K=None):
    return Activate(y,alpha,K) + Repress(z,beta,0)

def ActivatePlusActivate(x,y,alpha1=None,alpha2=None,K=None):
    return Activate(x,alpha1,K) + Activate(y,alpha2,0)

def ActivatePlusActivatePlusRepress(x,y1,y2,alpha1=None,alpha2=None,beta=None,K=None):
    return Activate(x,alpha1,K) + Activate(y1,alpha2,0) + Repress(y2,beta,0)
