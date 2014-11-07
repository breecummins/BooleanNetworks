def checkpartialorder(order,kp):
    for i,k in enumerate(order):
        for m in order[i+1:]:
            if [m,k] in kp:
                return False
    return True

def addpairs(k,order,kp):
    pos = order.index(k)
    for q in order[:pos]:
        if [q,k] not in kp:
            kp.append([q,k])
    for q in order[pos+1:]:
        if [k,q] not in kp:
            kp.append([k,q])
    return kp

def insertall(k,order):
    return [order[:pos]+[k]+order[pos:] for pos in range(len(order)+1)]

def recurseorder1(N,kp,order=[1]):
    # This version returns duplicate copies in nested lists. Not ideal. See Graham's flat map to try and fix.
    if len(order) == N:
        return order
    else:
        orders = []
        for k in range(1,N+1):
            if k in order:
                continue
            else:
                for o in insertall(k,order):
                    if checkpartialorder(o,kp):
                        orders.append(recurseorder1(N,kp,o))
        return orders

def recurseorder(N,kp,order=[1]):
    if len(order) == N:
        return order
    else:
        orders=[]
        for k in range(1,N+1):
            if k in order:
                continue
            else:
                c = [r for o in insertall(k,order) for r in recurseorder(N,kp,o) if checkpartialorder(o,kp)]
                print(c)
                orders.append([q for q in c if q not in orders])
        return orders
        # return [r for k in range(2,N+1) for o in insertall(k,order) for r in recurseorder(kp,N,o) if checkpartialorder(o,kp)]

if __name__ == '__main__':
    l=recurseorder(3,[[1,2]])
    print('------')
    print(l)
    # print(linearextensions(4,[[1,2],[1,3],[1,4],[2,4],[3,4]]))

