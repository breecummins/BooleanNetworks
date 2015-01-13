from patternmatch2 import matchPattern, pathDependentStringConstruction
import itertools

def testme():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED

    # EXAMPLE 0
    outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    R=range(len(outedges))
    inedges=[tuple([j for j,o in enumerate(outedges) if i in o ]) for i in R]
    for k in R:
        ie=inedges[k]
        oe=outedges[k]
        wl=[]
        for i,o in itertools.product(ie,oe):
            wl.extend(pathDependentStringConstruction(i,k,o,walldomains,outedges))
        print ie
        print oe
        print(list(set(wl)))

    # pattern=[]
    # match = matchPattern(pattern,walldomains,outedges,suppress=1)
    # print match==[(0,4,5,6,0)]


if __name__=='__main__':
	testme()
