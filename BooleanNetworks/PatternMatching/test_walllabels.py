import walllabels as WL
import preprocess as PP
import testcases as tc

def testme():
    test0()
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()

def test0():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels= PP.filterAllTriples(*tc.test0())
    inedges=[[j for j,o in enumerate(outedges) if node in o] for node in range(len(outedges))]
    print [set(a) for a in allwalllabels]==[set(a) for a in [['md'],['ud'],['dd'],['md'],['um'],['dM'],['Mu']]]
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3, 8]
    print [inds[j] for j in WL.getFirstwalls('um',allwalllabels)]==[10]
    print [inds[j] for j in WL.getFirstwalls('ud',allwalllabels)]==[5]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)],inedges)==['um']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)],inedges)==['um']
    print WL.infoFromWalls(0,walldomains[inds.index(10)][0],[inds.index(5),inds.index(8)],2,walldomains)==(True,False)
    # print WL.isVarGTorLT(walldomains[inds.index(10)][0],[inds.index(5),inds.index(8)],walldomains,0)==(True,False)

def test1():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test1())
    inedges=[[j for j,o in enumerate(outedges) if node in o] for node in range(len(outedges))]
    print [set(a) for a in allwalllabels]==[set(a) for a in [['md'],['um'],['dM'],['Mu']]]
    print [inds[j] for j in WL.getFirstwalls('dd',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[8]
    print [inds[j] for j in WL.getFirstwalls('dM',allwalllabels)]==[11]
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(10),inds.index(13),walldomains, outedges,varsaffectedatwall[inds.index(10)],inedges)==['um']
    print WL.pathDependentStringConstruction(inds.index(13),inds.index(11),inds.index(10),walldomains,outedges,varsaffectedatwall[inds.index(11)],inedges)==['dM']    
    print WL.infoFromWalls(1,walldomains[inds.index(11)][1],[inds.index(13)],2,walldomains)==(True,False)

def test2():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test2())
    inedges=[[j for j,o in enumerate(outedges) if node in o] for node in range(len(outedges))]
    print [set(a) for a in allwalllabels]==[set(a) for a in [['md'],['um'],['dM'],['Mu'],['uu'],['du'],['Mu']]]
    print [inds[j] for j in WL.getFirstwalls('Mu',allwalllabels)]==[8,13] 
    print [inds[j] for j in WL.getFirstwalls('md',allwalllabels)]==[3]
    print [inds[j] for j in WL.getFirstwalls('uM',allwalllabels)]==[]
    print WL.pathDependentStringConstruction(inds.index(3),inds.index(5),inds.index(8),walldomains, outedges,varsaffectedatwall[inds.index(5)],inedges)==['um']
    print WL.pathDependentStringConstruction(inds.index(8),inds.index(6),inds.index(3),walldomains,outedges,varsaffectedatwall[inds.index(6)],inedges)==['dM']
    print WL.pathDependentStringConstruction(inds.index(5),inds.index(10),inds.index(13),walldomains,outedges,varsaffectedatwall[inds.index(10)],inedges)==['uu']    
    print WL.infoFromWalls(1,walldomains[inds.index(5)][1],[inds.index(8),inds.index(10)],2,walldomains)==(False,True)

def test3():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test3())
    inedges=[[j for j,o in enumerate(outedges) if node in o] for node in range(len(outedges))]
    print [set(a) for a in allwalllabels]==[set(a) for a in [['udm','udu'],['uMd','udd'],['ddu','Mdu'],['uud','mud'],['duu','dmu'],['dud','duM']]]
    print [inds[j] for j in WL.getFirstwalls('Muu',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('ddm',allwalllabels)]==[] 
    print [inds[j] for j in WL.getFirstwalls('uMd',allwalllabels)]==[3] 
    print [inds[j] for j in WL.getFirstwalls('dmu',allwalllabels)]==[9] 
    print WL.pathDependentStringConstruction(inds.index(0),inds.index(4),inds.index(9),walldomains, outedges,varsaffectedatwall[inds.index(4)],inedges)==['ddu','Mdu']
    print WL.pathDependentStringConstruction(inds.index(6),inds.index(3),inds.index(0),walldomains, outedges,varsaffectedatwall[inds.index(3)],inedges)==['udd','uMd']
    print WL.pathDependentStringConstruction(inds.index(9),inds.index(10),inds.index(6),walldomains,outedges,varsaffectedatwall[inds.index(10)],inedges)==['dud','duM']    
    print WL.pathDependentStringConstruction(inds.index(4),inds.index(9),inds.index(10),walldomains,outedges,varsaffectedatwall[inds.index(9)],inedges)==['duu','dmu']    
    print WL.infoFromWalls(1,walldomains[inds.index(0)][1],[inds.index(3)],2,walldomains)==(False,True)

def test4():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test4())
    inedges=[[j for j,o in enumerate(outedges) if node in o] for node in range(len(outedges))]
    print [set(a) for a in allwalllabels]==[set(a) for a in [['ud'],['md'],['um'],['um'],['dM'],['uu'],['Mu']]]
    print [inds[j] for j in WL.getFirstwalls('um',allwalllabels)]==[7,8]
    print [inds[j] for j in WL.getFirstwalls('dd',allwalllabels)]==[] 
    print WL.pathDependentStringConstruction(inds.index(9),inds.index(6),inds.index(8),walldomains, outedges,varsaffectedatwall[inds.index(6)],inedges)==['md']
    print WL.pathDependentStringConstruction(inds.index(9),inds.index(6),inds.index(5),walldomains, outedges,varsaffectedatwall[inds.index(6)],inedges)==['md']
    print WL.pathDependentStringConstruction(inds.index(10),inds.index(11),inds.index(9),walldomains, outedges,varsaffectedatwall[inds.index(11)],inedges)==['Mu']

def test5():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test5())
    mylist=[['mdd','udd','Mdd','ddd'],['ddM','ddd'],['dMu','ddu'],['mdd','udd'],['mdd','udd'],['Muu','duu'],['udd'],['umd'],['umd'],['uuu','uud'],['uuu','uum']]
    print [set(a) for a in allwalllabels]==[set(a) for a in mylist]
    print WL.getFirstwalls('mdd',allwalllabels)==[0,3,4]
    print WL.getFirstwalls('umd',allwalllabels)==[7,8]

def test6():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test6())
    mylist=[['umu'],['umd'],['dMd','dud'],['uuu'],['uum'],['duu'],['duM'],['udd','udm'],['uuM'],['duM'],['uuu'],['duu'],['mdd'],['Muu'],['mud'],['Muu'],['Muu']]
    print [set(a) for a in allwalllabels]==[set(a) for a in mylist]

if __name__=='__main__':
    testme()
