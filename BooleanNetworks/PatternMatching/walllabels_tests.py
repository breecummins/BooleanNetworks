import walllabels as WL
import prepatternmatch as pp
import testcases as tc

def testme():
    walldomains,outedges,varsaffectedatwall=tc.test0()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('md',outedges,walldomains,varsaffectedatwall)]==[3, 8]
    print [inds[j] for j in WL.getFirstwalls('um',outedges,walldomains,varsaffectedatwall)]==[10]
    print [inds[j] for j in WL.getFirstwalls('ud',outedges,walldomains,varsaffectedatwall)]==[5]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.isVarGTorLT(walldomains[inds.index(10)][0],[inds.index(5),inds.index(8)],walldomains,0)==(True,False)

    walldomains,outedges,varsaffectedatwall=tc.test1()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('dd',outedges,walldomains,varsaffectedatwall)]==[6] 
    print [inds[j] for j in WL.getFirstwalls('md',outedges,walldomains,varsaffectedatwall)]==[8]
    print [inds[j] for j in WL.getFirstwalls('Md',outedges,walldomains,varsaffectedatwall)]==[]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(11),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)])==['dd']
    print WL.pathDependentStringConstruction(inds.index(13),inds.index(11),inds.index(6),walldomains,outedges,varsaffectedatwall[inds.index(11)])==['dM']    
    print WL.isVarGTorLT(walldomains[inds.index(11)][1],[inds.index(13)],walldomains,1)==(True,False)

    walldomains,outedges,varsaffectedatwall=tc.test2()
    inds,outedges,walldomains,varsaffectedatwall=pp.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('Mu',outedges,walldomains,varsaffectedatwall)]==[8,13] 
    print [inds[j] for j in WL.getFirstwalls('md',outedges,walldomains,varsaffectedatwall)]==[3]
    print [inds[j] for j in WL.getFirstwalls('uM',outedges,walldomains,varsaffectedatwall)]==[]
    print WL.pathDependentStringConstruction(inds.index(3),inds.index(5),inds.index(8),walldomains, outedges,varsaffectedatwall[inds.index(5)])==['um']
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)])==['dM']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['uu']    
    print WL.isVarGTorLT(walldomains[inds.index(5)][1],[inds.index(8),inds.index(10)],walldomains,1)==(False,True)


if __name__=='__main__':
	testme()
