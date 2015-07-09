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
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('md',wallinfo['triples'],wallinfo['walllabels']))==set([(0,1),(3,4)])    
    print set(wl.getFirstAndNextWalls('um',wallinfo['triples'],wallinfo['walllabels']))==set([(4,6)])    
    print set(wl.getFirstAndNextWalls('ud',wallinfo['triples'],wallinfo['walllabels']))==set([(1,4)])    
    print set(wl.getFirstAndNextWalls('uM',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print wl.pathDependentLabelConstruction(3,4,6,walldomains, outedges,varsaffectedatwall[4],inedges)==['um']
    print wl.pathDependentLabelConstruction(1,4,6,walldomains,outedges,varsaffectedatwall[4],inedges)==['um']
    print wl.infoFromWalls(0,walldomains[4][0],[1,3],2,walldomains)==(True,False)

def test1():
    outedges,walldomains,varsaffectedatwall=tc.test1()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('dd',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print set(wl.getFirstAndNextWalls('md',wallinfo['triples'],wallinfo['walllabels']))==set([(0,1)])    
    print set(wl.getFirstAndNextWalls('dM',wallinfo['triples'],wallinfo['walllabels']))==set([(2,0)])    
    print wl.pathDependentLabelConstruction(0,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['um']
    print wl.pathDependentLabelConstruction(3,2,1,walldomains,outedges,varsaffectedatwall[2],inedges)==['dM']    
    print wl.infoFromWalls(1,walldomains[2][1],[3],2,walldomains)==(True,False)

def test2():
    outedges,walldomains,varsaffectedatwall=tc.test2()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('Mu',wallinfo['triples'],wallinfo['walllabels']))==set([(3,2),(6,5)])    
    print set(wl.getFirstAndNextWalls('md',wallinfo['triples'],wallinfo['walllabels']))==set([(0,1)])    
    print set(wl.getFirstAndNextWalls('uM',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print wl.pathDependentLabelConstruction(0,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['um']
    print wl.pathDependentLabelConstruction(3,2,0,walldomains,outedges,varsaffectedatwall[2],inedges)==['dM']
    print wl.pathDependentLabelConstruction(1,4,6,walldomains,outedges,varsaffectedatwall[4],inedges)==['uu']    
    print wl.infoFromWalls(1,walldomains[1][1],[3,4],2,walldomains)==(False,True)

def test3():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('Muu',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print set(wl.getFirstAndNextWalls('ddm',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print set(wl.getFirstAndNextWalls('uMd',wallinfo['triples'],wallinfo['walllabels']))==set([(1,0)])    
    print set(wl.getFirstAndNextWalls('dmu',wallinfo['triples'],wallinfo['walllabels']))==set([(4,5)])    
    print wl.pathDependentLabelConstruction(0,2,4,walldomains, outedges,varsaffectedatwall[2],inedges)==['ddu','Mdu']
    print wl.pathDependentLabelConstruction(3,1,0,walldomains, outedges,varsaffectedatwall[1],inedges)==['udd','uMd']
    print wl.pathDependentLabelConstruction(4,5,3,walldomains,outedges,varsaffectedatwall[5],inedges)==['dud','duM']    
    print wl.pathDependentLabelConstruction(2,4,5,walldomains,outedges,varsaffectedatwall[4],inedges)==['duu','dmu']    
    print wl.infoFromWalls(1,walldomains[0][1],[1],2,walldomains)==(False,True)

def test4():
    outedges,walldomains,varsaffectedatwall=tc.test4()
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('um',wallinfo['triples'],wallinfo['walllabels']))==set([(2,5),(3,6)])    
    print set(wl.getFirstAndNextWalls('dd',wallinfo['triples'],wallinfo['walllabels']))==set([])    
    print wl.pathDependentLabelConstruction(4,1,3,walldomains, outedges,varsaffectedatwall[1],inedges)==['md']
    print wl.pathDependentLabelConstruction(4,1,0,walldomains, outedges,varsaffectedatwall[1],inedges)==['md']
    print wl.pathDependentLabelConstruction(5,6,4,walldomains, outedges,varsaffectedatwall[6],inedges)==['Mu']

def test5():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wl.getFirstAndNextWalls('mdd',wallinfo['triples'],wallinfo['walllabels']))==set([(0,3),(3,7),(4,8),(4,6)])
    print set(wl.getFirstAndNextWalls('umd',wallinfo['triples'],wallinfo['walllabels']))==set([(7,9),(8,10)])

def test6():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)

if __name__=='__main__':
    testme()
