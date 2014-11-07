def checkpartialorder(order,kp):
    for i,k in enumerate(order):
        for m in order[i+1:]:
            if [m,k] in kp:
                return False
    return True

def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.append(el) if not isinstance(el,list) else flat.extend(flattenlessone(el))
        return flat

def insertall(k,order):
    return [order[:pos]+[k]+order[pos:] for pos in range(len(order)+1)]

def recurseorder(N,kp,order=[1]):
    if len(order) == N:
        return order
    else:
        orders=[]
        for k in range(1,N+1):
            if k in order:
                continue
            else:
                orders.extend(flattenlessone([recurseorder(N,kp,o) for o in insertall(k,order) if checkpartialorder(o,kp)]))
        return orders

def linearextensions(N,kp):
    l=recurseorder(N,kp)
    return set([tuple(x) for x in l])


if __name__ == '__main__':
    # This algorithm is not nearly as good as linearextensions2.py.
    print(linearextensions(3,[[1,2]]))
    print(linearextensions(4,[[1,2],[1,3],[1,4],[2,4],[3,4]]))

