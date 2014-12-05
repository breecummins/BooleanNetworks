import ast

def booleantomanyvalues(vardict):
    vardict['manyvaldomains'] = []
    vardict['extrema'] = []
    for k,bd in enumerate(vardict['booldomains']):
        invars = vardict['inputs'][k]
        print(invars)
        thresholds = [vardict['ordoutputs'][i].index(k)+1 for i in invars]
        print(thresholds)
        maxvals = [len(vardict['ordoutputs'][i])+1 for i in invars]
        alldoms = []
        for dom in bd:
            print(len(dom))
            thisdom=[]
            for j,d in enumerate(dom):
                if d == 0:
                    thisdom.append([0.5*n for n in range(1,2*thresholds[j])])
                else:
                    thisdom.append([0.5*n for n in range(2*thresholds[j]+1,2*maxvals[j])])
            alldoms.append(thisdom)
        vardict['manyvaldomains'].append(alldoms)
        vardict['extrema'].append(thresholds)
    return vardict

def removeboundaries(walls):
    # also must remove or mark steady states
    for k,w in enumerate(walls):
        if 0 in w[1:]:
            walls.pop(k)
    return walls
    
def parsewalls(f):
    # assuming ideal wall file
    # domains are 0.5, 1.5, etc - the average of the thresholds on either side
    # every wall has at most one threshold
    return [[float(a) if i > 0 else int(a) for i,a in enumerate(l.split(' '))]  for l in f.readlines()]

def parsevars(f):
    # Each line in f has the space separated quantities:
    # var number, ordered outputs, inputs, boolean domains, location of focal point for each domain
    # integer, list of integers, list of integers, list of boolean tuples, list of floats
    # the domains are 0.5, 1.5, etc - the average of the thresholds on either side
    S = [ast.literal_eval(t) for l in f.readlines() for t in l.split(' ')]
    return {'varnums':S[0::5], 'ordoutputs':S[1::5], 'inputs':S[2::5], 'booldomains':S[3::5], 'fplocations':S[4::5]}

def main(varfname,wallsfname):
    vardict = parsevars(varfname)
    walls = parsewalls(wallsfname)
    walls = removeboundaries(walls)

if __name__ == '__main__':
    vardict=parsevars(open('toyvarfile.txt'))
    vardict=booleantomanyvalues(vardict)
    for k,v in vardict.items():
        print k,v