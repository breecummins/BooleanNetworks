import makewalllabels as mwl
import prepforpatternmatch as pp

def testme():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED

    # EXAMPLE 0, NO STEADY STATES
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    varsaffectedatwall=[-1]*len(outedges)
    varsaffectedatwall[3]=0
    varsaffectedatwall[8]=0
    varsaffectedatwall[13]=0
    varsaffectedatwall[10]=1
    varsaffectedatwall[11]=1
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsAndSteadyStates(outedges,walldomains,varsaffectedatwall)
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (4,), (0,), (4,), (6,), (2, 3), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, -1, -1, 0, 1, 1, 0]
    print [inds[j] for j in mwl.getFirstwalls('md',outedges,walldomains,varsaffectedatwall)]==[3, 8]
    print mwl.pathDependentStringConstruction2(inds.index(8),inds.index(10),inds.index(13),walldomains,varsaffectedatwall[inds.index(10)])==['um']

    # # EXAMPLE 1, HAS STEADY STATE
    # walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5),(0.5,0.5)]
    # outedges=[(17,),(3,),(17,),(17,),(3,),(10,17),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,),(17,)]

    # pattern=['Md'] # this label only exists because of entrance from boundary
    # match=matchPattern(pattern,walldomains,outedges,suppresscycleinfo=1)
    # print match==[(3,)]

    # pattern=['md','um','Mu','dM','md']
    # match=matchPattern(pattern,walldomains,outedges,suppresscycleinfo=1)
    # print match==[(8, 10, 13, 11, 8)] # acyclic path (8,10,13,11,6,3) exists but should be weeded out

    # pattern=['md','um','Mu','dM','md']
    # match=matchPattern(pattern,walldomains,outedges,suppresscycleinfo=1,cycliconly=0)
    # print match==[(8, 10, 13, 11, 8),(8,10,13,11,6,3)] # now acyclic path should be returned

    # pattern=['md','um','Mu','dM','Md'] # even though wall 3 can be 'Md', this comes from the boundary, so search should fail
    # match=matchPattern(pattern,walldomains,outedges,suppresscycleinfo=1)
    # print 'None' in match 

    # pattern=['md','Mu','dM','md'] # even though wall 10 can be 'uu', this comes from wall 5, so search should fail
    # match=matchPattern(pattern,walldomains,outedges,suppresscycleinfo=1)
    # print 'None' in match


if __name__=='__main__':
	testme()
