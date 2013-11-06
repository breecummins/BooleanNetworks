import numpy as np
import itertools

def xyz3DExample():
    '''
    Example inputs.

    '''
    # define the interactions between variables
    sources = ['x','y','z']
    targets = [['x','y','z'],['x','z'],['x']]
    repressors = [('z','x')]
    # give the thresholds for each interaction
    thresholds = [[0.25,0.5,0.75],[0.5,0.5],[0.5]]
    # give the amplitudes of each interaction (upper and lower bounds for parameter search)
    loweramplitudes = [[0.25,0.5,0.5],[0.5,0.5],[0.5]]
    upperamplitudes = [[0.75,1.5,1.5],[1.5,1.5],[1.5]]
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1.5,-0.75,-0.75]
    upperdecayrates = [-0.5,-0.25,-0.25]
    # give the endogenous production rates. These values must be nonzero.
    productionrates = [0.1,0.1,0.1] 
    return sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates

def convertInputsToXML(sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates):
    thresh,lamp,uamp,rep,pr = makeParameterArrays(sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, productionrates)
    upperbounds = ((np.sum(uamp,1) + pr) / np.abs(np.array(upperdecayrates))) + pr # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    doms = getDomains(thresh,upperbounds)
    lsigs,usigs = getSigmas(doms,thresh,lamp,uamp,rep,pr)
    generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs)

def makeParameterArrays(sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, productionrates):
    '''
    Put model parameters into square arrays, where the column 
    index indicates the source variable and the row index 
    indicates the target variable.

    The outputs thresh, lamp, uamp, and rep are len(sources) x len(sources)
    arrays with threshold values, amplitudes, and repressor 
    identities filled in between the appropriate source-target 
    interactions. All other array values are zero. The output
    pr is simply the list productionrates converted to an array.

    '''
    N = len(sources)
    thresh = np.zeros((N,N))
    lamp = np.zeros((N,N))
    uamp = np.zeros((N,N))
    for j,targ in enumerate(targets): #j is index of source
        for k,t in enumerate(targ):
            i = sources.index(t) #i is index of target
            thresh[i,j] = thresholds[j][k]
            lamp[i,j] = loweramplitudes[j][k]
            uamp[i,j] = upperamplitudes[j][k]
    rep = np.zeros((N,N))
    for r in repressors:
        j = sources.index(r[0])
        i = sources.index(r[1])
        rep[i,j] = 1
        if i == j:
            raise ValueError('Negative self-regulation is not allowed. No variable may repress itself.')
    pr = np.array(productionrates)
    return thresh, lamp, uamp, rep.astype(int), pr

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

def getSigmas(doms,thresh,lamp,uamp,rep,pr):
    '''
    Find the sigma bounds in each regular domain.

    '''
    lsigs = []
    usigs = []
    for i in range(doms.shape[0]):
        uprep = (np.mean(doms[i,:,:],1) > thresh) ^ rep # array of zeros and ones
        lsigs.append( (lamp*uprep).sum(1) + pr ) # mask amps by 0-1 array, then sum the result
        usigs.append( (uamp*uprep).sum(1) + pr ) 
    return lsigs,usigs

def generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs):
    f = open('input.xml','w')
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
    sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates = xyz3DExample()
    convertInputsToXML(sources, targets, repressors, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates)