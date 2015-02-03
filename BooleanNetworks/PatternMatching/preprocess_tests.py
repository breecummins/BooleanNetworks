import prepatternmatch as pp
import testcases as tc

def testme():
    walldomains,outedges,varsaffectedatwall=tc.test0()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (4,), (0,), (4,), (6,), (2, 3), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 0, 0, 0, 1, 1, 0]

    walldomains,outedges,varsaffectedatwall=tc.test1()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print inds==[3, 6, 8, 10, 11, 13]
    print outedges==[(), (0,), (3,), (5,), (1, 2), (4,)]
    print walldomains==[(0.5, 1), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 0, 0, 1, 1, 0]

    walldomains,outedges,varsaffectedatwall=tc.test2()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (3,4), (0,), (2,), (6,), (2,), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 1, 1, 0, 0, 0, 0]

if __name__=='__main__':
	testme()
