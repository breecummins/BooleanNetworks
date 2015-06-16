import preprocess as PP
import testcases as tc
import fileparsers as fp
import numpy as np

def testme():
    test0()
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()

def test0():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test0())
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (4,), (0,), (4,), (6,), (2, 3), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 0, 0, 0, 1, 1, 0]
    varnames=['X','Z']
    patternnames=[['X','Z','X','Z']]
    patternmaxmin=[['max','max','min','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['Mu','dM','md','um','Mu']]

def test1():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test1())
    print inds==[8, 10, 11, 13]
    print outedges==[(1,), (3,), (0,), (2,)]
    print walldomains==[(1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 1, 1, 0]
    varnames=['X','Z']
    patternnames=[['X','X','Z','Z']]
    patternmaxmin=[['max','min','max','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['Mu','mu','uM','um','Mu']]

def test2():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test2())
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (3,4), (0,), (2,), (6,), (2,), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 1, 1, 0, 0, 0, 0]

def test3():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test3())
    print inds==[0,3,4,6,9,10]
    print outedges==[(2,),(0,),(4,),(1,),(5,),(3,)]
    print walldomains==[(1.5,1,0.5),(1,1.5,0.5),(1.5,0.5,1),(0.5,1.5,1),(1,0.5,1.5),(0.5,1,1.5)]
    print varsaffectedatwall==[2,1,0,0,1,2]
    varnames=['X','Y','Z']
    patternnames=[['X','Z','Y','X','Y','Z'],['Z','X','Y','Y','X','Z']]
    patternmaxmin=[['min','max','min','max','max','min'],['max','min','min','max','max','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['mdu','udM','umd','Mud','dMd','ddm','mdu'],['ddM','mdd','umd','uMd','Mdd','ddm','ddM']]

    outedges,walldomains,varsaffectedatwall=tc.test3()
    print PP.strongConnectWallNumbers(outedges) == [0,3,4,6,9,10]
    varnames=fp.parseVars()
    patternnames,patternmaxmin=fp.parsePatterns()
    print PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)==[['udm','Mdu','dmu','duM','mud','uMd','udm'],['dum','muu','uMu','umu','uuM','Mud','dum']]
    wallthresh=[1,0,1,0,2,2,2,2,1,0,1,0]+[1,0,2]*8
    threshnames=fp.parseEqns()
    print PP.varsAtWalls(threshnames,walldomains,wallthresh,varnames)==varsaffectedatwall


def test4():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test4())
    print inds==range(5,12)
    print outedges==[(2,),(0,3),(5,),(6,),(1,),(6,),(4,)]
    print walldomains==[(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2,2.5),(2.5,1),(2.5,2)]
    print varsaffectedatwall==[1,0,1,1,1,1,0]
    varnames=['X1','X2']
    patternnames=[['X1','X2','X1','X2'],['X1','X1','X2','X2']]
    patternmaxmin=[['min','min','max','max'],['max','min','min','max']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['md','um','Mu','dM','md'],['Md','md','um','uM','Md']]

def test5():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test5())
    print inds==[0,1,4,7,8,12,13,15,16,18,19]
    print outedges==[(3,),(0,4),(1,),(7,),(6,8),(2,),(7,),(9,),(10,),(10,),(5,)]
    print walldomains==[(0.5,1,1.5),(0.5,2,1.5),(1,2.5,1.5),(0.5,0.5,1),(0.5,1.5,1),(1.5,2.5,1),(0.5,1,0.5),(1,0.5,0.5),(1,1.5,0.5),(1.5,1,0.5),(1.5,2,0.5)]
    print varsaffectedatwall==[0,2,1,0,0,0,0,1,1,0,2]
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['mdd','umd','uum','Muu','dMu','ddM','mdd'],['mdd','umd','Mud','dum','dMu','ddM','mdd']]

def test6():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels,inedges,triples,sortedwalllabels = PP.filterAllTriples(*tc.test6())
    print inds==[4,5,7,8,9,10,11,14,16,17,18,19,23,24,25,26,27]
    print outedges==[(3,8,13),(4,),(12,),(10,15),(16,),(9,),(2,14),(0,),(4,),(2,14),(16,),(6,),(1,7),(9,),(4,),(5,11),(6,)]
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['umu','Muu','duM','dMd','mdd','udm','umu'],['uuM','uum','Muu','duM','dMd','mdd','udm','umu','uuM'],['mud','uum','Muu','duM','mud'],['mdd','udm','Mdu','ddM','mdd'],['umd','uum','Muu','duM','dMd','mdd','umd'],['dmd','dum','muu','uuM','uMd','Mdd','dmd']]

def test7():
    outedges=[(1,2),(5,8),(3,),(4,),(2,),(6,7),(7,),(6,),(0,)]
    components=PP.strongConnect(outedges)
    print all(components==np.array([3,3,0,0,0,2,1,1,3]))
    print PP.strongConnectWallNumbers(outedges) == [0,1,2,3,4,6,7,8]


if __name__=='__main__':
	testme()
