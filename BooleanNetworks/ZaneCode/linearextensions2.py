def flattenlessone(l):
    if all(isinstance(el, list) for el in l) and not any(isinstance(a,list) for el in l for a in el):
        return l
    else:
        flat = []
        for el in l:
            flat.append(el) if not isinstance(el,list) else flat.extend(flattenlessone(el))
        return flat

def least(partord):
    RHS = [item for tup in partord for item in tup[1] ]
    return [t[0] for t in partord if t[0] not in RHS]
    
def recurseorder(N,partord,order=[]):
    if len(order) == N:
        return order
    else:
        orders=[]
        smallest = least(partord)
        for s in smallest:
            orders.append(recurseorder(N,[t for t in partord if t[0] != s],order+[s]))
        return flattenlessone(orders)

if __name__ == "__main__":
    # # data model is [(1,(less thans for 1)),(2,(less thans for 2)),...]
    # print(least([(1,(3,)),(4,(2,3)),(2,()),(3,())]))
    print(recurseorder(3,[(1,(2,)),(2,()),(3,())]))
    print(recurseorder(4,[(1,(2,3,4)),(2,(4,)),(3,(4,)),(4,())]))
