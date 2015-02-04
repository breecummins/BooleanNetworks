import walllabels as WL
import preprocess as PP
import testcases as tc

def testme():
    test0()
    test1()
    test2()
    test3()

def preprocess((walldomains,outedges,varsaffectedatwall)):
    # filter out walls not involved in cycles and create wall labels for the filtered walls
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(outedges,walldomains,varsaffectedatwall)
    return inds,outedges,walldomains,varsaffectedatwall,allwalllabels


def test0():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels=preprocess(tc.test0())
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3, 8]
    print [inds[j] for j in WL.getFirstwalls('um',allwalllabels)]==[10]
    print [inds[j] for j in WL.getFirstwalls('ud',allwalllabels)]==[3,5]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]#==[5]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.isVarGTorLT(walldomains[inds.index(10)][0],[inds.index(5),inds.index(8)],walldomains,0)==(True,False)

def test1():
    walldomains,outedges,varsaffectedatwall=tc.test1()
    inds,outedges,walldomains,varsaffectedatwall=ppm.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('dd',allwalllabels)]==[6] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[8]
    print [inds[j] for j in WL.getFirstwalls('Md',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(11),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)])==['dd']
    print WL.pathDependentStringConstruction(inds.index(13),inds.index(11),inds.index(6),walldomains,outedges,varsaffectedatwall[inds.index(11)])==['dM']    
    print WL.isVarGTorLT(walldomains[inds.index(11)][1],[inds.index(13)],walldomains,1)==(True,False)

def test2():
    walldomains,outedges,varsaffectedatwall=tc.test2()
    inds,outedges,walldomains,varsaffectedatwall=ppm.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('Mu',allwalllabels)]==[8,13] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(3),inds.index(5),inds.index(8),walldomains, outedges,varsaffectedatwall[inds.index(5)])==['um']
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)])==['dM']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['uu']    
    print WL.isVarGTorLT(walldomains[inds.index(5)][1],[inds.index(8),inds.index(10)],walldomains,1)==(False,True)

def test3():
    walldomains,outedges,varsaffectedatwall,varnames=tc.test3()
    inds,outedges,walldomains,varsaffectedatwall=ppm.filterBoundaryWallsSteadyStatesWhiteWalls(outedges,walldomains,varsaffectedatwall)
    print [inds[j] for j in WL.getFirstwalls('Muu',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('ddm',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('uMd',allwalllabels)]==[3] 
    print [inds[j] for j in WL.getFirstwalls('dmu',allwalllabels)]==[9] 
    print WL.pathDependentStringConstruction(inds.index(0),inds.index(4),inds.index(9),walldomains, outedges,varsaffectedatwall[inds.index(4)])==['Mdu']
    print WL.pathDependentStringConstruction(inds.index(6),inds.index(3),inds.index(0),walldomains, outedges,varsaffectedatwall[inds.index(3)])#==['uMd']
    print WL.pathDependentStringConstruction(inds.index(9),inds.index(10),inds.index(6),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['duM']    
    print WL.isVarGTorLT(walldomains[inds.index(0)][1],[inds.index(3)],walldomains,1)==(False,True)


if __name__=='__main__':
    walldomains,outedges,varsaffectedatwall = tc.test3()
    walldomains,outedges,varsaffectedatwall = walldomains[:12],outedges[:12],varsaffectedatwall[:12]
    allwalllabels=WL.makeAllWallLabels(outedges,walldomains,varsaffectedatwall)
    print allwalllabels
    print WL.pathDependentStringConstruction(7,0,4,walldomains, outedges,varsaffectedatwall[0])
    # inds,outedges,walldomains,varsaffectedatwall,allwalllabels=preprocess(tc.test3())
    # print inds 
    # print [tuple([inds[j] for j in o]) for o in outedges]
    # print allwalllabels
