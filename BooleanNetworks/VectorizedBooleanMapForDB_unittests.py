import numpy as np
import VectorizedBooleanMapForDB as VBD

def xyz3DTest():
    # 3D example
    sources = ['x','y','z']
    targets = [['x','y','z'],['x','z'],['x']]
    thresholds = [[0.25,0.5,0.75],[0.5,0.5],[0.5]]
    amplitudes = [[0.5,1.0,1.0],[1.0,1.0],[1.0]]
    decayrates = [1.0,0.5,0.5]
    repressors = [('z','x')]
    productionrates = [0.1,0.1,0.1]
    thresh,amp,rep,dr,pr = VBD.makeParameterArrays(sources,targets,thresholds,amplitudes,productionrates,decayrates,repressors)
    maxvals = [2.0,3.0,4.0]
    doms, fps = VBD.getDomainsAndFocalPoints(thresh,amp,rep,dr,pr,maxvals)
    print("Number of domains: {0}".format(len(doms)))
    walls = VBD.makeWalls(thresh,maxvals)
    print("Number of walls: {0}".format(len(walls)))
    # for w in walls:
    #     formattedw = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in w]
    #     print(str(formattedw).translate(None, "'"))
    unidirwalls, unidirfps, whitewalls = VBD.identifyWhiteWalls(walls,doms,fps,dr)
    next_threshs, steadypts = VBD.getNextThresholdsAndSteadyStates(unidirwalls, unidirfps, thresh)
    print("White walls: {0}".format(whitewalls))
    formattedh = ['[{0:.3f}, {1:.3f}, {2:.3f}, {3:.3f}]'.format(sp[0],sp[1],sp[2],sp[3]) for sp in steadypts]
    print("Steady points: " + str(formattedh).translate(None, "'"))
    print("")
    wallvertices = VBD.constructVertices(unidirwalls)
    mappedpts = []
    allsteps = []
    for k,w in enumerate(wallvertices):
        mp, mpa = VBD.mapManyPointsToMultipleHyperplanes(w,unidirfps[k],next_threshs[k],dr)
        mappedpts.append( mp )
        allsteps.append( mpa )
    for k,u in enumerate(unidirwalls):
        formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in u]
        print("Wall: " + str(formattedh).translate(None, "'"))
        print("Focal point: {0}".format(unidirfps[k]))
        print("Next hyperplanes: {0}".format(next_threshs[k]))
        print("Wall vertices: {0}".format(wallvertices[k]))
        print("Next steps for vertices: {0}".format(mappedpts[k]))
        print("All hyperplane steps for vertices: {0}".format(allsteps[k]))
        print("")

if __name__ == '__main__':
    xyz3DTest()