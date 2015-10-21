# The MIT License (MIT)

# Copyright (c) 2015 Breschine Cummins

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import walllabels as wl
import preprocess as pp
import testcases as tc

def testme():
    test0()
    test1()
    test2()
    test3()
    test4()
    # test5()
    # test6()

def test0():
    outedges,walldomains,varsaffectedatwall=tc.test0()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print wallinfo[(3,4)]==[(6,('um',))]
    print wallinfo[(1,4)]==[(6,('um',))]
    print wallinfo[(2,0)]==[(1,('md',))]
    print set(wallinfo[(6,5)])==set([(2,('dM',)),(3,('dM',))])
    # print wl.infoFromWalls(0,walldomains[4][0],[1,3],walldomains)==(True,False)

def test1():
    outedges,walldomains,varsaffectedatwall=tc.test1()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print wallinfo[(0,1)]==[(3,('um',))]
    print wallinfo[(1,3)]==[(2,('Mu',))]
    print wallinfo[(3,2)]==[(0,('dM',))]
    print wallinfo[(2,0)]==[(1,('md',))]
    # print wl.infoFromWalls(1,walldomains[2][1],[3],walldomains)==(True,False)

def test2():
    outedges,walldomains,varsaffectedatwall=tc.test2()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(0,1)])==set([(3,('um',)),(4,('um',))])
    print wallinfo[(3,2)]==[(0,('dM',))]
    print wallinfo[(5,2)]==[(0,('dM',))]
    print wallinfo[(1,4)]==[(6,('uu',))]
    # print wl.infoFromWalls(1,walldomains[1][1],[3,4],walldomains)==(False,True)

def test3():
    domaingraph,domaincells,morseset,vertexmap,outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    extendedmorsegraph,extendedmorsecells=pp.makeExtendedMorseSetDomainGraph(vertexmap,morseset,domaingraph,domaincells)
    newoutedges,wallthresh,newwalldomains,booleanoutedges=pp.makeWallGraphFromDomainGraph(len(vertexmap),extendedmorsegraph, extendedmorsecells)
    newvarsaffectedatwall=pp.varsAtWalls(threshnames,newwalldomains,wallthresh,varnames)
    wallinfo = wl.makeWallInfo(newoutedges,newwalldomains,newvarsaffectedatwall)
    wallinfo = pp.truncateExtendedWallGraph(booleanoutedges,newoutedges,wallinfo)
    print set(wallinfo.keys())==set([(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)])
    print wallinfo[(0,1)]==[(2,('dmu',))]   
    print wallinfo[(1,2)]==[(3,('duM',))]   
    print wallinfo[(2,3)]==[(4,('mud',))]   
    print wallinfo[(3,4)]==[(5,('uMd',))]   
    print wallinfo[(4,5)]==[(0,('udm',))]   
    print wallinfo[(5,0)]==[(1,('Mdu',))]   

def test4():
    domaingraph,domaincells,morseset,vertexmap,outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test4()
    extendedmorsegraph,extendedmorsecells=pp.makeExtendedMorseSetDomainGraph(vertexmap,morseset,domaingraph,domaincells)
    newoutedges,wallthresh,newwalldomains,booleanoutedges=pp.makeWallGraphFromDomainGraph(len(vertexmap),extendedmorsegraph, extendedmorsecells)
    newvarsaffectedatwall=pp.varsAtWalls(threshnames,newwalldomains,wallthresh,varnames)
    wallinfo = wl.makeWallInfo(newoutedges,newwalldomains,newvarsaffectedatwall)
    wallinfo = pp.truncateExtendedWallGraph(booleanoutedges,newoutedges,wallinfo)
    print set(wallinfo.keys())==set([(0,1),(0,2),(1,3),(2,5),(3,6),(4,0),(5,4),(6,5)])
    print wallinfo[(0,1)]==[(3,('ud',))]
    print wallinfo[(0,2)]==[(5,('um',))]
    print wallinfo[(1,3)]==[(6,('um',))]
    print wallinfo[(2,5)]==[(4,('Mu',))]
    print wallinfo[(3,6)]==[(5,('uu',))]
    print set(wallinfo[(4,0)])==set([(1,('md',)),(2,('md',))])
    print wallinfo[(5,4)]==[(0,('dM',))]
    print wallinfo[(6,5)]==[(4,('Mu',))]

def test5():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(1,0)][0][1])==set(('ddd','mdd','udd','Mdd'))
    print set( [ wallinfo[(2,1)][k][0] for k in [0,1] ]  )==set([0,4])
    print set( wallinfo[(2,1)][0][1]  )==set(('ddd','ddM'))
    print set( wallinfo[(2,1)][1][1]  )==set(('ddd','ddM'))
    print set(wallinfo[(1,4)])==set([(6,('udd','mdd')),(8,('udd','mdd'))])

def test6():
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    wallinfo = wl.makeWallInfo(outedges,walldomains,varsaffectedatwall)
    print set(wallinfo[(7,0)])==set([(3,('umu',)),(8,('umu',)),(13,('umu',))])
    print set(wallinfo[(3,15)])==set([(5,('Muu',)),(11,('Muu',))])
    print wallinfo[(4,16)]==[(6,('Muu',))]
    print wallinfo[(10,16)]==[(6,('Muu',))]
    print wallinfo[(6,2)]==[(12,('dud','dMd'))]
    print wallinfo[(0,3)]#==[(10,('uuu',)),(15,('uuu',))]
    print wallinfo[(12,1)]#==[(4,('udd','umd'))]
    print wallinfo[(0,13)]#==[(9,('Muu',))]


if __name__=='__main__':
    testme()
