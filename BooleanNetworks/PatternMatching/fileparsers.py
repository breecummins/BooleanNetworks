import json

def parsePatterns(fname="patterns.txt"):
    f=open(fname,'r')
    Maxmin=[]
    varnames=[]
    for l in f:
        L=l.replace(',',' ').split()
        varnames.append(L[::2])
        Maxmin.append(L[1::2])
    return varnames, Maxmin

def parseJSONFormat(fname='dsgrn_output.json'):
    parsed = json.load(open(fname),strict=False)
    varnames = [ x[0] for x in parsed["network"] ]
    threshnames = [ [parsed["network"][i][2][j] for j in parsed["parameter"][i][2]] for i in range(len(parsed["network"])) ]
    return varnames,threshnames,parsed["graph"],parsed["cells"]

if __name__=='__main__':
    # print parseVars("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/variables.txt")
    # print parsePatterns()
    # print parseEqns("/Users/bcummins/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/equations.txt")
    parseJSON()