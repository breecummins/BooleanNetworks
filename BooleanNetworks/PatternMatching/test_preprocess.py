import preprocess as PP
import walllabels as WL
import testcases as tc
import fileparsers as fp

def testme():
    test0()
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()

def test0():
    varnames=['X','Z']
    patternnames=[['X','Z','X','Z']]
    patternmaxmin=[['max','max','min','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['Mu','dM','md','um','Mu']]

def test1():
    varnames=['X','Z']
    patternnames=[['X','X','Z','Z']]
    patternmaxmin=[['max','min','max','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['Mu','mu','uM','um','Mu']]

def test2():
    varnames=['X','Z']
    patternnames=[['X','X','Z']]
    patternmaxmin=[['max','min','max']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=0)
    print patterns==[['Mu','mu','uM']]

def test3():
    outedges,walldomains,varsaffectedatwall=tc.test3()
    varnames=['X','Y','Z']
    patternnames=[['X','Z','Y','X','Y','Z'],['Z','X','Y','Y','X','Z']]
    patternmaxmin=[['min','max','min','max','max','min'],['max','min','min','max','max','min']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['mdu','udM','umd','Mud','dMd','ddm','mdu'],['ddM','mdd','umd','uMd','Mdd','ddm','ddM']]
    varnames=fp.parseVars()
    patternnames,patternmaxmin=fp.parsePatterns()
    print PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)==[['udm','Mdu','dmu','duM','mud','uMd','udm'],['dum','muu','uMu','umu','uuM','Mud','dum']]
    wallthresh=[1,0,2,2,0,1]
    threshnames=fp.parseEqns()
    print PP.varsAtWalls(threshnames,walldomains,wallthresh,varnames)==varsaffectedatwall


def test4():
    varnames=['X1','X2']
    patternnames=[['X1','X2','X1','X2'],['X1','X1','X2','X2']]
    patternmaxmin=[['min','min','max','max'],['max','min','min','max']]
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['md','um','Mu','dM','md'],['Md','md','um','uM','Md']]

def test5():
    _=tc.test5()
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['mdd','umd','uum','Muu','dMu','ddM','mdd'],['mdd','umd','Mud','dum','dMu','ddM','mdd']]

def test6():
    _=tc.test6()
    patternnames,patternmaxmin=fp.parsePatterns()
    varnames=fp.parseVars()
    patterns=PP.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    print patterns==[['umu','Muu','duM','dMd','mdd','udm','umu'],['uuM','uum','Muu','duM','dMd','mdd','udm','umu','uuM'],['mud','uum','Muu','duM','mud'],['mdd','udm','Mdu','ddM','mdd'],['umd','uum','Muu','duM','dMd','mdd','umd'],['dmd','dum','muu','uuM','uMd','Mdd','dmd']]

def test7():
    tc.test7()
    varnames,threshnames,domgraph,cells=fp.parseNewJSONFormat()
    outedges,wallthresh,walldomains=PP.makeWallGraphFromDomainGraph(domgraph,cells)
    varsaffectedatwall=PP.varsAtWalls(zip(varnames,threshnames),walldomains,wallthresh,varnames)
    print outedges==[(1,),(2,),(3,),(4,),(5,),(0,)]
    print wallthresh==[1,2,0,1,2,0]
    print walldomains==[(0.5,1,1.5),(0.5,1.5,1),(1,1.5,0.5),(1.5,1,0.5),(1.5,0.5,1),(1,0.5,1.5)]
    print varsaffectedatwall==[2,0,1,2,0,1]


def test8():
    tc.test8()
    varnames,threshnames,domgraph,cells=fp.parseNewJSONFormat()
    outedges,wallthresh,walldomains=PP.makeWallGraphFromDomainGraph(domgraph,cells)
    varsaffectedatwall=PP.varsAtWalls(zip(varnames,threshnames),walldomains,wallthresh,varnames)
    print outedges == [(1,),(2,3),(6,),(4,),(5,),(6,),(0,)]
    print wallthresh == [2,3,2,3,2,3,3]
    print walldomains == [(0.5,1.5,3,0.5,1.5),(0.5,1.5,3.5,1,1.5),(0.5,1.5,3,1.5,1.5),(0.5,1.5,3.5,2,1.5),(0.5,1.5,3,2.5,1.5),(0.5,1.5,2.5,2,1.5),(0.5,1.5,2.5,1,1.5)]
    print varsaffectedatwall==[3,2,3,4,3,4,2]

if __name__=='__main__':
	testme()
