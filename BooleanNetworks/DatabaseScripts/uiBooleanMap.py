import numpy as np
import itertools
import libBooleanMap as libBM

def xyz3DExample():
    '''
    Example problem worked out analytically.
    Code working on Mac OS 10.7.5 with the Enthought Python distribution.
    Python 2.7.2 (32 bit) and numpy 1.6.1.

    '''
    sources = ['x','y','z']
    targets = [['x','y','z'],['x','z'],['x']]
    thresholds = [[0.25,0.5,0.75],[0.5,0.5],[0.5]]
    amplitudes = [[0.5,1.0,1.0],[1.0,1.0],[1.0]]
    decayrates = [1.0,0.5,0.5]
    repressors = [('z','x')]
    productionrates = [0.1,0.1,0.1] # These values must remain nonzero
    thresh,amp,rep,dr,pr = libBM.makeParameterArrays(sources,targets,thresholds,amplitudes,productionrates,decayrates,repressors)
    maxvals = ((np.sum(amp,1) + pr) / dr) + pr # calculate upper bounds of domains
    wallsandsteadypts, wallvertices, shorteststepinds, allsteps, allmaps, next_threshs, focalpts = libBM.runModel(thresh,amp,rep,dr,pr,maxvals)
    return wallsandsteadypts, wallvertices, shorteststepinds, allsteps, allmaps, next_threshs, focalpts, dr

def makeNewGridPoints(wallvertices):
    '''
    This function subdivides each wall into 4 pieces and returns all the vertices,
    including the corners (which were already mapped).

    '''
    newgridpoints = [] 
    for wv in wallvertices:
        coords = [[v[j] for v in wv] for j in range(len(wv[0]))]
        mins = [np.min(c) for c in coords]
        maxs = [np.max(c) for c in coords]
        lists = []
        for j in range(len(mins)):
            if mins[j] == maxs[j]:
                lists.append( [mins[j]] )
            else:
                lists.append( [mins[j], (maxs[j] - mins[j])/2, maxs[j] ])
        newgridpoints.append([ np.array(pt) for pt in itertools.product(*lists)])
    return newgridpoints

def mapSubdivisions(newgridpoints,focalpts,next_threshs,dr,wallsandsteadypts,allmaps):
    newshorteststepinds, newallsteps = libBM.takeSteps(newgridpoints,focalpts,next_threshs,dr,wallsandsteadypts,allmaps)
    return newshorteststepinds, newallsteps

def getMappedPts(shorteststepinds,allsteps):
    '''
    Return the true images of all of the vertices.

    '''
    mappedpts = []
    for k,m in enumerate(shorteststepinds):    
        um = [sublist[0] for sublist in m]
        mappedpts.append([allsteps[k][j][m1] for j,m1 in enumerate(um)])
    return mappedpts

def getWallIdentifiers(shorteststepinds,allmaps):
    '''
    Return the indices of the walls for the true images of 
    all the vertices. More than one wall index may be returned
    per point due to simultaneous arrival times.

    '''
    wallidentifiers = []
    for k,m in enumerate(shorteststepinds):    
        wallidentifiers.append([[allmaps[k][q] for q in sublist] for sublist in m ])
    return wallidentifiers

def printOutput(wallsandsteadypts, wallvertices, shorteststepinds, allsteps, allmaps):
    '''
    Print the output of xyz3DExample or of mapSubdivisions in a readable format.

    '''
    mappedpts = getMappedPts(shorteststepinds,allsteps)
    wallidentifiers = getWallIdentifiers(shorteststepinds,allmaps)
    for k,m in enumerate(shorteststepinds):
        formattedh = ['({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in wallsandsteadypts[k]]
        print("Wall: " + str(formattedh).translate(None, "'"))
        print("Wall identifier: {0}".format(k))
        print("Wall vertices: ")
        for arr in wallvertices[k]:
            formattedv = '[{0:.4f}, {1:.4f}, {2:.4f}]'.format(arr[0],arr[1],arr[2])
            print(str(formattedv).translate(None, "'"))
        print("Next steps for vertices: ")
        for mp in mappedpts[k]:
            formattedn = '[{0:.4f}, {1:.4f}, {2:.4f}]'.format(mp[0],mp[1],mp[2])
            print(str(formattedn).translate(None, "'"))
        print("Wall identifiers for next steps: {0}".format(wallidentifiers[k]))
        print("Walls of next steps: ")
        for sublist in wallidentifiers[k]:
            try:
                formattedhs = [ [ '({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in wallsandsteadypts[i] ] for i in sublist ]
            except:
                formattedhs = [ '({0:.3f}, {1:.3f})'.format(tup[0],tup[1]) for tup in wallsandsteadypts[sublist] ]
            print(str(formattedhs).translate(None, "'"))
        print("All hyperplane steps for vertices: ")
        for sublist in allsteps[k]:
            formattedhs = [ '[{0:.4f}, {1:.4f}, {2:.4f}]'.format(arr[0],arr[1],arr[2]) for arr in sublist ]
            print(str(formattedhs).translate(None, "'"))
        print("")
        print("")
        print("")


if __name__ == '__main__':
    wallsandsteadypts, wallvertices, shorteststepinds, allsteps, allmaps, next_threshs, focalpts, dr = xyz3DExample()
    # printOutput(wallsandsteadypts, wallvertices, shorteststepinds, allsteps, allmaps)
    newgridpoints = makeNewGridPoints(wallvertices)
    newshorteststepinds, newallsteps = mapSubdivisions(newgridpoints,focalpts,next_threshs,dr,wallsandsteadypts,allmaps)
    printOutput(wallsandsteadypts, newgridpoints, newshorteststepinds, newallsteps, allmaps)