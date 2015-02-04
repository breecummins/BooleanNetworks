import walllabels as WL
import preprocess as PP
import testcases as tc

def testme():
    test0()
    test1()
    test2()
    test3()

def test0():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test0())
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3, 8]
    print [inds[j] for j in WL.getFirstwalls('um',allwalllabels)]==[10]
    print [inds[j] for j in WL.getFirstwalls('ud',allwalllabels)]==[5]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['uu','um']
    print WL.isVarGTorLT(walldomains[inds.index(10)][0],[inds.index(5),inds.index(8)],walldomains,0)==(True,False)

def test1():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test1())
    print [inds[j] for j in WL.getFirstwalls('dd',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[8]
    print [inds[j] for j in WL.getFirstwalls('dM',allwalllabels)]==[11]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)])==['um']
    print WL.pathDependentStringConstruction(inds.index(13),inds.index(11),inds.index(10),walldomains,outedges,varsaffectedatwall[inds.index(11)])==['dM']    
    print WL.isVarGTorLT(walldomains[inds.index(11)][1],[inds.index(13)],walldomains,1)==(True,False)

def test2():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test2())
    print [inds[j] for j in WL.getFirstwalls('Mu',allwalllabels)]==[8,13] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(3),inds.index(5),inds.index(8),walldomains, outedges,varsaffectedatwall[inds.index(5)])==['um']
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)])==['dM']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['uu']    
    print WL.isVarGTorLT(walldomains[inds.index(5)][1],[inds.index(8),inds.index(10)],walldomains,1)==(False,True)

def test3():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test3())
    print [inds[j] for j in WL.getFirstwalls('Muu',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('ddm',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('uMd',allwalllabels)]==[3] 
    print [inds[j] for j in WL.getFirstwalls('dmu',allwalllabels)]==[9] 
    print WL.pathDependentStringConstruction(inds.index(0),inds.index(4),inds.index(9),walldomains, outedges,varsaffectedatwall[inds.index(4)])==['ddu','Mdu']
    print WL.pathDependentStringConstruction(inds.index(6),inds.index(3),inds.index(0),walldomains, outedges,varsaffectedatwall[inds.index(3)])==['udd','uMd']
    print WL.pathDependentStringConstruction(inds.index(9),inds.index(10),inds.index(6),walldomains,outedges,varsaffectedatwall[inds.index(10)])==['dud','duM']    
    print WL.pathDependentStringConstruction(inds.index(4),inds.index(9),inds.index(10),walldomains,outedges,varsaffectedatwall[inds.index(9)])==['duu','dmu']    
    # print WL.isVarGTorLT(walldomains[inds.index(0)][1],[inds.index(3)],walldomains,1)==(False,True)


if __name__=='__main__':
    testme()
