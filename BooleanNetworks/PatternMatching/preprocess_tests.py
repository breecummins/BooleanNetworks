import preprocess as PP
import testcases as tc

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



if __name__=='__main__':
	testme()
