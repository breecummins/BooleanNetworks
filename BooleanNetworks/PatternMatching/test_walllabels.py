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
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print wallinfo[(3,4)]==[(6,('um',))]
    print wallinfo[(1,4)]==[(6,('um',))]
    print set(wallinfo[(6,5)])==set([(2,('dM',)),(3,('dM',))])
    print wl.infoFromWalls(0,walldomains[4][0],[1,3],walldomains)==(True,False)

def test1():
    outedges,walldomains,varsaffectedatwall=tc.test1()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print wallinfo[(0,1)]==[(3,('um',))]
    print wallinfo[(1,3)]==[(2,('Mu',))]
    print wallinfo[(3,2)]==[(0,('dM',))]
    print wallinfo[(2,0)]==[(1,('md',))]
    print wl.infoFromWalls(1,walldomains[2][1],[3],walldomains)==(True,False)

def test2():
    outedges,walldomains,varsaffectedatwall=tc.test2()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(0,1)])==set([(3,('um',)),(4,('um',))])
    print wallinfo[(3,2)]==[(0,('dM',))]
    print wallinfo[(1,4)]==[(6,('uu',))]
    print wl.infoFromWalls(1,walldomains[1][1],[3,4],walldomains)==(False,True)

def test3():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(0,2)][0][1])==set(('ddu','Mdu'))
    print set(wallinfo[(3,1)][0][1])==set(('udd','uMd'))
    print set(wallinfo[(4,5)][0][1])==set(('dud','duM'))
    print set(wallinfo[(2,4)][0][1])==set(('duu','dmu'))
    print wl.infoFromWalls(1,walldomains[0][1],[1],walldomains)==(False,True)

def test4():
    outedges,walldomains,varsaffectedatwall=tc.test4()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(4,1)])==set([(0,('md',)),(3,('md',))])
    print wallinfo[(5,6)]==[(4,('Mu',))]
    print wallinfo[(3,6)]==[(4,('Mu',))]

def test5():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(1,0)][0][1])==set(('ddd','mdd','udd','Mdd'))
    print set( [ wallinfo[(2,1)][k][0] for k in [0,1] ]  )==set([0,4])
    print set( wallinfo[(2,1)][0][1]  )==set(('ddd','ddM'))
    print set( wallinfo[(2,1)][1][1]  )==set(('ddd','ddM'))
    print set(wallinfo[(1,4)])==set([(6,('mdd','udd')),(8,('mdd','udd'))])

def test6():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(7,0)])==set([(3,('umu',)),(8,('umu',)),(13,('umu',))])
    print set(wallinfo[(3,15)])==set([(5,('Muu',)),(11,('Muu',))])
    print wallinfo[(4,16)]==[(6,('Muu',))]
    print wallinfo[(10,16)]==[(6,('Muu',))]
    print wallinfo[(0,13)]==[(9,('Muu',))]


if __name__=='__main__':
    testme()
