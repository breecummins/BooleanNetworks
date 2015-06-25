import json

def parseOutEdges(fname='outEdges.txt'):
    f=open(fname,'r')
    outedges=[]
    for l in f:
        outedges.append(tuple([int(i) for i in l.split(' ')[1:-1]]))
    return outedges

def parseWalls(fname='walls.txt'):
    f=open(fname,'r')
    walldomains=[]
    varatthresh=[]
    for l in f:
        L = filter(None,l.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' ')[1:-1])
        varatthresh.append(int(L[0]))
        L = [float(n) for n in L[1:]]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2) # thresholds are integers, regular domains end in .5
        walldomains.append(tuple(T))
    return walldomains,varatthresh

def parseVars(fname="variables.txt"):
    # this parser depends on the file being small enough to fit in memory
    f=open(fname,'r')
    R=f.read().split()
    return R[1::2]  

def parseEqns(fname="equations.txt"):
    f=open(fname,'r')
    threshvars=[]
    for l in f:
        L=l.split(':')
        threshvars.append(tuple([L[0].replace(' ',''),L[2].split()]))
    return threshvars

def parsePatterns(fname="patterns.txt"):
    f=open(fname,'r')
    Maxmin=[]
    varnames=[]
    for l in f:
        L=l.replace(',',' ').split()
        varnames.append(L[::2])
        Maxmin.append(L[1::2])
    return varnames, Maxmin

def parsePatternGenerator(fname="patterngenerator.txt"):
    f=open(fname,'r')
    patternstart=[p.strip() for p in f.readline().split(',')]
    patternremainder=[p.strip() for p in f.readline().split(',')]
    return patternstart, patternremainder

def parseAll(oname='outEdges.txt',wname='walls.txt',vname="variables.txt",ename="equations.txt",pname="patterns.txt"):
    return parseOutEdges(oname), parseWalls(wname), parseVars(vname), parseEqns(ename), parsePatterns(pname)

def parseAllNoPattern(oname='outEdges.txt',wname='walls.txt',vname="variables.txt",ename="equations.txt"):
    return parseOutEdges(oname), parseWalls(wname), parseVars(vname), parseEqns(ename)

def parseJSON(fname='output.json'):
    json_data = open(fname)
    data = json.load(json_data,strict=False)
    # parameters
    parameterinds=data['parameters']['index']
    # variables
    varnames=[str(v) for v in data["variables"]["info"]]
    # unsorted outedges
    wallindslist=[[int(k) for k in item[0].keys()] for item in data['outedges']['data']]
    outedgeslist=[ [L for L in item[0].values()] for item in data['outedges']['data']]
    # sorted outedges
    sortedinds=[ sorted(zip(w,range(len(w)))) for w in wallindslist ]
    wallindslist=[ [x for (x,y) in s] for s in sortedinds ]
    outedgeslist=[ [tuple(o[y]) for (x,y) in s] for o,s in zip(outedgeslist,sortedinds)] 
    # unsorted unsplit walls
    wallnameslist=[int(item) for item in data['walls']['info'].keys()]
    wallinfolist=data['walls']['info'].values()
    # sorted unsplit walls
    sortedinds=sorted(zip(wallnameslist,range(len(wallnameslist))))
    wallnameslist,inds=zip(*sortedinds)
    walldomainslist1=[]
    varatthreshlist1=[]
    for i in inds:
        w=wallinfolist[i]
        L = filter(None,w.replace('[',' ').replace('x',' ').replace(']',' ').replace(',',' ').split(' '))
        varatthreshlist1.append(int(L[0]))
        L = [float(n) for n in L[1:]]
        T = []
        for k in range(0,len(L)-1,2):
            T.append(sum(L[k:k+2])/2) # thresholds are integers, regular domains end in .5
        walldomainslist1.append(tuple(T))
    # sorted split walls
    walldomainslist=[[] for _ in range(len(wallindslist))]
    varatthreshlist=[[] for _ in range(len(wallindslist))]
    for j,wn in enumerate(wallnameslist):
        for k,w in enumerate(wallindslist):
            if wn in w:
                walldomainslist[k].append(walldomainslist1[j])
                varatthreshlist[k].append(varatthreshlist1[j])
    return varnames,wallindslist,outedgeslist,walldomainslist,varatthreshlist,parameterinds

def parseNewJSONFormat(fname='dsgrn_output.json'):
    parsed = json.loads(fname)
    N = len(parsed["network"])
    varnames = [ x[0] for x in parsed["network"] ]
    threshord = [ [parsed["network"][i][2][j] for j in parsed["parameter"][i][2]] for i in range(N) ]
    graph = parsed["graph"]
    cells = parsed["cells"]

if __name__=='__main__':
    # print parseVars("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt")
    # print parsePatterns()
    # print parseEqns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/equations.txt")
    parseJSON()