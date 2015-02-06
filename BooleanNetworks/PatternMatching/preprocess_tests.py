import preprocess as PP
import testcases as tc
import fileparsers as fp
import numpy as np

def testme():
    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test0())
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (4,), (0,), (4,), (6,), (2, 3), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 0, 0, 0, 1, 1, 0]
    varnames=['X','Z']
    patternnames=[['X','Z','X','Z']]
    patternmaxmin=[['max','max','min','min']]
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    print patterns==[['Mu','dM','md','um','Mu']]

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test1())
    print inds==[8, 10, 11, 13]
    print outedges==[(1,), (3,), (0,), (2,)]
    print walldomains==[(1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 1, 1, 0]
    varnames=['X','Z']
    patternnames=[['X','X','Z','Z']]
    patternmaxmin=[['max','min','max','min']]
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    print patterns==[['Mu','mu','uM','um','Mu']]

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test2())
    print inds==[3, 5, 6, 8, 10, 11, 13]
    print outedges==[(1,), (3,4), (0,), (2,), (6,), (2,), (5,)]
    print walldomains==[(0.5, 1), (1, 0.5), (1, 1.5), (1.5, 1), (2, 0.5), (2, 1.5), (2.5, 1)]
    print varsaffectedatwall==[0, 1, 1, 0, 0, 0, 0]

    inds,outedges,walldomains,varsaffectedatwall,allwalllabels = PP.filterAll(*tc.test3())
    print inds==[0,3,4,6,9,10]
    print outedges==[(2,),(0,),(4,),(1,),(5,),(3,)]
    print walldomains==[(1.5,1,0.5),(1,1.5,0.5),(1.5,0.5,1),(0.5,1.5,1),(1,0.5,1.5),(0.5,1,1.5)]
    print varsaffectedatwall==[2,1,0,0,1,2]
    varnames=['X','Y','Z']
    patternnames=[['X','Z','Y','X','Y','Z'],['Z','X','Y','Y','X','Z']]
    patternmaxmin=[['min','max','min','max','max','min'],['max','min','min','max','max','min']]
    patterns=PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)
    print patterns==[['mdu','udM','umd','Mud','dMd','ddm','mdu'],['ddM','mdd','umd','uMd','Mdd','ddm','ddM']]

    outedges=[(1,2),(5,8),(3,),(4,),(2,),(6,7),(7,),(6,),(0,)]
    N,components=PP.strongConnect(outedges)
    print N==4 and all(components==np.array([3,3,0,0,0,2,1,1,3]))
    print PP.strongConnectWallNumbers(outedges) == [0,1,2,3,4,6,7,8]

    outedges,walldomains,varsaffectedatwall=tc.test3()
    print PP.strongConnectWallNumbers(outedges) == [0,3,4,6,9,10]
    varnames=fp.parseVars()
    patternnames,patternmaxmin=fp.parsePatterns()
    print PP.constructCyclicPatterns(varnames,patternnames,patternmaxmin)==[['udm','Mdu','dmu','duM','mud','uMd','udm'],['dum','muu','uMu','umu','uuM','Mud','dum']]
    wallthresh=[1,0,1,0,2,2,2,2,1,0,1,0]+[1,0,2]*8
    threshnames=fp.parseEqns()
    print PP.varsAtWalls(threshnames,walldomains,wallthresh,varnames)==varsaffectedatwall



if __name__=='__main__':
	testme()
