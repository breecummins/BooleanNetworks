import walllabels as wl
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
    outedges,walldomains,varsaffectedatwall=tc.test0()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in [['md'],['ud'],['dd'],['md'],['um'],['dM'],['Mu']]]
    print set(wl.getFirstAndNextWalls('md',paramDict['triples'],paramDict['walllabels_previous']))==set([(0,1),(3,4)])    
    print set(wl.getFirstAndNextWalls('um',paramDict['triples'],paramDict['walllabels_previous']))==set([(4,6)])    
    print set(wl.getFirstAndNextWalls('ud',paramDict['triples'],paramDict['walllabels_previous']))==set([(1,4)])    
    print set(wl.getFirstAndNextWalls('uM',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print wl.pathDependentStringConstruction(3,4,6,walldomains, outedges,varsaffectedatwall[4],inedges)==['um']
    print wl.pathDependentStringConstruction(1,4,6,walldomains,outedges,varsaffectedatwall[4],inedges)==['um']
    print wl.infoFromWalls(0,walldomains[4][0],[1,3],2,walldomains)==(True,False)

def test1():
    outedges,walldomains,varsaffectedatwall=tc.test1()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in [['md'],['um'],['dM'],['Mu']]]
    print set(wl.getFirstAndNextWalls('dd',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print set(wl.getFirstAndNextWalls('md',paramDict['triples'],paramDict['walllabels_previous']))==set([(0,1)])    
    print set(wl.getFirstAndNextWalls('dM',paramDict['triples'],paramDict['walllabels_previous']))==set([(2,0)])    
    print wl.pathDependentStringConstruction(0,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['um']
    print wl.pathDependentStringConstruction(3,2,1,walldomains,outedges,varsaffectedatwall[2],inedges)==['dM']    
    print wl.infoFromWalls(1,walldomains[2][1],[3],2,walldomains)==(True,False)

def test2():
    outedges,walldomains,varsaffectedatwall=tc.test2()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in [['md'],['um'],['dM'],['Mu'],['uu'],['du'],['Mu']]]
    print set(wl.getFirstAndNextWalls('Mu',paramDict['triples'],paramDict['walllabels_previous']))==set([(3,2),(6,5)])    
    print set(wl.getFirstAndNextWalls('md',paramDict['triples'],paramDict['walllabels_previous']))==set([(0,1)])    
    print set(wl.getFirstAndNextWalls('uM',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print wl.pathDependentStringConstruction(0,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['um']
    print wl.pathDependentStringConstruction(3,2,0,walldomains,outedges,varsaffectedatwall[2],inedges)==['dM']
    print wl.pathDependentStringConstruction(1,4,6,walldomains,outedges,varsaffectedatwall[4],inedges)==['uu']    
    print wl.infoFromWalls(1,walldomains[1][1],[3,4],2,walldomains)==(False,True)

def test3():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in [['udm','udu'],['uMd','udd'],['ddu','Mdu'],['uud','mud'],['duu','dmu'],['dud','duM']]]
    print set(wl.getFirstAndNextWalls('Muu',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print set(wl.getFirstAndNextWalls('ddm',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print set(wl.getFirstAndNextWalls('uMd',paramDict['triples'],paramDict['walllabels_previous']))==set([(1,0)])    
    print set(wl.getFirstAndNextWalls('dmu',paramDict['triples'],paramDict['walllabels_previous']))==set([(4,5)])    
    print wl.pathDependentStringConstruction(0,2,4,walldomains, outedges,varsaffectedatwall[2],inedges)==['ddu','Mdu']
    print wl.pathDependentStringConstruction(3,1,0,walldomains, outedges,varsaffectedatwall[1],inedges)==['udd','uMd']
    print wl.pathDependentStringConstruction(4,5,3,walldomains,outedges,varsaffectedatwall[5],inedges)==['dud','duM']    
    print wl.pathDependentStringConstruction(2,4,5,walldomains,outedges,varsaffectedatwall[4],inedges)==['duu','dmu']    
    print wl.infoFromWalls(1,walldomains[0][1],[1],2,walldomains)==(False,True)

def test4():
    outedges,walldomains,varsaffectedatwall=tc.test4()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in [['ud'],['md'],['um'],['um'],['dM'],['uu'],['Mu']]]
    print set(wl.getFirstAndNextWalls('um',paramDict['triples'],paramDict['walllabels_previous']))==set([(2,5),(3,6)])    
    print set(wl.getFirstAndNextWalls('dd',paramDict['triples'],paramDict['walllabels_previous']))==set([])    
    print wl.pathDependentStringConstruction(4,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['md']
    print wl.pathDependentStringConstruction(4,1,0,walldomains, outedges,varsaffectedatwall[1],inedges)==['md']
    print wl.pathDependentStringConstruction(5,6,4,walldomains, outedges,varsaffectedatwall[6],inedges)==['Mu']

def test5():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    mylist=[['mdd','udd','Mdd','ddd'],['ddM','ddd'],['dMu','ddu'],['mdd','udd'],['mdd','udd'],['Muu','duu'],['udd'],['umd'],['umd'],['uuu','uud'],['uuu','uum']]
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in mylist]
    print set(wl.getFirstAndNextWalls('mdd',paramDict['triples'],paramDict['walllabels_previous']))==set([(0,3),(3,7),(4,8),(4,6)])
    print set(wl.getFirstAndNextWalls('umd',paramDict['triples'],paramDict['walllabels_previous']))==set([(7,9),(8,10)])

def test6():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    paramDict = wl.makeAllTriples(outedges,walldomains,varsaffectedatwall)
    mylist=[['umu'],['umd'],['dMd','dud'],['uuu'],['uum'],['duu'],['duM'],['udd','udm'],['uuM'],['duM'],['uuu'],['duu'],['mdd'],['Muu'],['mud'],['Muu'],['Muu']]
    print [set(a) for a in paramDict['walllabels_current']]==[set(a) for a in mylist]

if __name__=='__main__':
    testme()
