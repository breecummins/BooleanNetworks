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

def recurseorder(order,kp,N):
    if len(order) == N:
        return order
    else:
        orders = []
        for k in range(1,N+1):
            if k in order:
                continue
            else:
                for pos in range(len(order)+1):
                    o = order[:pos]+[k]+order[pos:]
                    if checkpartialorder(o,kp):
                        orders.append(recurseorder(o,kp,N))
        return orders

def linearextensions(N,knownpairs):
    return recurseorder([1],knownpairs,N)

if __name__ == '__main__':
    l=linearextensions(3,[[1,2]])
    print('------')
    print(l)
    # print(linearextensions(4,[[1,2],[1,3],[1,4],[2,4],[3,4]]))

