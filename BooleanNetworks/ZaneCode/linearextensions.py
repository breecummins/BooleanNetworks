def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.extend(flattenlessone(el))
        return flat

def least(partord):
    # Faster, but more opaque. Uses set intersection and differencing after splitting apart the tuple values.
    z=zip(*partord)
    return set(z[0]) - ( set(z[0]) & set(sum(z[1],())) )

def least2(partord):
    # This method is not as fast as the other, but clearer
    return [t[0] for t in partord if t[0] not in set([item for tup in partord for item in tup[1]])]
    
def recurseorder(N,partord,order=[]):
    if len(order) == N:
        return order
    else:
        orders=[]
        for s in least(partord):
            orders.append(recurseorder(N,[t for t in partord if t[0] != s],order+[s]))
        return flattenlessone(orders)

if __name__ == "__main__":
    # # data model is [(1,(constraints for 1)),(2,(constraints for 2)),...]
    print(recurseorder(3,[(1,(2,)),(2,()),(3,())]))
    print(recurseorder(4,[(1,(2,3,4)),(2,(4,)),(3,(4,)),(4,())]))
