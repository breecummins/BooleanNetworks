import numpy as np
import itertools

def xyz3DExample():
    '''
    Example inputs.

    '''
    # define the interactions between variables
    variables = ['x','y','z']
    affectedby = [['x','y','z'],['x'],['x','y']]
    # give the thresholds for each interaction
    thresholds = [[0.25,0.5,0.5],[0.5],[0.75,0.5]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,0),(0,1),(1,0),(1,1)]]
    loweramplitudes = [[0.5,0.75,1.0,0.0,1.25,0.25,0.5,0.75],[0.0,0.5],[0.0,0.5,0.5,1.0]]
    upperamplitudes = [[1.5,2.25,3.0,0.0,3.75,0.75,1.5,2.25],[0.0,1.5],[0.0,1.5,1.5,3.0]]
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1.5,-0.75,-0.75]
    upperdecayrates = [-0.5,-0.25,-0.25]
    # give the endogenous production rates. These values must be nonzero.
    productionrates = [0.1,0.1,0.1] 
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates

def convertInputsToXML(variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates):
    thresh,ainds,pr = makeParameterArrays(variables, affectedby, thresholds, productionrates)
    upperbounds = ((np.array([np.max(u) for u in upperamplitudes]) + pr) / np.abs(np.array(upperdecayrates))) + pr # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    doms = getDomains(thresh,upperbounds)
    lsigs,usigs = getSigmas(doms,thresh,loweramplitudes,upperamplitudes,pr,ainds,maps)
    generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs)

def makeParameterArrays(variables, affectedby, thresholds, productionrates):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, lamp, uamp, and rep are len(variables) x len(variables)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero. The output
    pr is simply the list productionrates converted to an array.

    '''
    N = len(variables)
    thresh = np.zeros((N,N))
    ainds = []
    for j,a in enumerate(affectedby): #j is index of target
        at = []
        for k,t in enumerate(a):
            i =  variables.index(t) #i is index of source
            at.append(i)
            thresh[j,i] = thresholds[j][k]
        ainds.append(at)
    pr = np.array(productionrates)
    return thresh, ainds, pr

def getDomains(thresh,upperbounds):
    '''
    Find the domain bounds for each 
    regular domain (area between thresholds).

    '''
    dp = []
    for j in range(thresh.shape[1]):
        tl = list(np.unique(thresh[:,j])) + [upperbounds[j]]
        if tl[0] != 0:
            tl = [0] + tl
        dp.append( [tl[k:k+2] for k in range(len(tl[:-1]))] )
    # return the bounds for each regular domain 
    return np.array(list(itertools.product(*dp)))

def getSigmas(doms,thresh,lamp,uamp,pr,ainds,maps):
    '''
    Find the sigma bounds in each regular domain.

    '''
    lsigs = []
    usigs = []
    for i in range(doms.shape[0]):
        ls=[]
        us=[]
        for j,a in enumerate(ainds):
            bmap = tuple( (np.mean(doms[i,:,:],1) > thresh[j,:]).astype(int)[a] ) # get the binary map for target j
            for k,m in enumerate(maps[j]):
                if m == bmap:
                    ls.append(lamp[j][k]+pr[j])
                    us.append(uamp[j][k]+pr[j])
                    break
        lsigs.append(ls)
        usigs.append(us)
    return lsigs,usigs

def generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs):
    f = open('input2.xml','w')
    f.write("<atlas>\n")
    f.write("  <dimension> " + str(len(lowerbounds)) + " </dimension>\n")
    f.write("  <phasespace>\n")
    f.write("    <bounds>\n")
    f.write("      <lower> " + "  ".join([str(l) for l in lowerbounds]) + " </lower>\n")  
    f.write("      <upper> " + "  ".join([str(u) for u in upperbounds]) + " </upper>\n")  
    f.write("    </bounds>\n")
    f.write("  </phasespace>\n")
    f.write("  <gamma>\n")
    f.write("    <lower> " + "  ".join([str(l) for l in lowerdecayrates]) + " </lower>\n")
    f.write("    <upper> " + "  ".join([str(u) for u in upperdecayrates]) + " </upper>\n")
    f.write("  </gamma>\n")
    f.write("  <listboxes>\n")
    for k in range(doms.shape[0]):
        f.write("    <box> <!-- box : " + str(k) + " -->\n")
        f.write("      <bounds>\n")
        f.write("        <lower> " + "  ".join([str(l) for l in doms[k,:,0]]) + " </lower>\n")
        f.write("        <upper> " + "  ".join([str(u) for u in doms[k,:,1]]) + " </upper>\n")
        f.write("      </bounds>\n")
        f.write("      <sigma> \n")
        f.write("        <lower> " + "  ".join([str(l) for l in lsigs[k]]) + " </lower>\n")
        f.write("        <upper> " + "  ".join([str(u) for u in usigs[k]]) + " </upper>\n")
        f.write("      </sigma>\n")
        f.write("    </box>\n")
    f.write("  </listboxes>\n")
    f.write("</atlas>\n")
    f.close()

if __name__ == "__main__":
    variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates = xyz3DExample()
    convertInputsToXML(variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates)