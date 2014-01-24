import numpy as np
import makeboxes

def Example5D_1(A1,A2,A3,A4,A5,A6,A7,B1,A1max,A2max,A3max,A4max,A5max,A6max,A7max,B1max):
    # define the interactions between variables
    variables = ['x','y1','y2','y3','z']
    affectedby = [['x','y3','z'],['x'],['x','y1'],['y2'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1,1],[1],[4,1],[1],[3]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,0),(1,0),(0,1),(1,1)],[(0,),(1,)],[(0,),(1,)] ]
    ampfunc = lambda A1,A2,A3,A4,A5,A6,A7,B1: [ [0,A1,A2,A1+A2,0,A1*B1,A2*B1,(A1+A2)*B1],[0,A3],[0,A4,A5,A4+A5],[0,A6],[0,A7] ]
    amps = ampfunc(A1,A2,A3,A4,A5,A6,A7,B1)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1,-1]
    # give the endogenous production rates. 
    productionrates = [0.1,0.1,0.1,0.1,0.1] 
    # get upper and lower bounds
    bigamps = ampfunc(A1max,A2max,A3max,A4max,A5max,A6max,A7max,B1max)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

def Example8D_2(A1,A2,A3,A4,A5,A6,A7,A8,A9,B1,B2,B3,B4,B5,A1max,A2max,A3max,A4max,A5max,A6max,A7max,A8max,A9max,B1max,B2max,B3max,B4max,B5max):
    # define the interactions between variables
    variables = ['x','y1','y2','y3','z','w1','w2','w3']
    affectedby = [['x','y3','w3','z','w1'],['x'],['x','y1','w1'],['y2','w1'],['x','w2'],['y2','w2'],['w1','w3'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1,1,2],[1],[4,1,1],[1,2],[3,1],[1,1],[1,2],[3]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0,0,0),(1,0,0,0,0),(0,1,0,0,0),(1,1,0,0,0),(0,0,1,0,0),(1,0,1,0,0),(0,1,1,0,0),(1,1,1,0,0),(0,0,0,1,0),(1,0,0,1,0),(0,1,0,1,0),(1,1,0,1,0),(0,0,1,1,0),(1,0,1,1,0),(0,1,1,1,0),(1,1,1,1,0),(0,0,0,0,1),(1,0,0,0,1),(0,1,0,0,1),(1,1,0,0,1),(0,0,1,0,1),(1,0,1,0,1),(0,1,1,0,1),(1,1,1,0,1),(0,0,0,1,1),(1,0,0,1,1),(0,1,0,1,1),(1,1,0,1,1),(0,0,1,1,1),(1,0,1,1,1),(0,1,1,1,1),(1,1,1,1,1)],[(0,),(1,)],[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,),(1,)] ]
    ampfunc = lambda A1,A2,A3,A4,A5,A6,A7,A8,A9,B1,B2,B3,B4,B5: [ [0,A1,A2,A1+A2,A3,A1+A3,A2+A3,A1+A2+A3,0,A1*B1,A2*B1,(A1+A2)*B1,A3*B1,(A1+A3)*B1,(A2+A3)*B1,(A1+A2+A3)*B1,0,A1*B2,A2*B2,(A1+A2)*B2,A3*B2,(A1+A3)*B2,(A2+A3)*B2,(A1+A2+A3)*B2,0,A1*B1*B2,A2*B1*B2,(A1+A2)*B1*B2,A3*B1*B2,(A1+A3)*B1*B2,(A2+A3)*B1*B2,(A1+A2+A3)*B1*B2],[0,1.25],[0,A4,A5,A4+A5,A6,A4+A6,A5+A6,A4+A5+A6],[0,A7,0,A7*B3],[0,A8,0,A8*B4],[0,A7,0,A7*B4],[0,A9,0,A9*B5],[0,2.25]  ]
    amps = ampfunc(A1,A2,A3,A4,A5,A6,A7,A8,A9,B1,B2,B3,B4,B5)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1,-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1,-1,-1,-1,-1]
    # give the endogenous production rates. 
    productionrates = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] 
    # get upper and lower bounds
    bigamps = ampfunc(A1max,A2max,A3max,A4max,A5max,A6max,A7max,A8max,A9max,B1max,B2max,B3max,B4max,B5max)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

def Example8D_1(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6,A1max,A2max,A3max,A4max,A5max,A6max,A7max,A8max,A9max,A10max,B1max,B2max,B3max,B4max,B5max,B6max):
    # define the interactions between variables
    variables = ['x','y1','y2','y3','z','w1','w2','w3']
    affectedby = [['x','y3','z','w1'],['x'],['x','y1','w1'],['y2','w1'],['x','w2'],['y2','w2'],['w1','w3'],['x','w2']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1,2],[1],[4,1,1],[1,2],[3,1],[1,1],[1,1],[3,1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0,0),(1,0,0,0),(0,1,0,0),(1,1,0,0),(0,0,1,0),(1,0,1,0),(0,1,1,0),(1,1,1,0),(0,0,0,1),(1,0,0,1),(0,1,0,1),(1,1,0,1),(0,0,1,1),(1,0,1,1),(0,1,1,1),(1,1,1,1)],[(0,),(1,)],[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(1,1)] ]
    ampfunc = lambda A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6: [ [0,A1,A2,A1+A2,0,A1*B1,A2*B1,(A1+A2)*B1,0,A1*B2,A2*B2,(A1+A2)*B2,0,A1*B1*B2,A2*B1*B2,(A1+A2)*B1*B2],[0,A3],[0,A4,A5,A4+A5,A6,A4+A6,A5+A6,A4+A5+A6],[0,A7,0,A7*B3],[0,A8,0,A8*B4],[0,A9,0,A9*B5],[0,A10,0,A10*B6],[0,A8,0,A8*B4]  ]
    amps = ampfunc(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1,-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1,-1,-1,-1,-1]
    # give the endogenous production rates. 
    productionrates = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] 
    # get upper and lower bounds
    bigamps = ampfunc(A1max,A2max,A3max,A4max,A5max,A6max,A7max,A8max,A9max,A10max,B1max,B2max,B3max,B4max,B5max,B6max)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds


def test4DExample1(A,B,C,D,E,F,Amax,Bmax,Cmax,Dmax,Emax,Fmax):
    '''
    Example inputs.

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1],[1]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    ampfunc = lambda A,B,C,D,E,F: [[0,E,A,A+E,0,E*F,A*F,(A+E)*F],[0,C],[0,D],[0,B]]
    amps = ampfunc(A,B,C,D,E,F)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1] #[-0.5,-0.5,-0.5]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(Amax,Bmax,Cmax,Dmax,Emax,Fmax)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

def test4DExample2(A,B,Amax,Bmax):
    '''
    Example inputs.

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[1],[1],[3]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,),(1,)]]
    ampfunc = lambda A,B: [[0,4.25,A,A+4.25,0,1.0625,A*0.25,(A+4.25)*0.25],[0,2.5],[0,2.5],[0,B]]
    amps = ampfunc(A,B)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1] #[-0.5,-0.5,-0.5]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(Amax,Bmax)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

def test4DExample3(A,B,Amax,Bmax):
    '''
    Example inputs.

    '''
    # define the interactions between variables
    variables = ['x','y1','y2','z']
    affectedby = [['x','y2','z'],['x'],['y1'],['x','y2']]
    # give the thresholds for each interaction
    thresholds = [[2,1,1],[3],[1],[1,2]]
    # give the maps and amplitudes of each interaction (upper and lower bounds for parameter search)
    maps = [[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)],[(0,),(1,)],[(0,),(1,)],[(0,0),(1,0),(0,1),(1,1)]]
    ampfunc = lambda A,B: [[0,4.25,A,A+4.25,0,1.0625,A*0.25,(A+4.25)*0.25],[0,2.5],[0,2.5],[0,B,0.4,B+0.4]]
    amps = ampfunc(A,B)
    loweramplitudes = amps
    upperamplitudes = amps
    # give the natural decay rates of the species (upper and lower bounds for parameter search)
    lowerdecayrates = [-1,-1,-1,-1]
    upperdecayrates = [-1,-1,-1,-1] #[-0.5,-0.5,-0.5]
    # give the endogenous production rates. 
    productionrates = [0.1,0.5,0.5,0.5] 
    # get upper and lower bounds
    bigamps = ampfunc(Amax,Bmax)
    upperbounds = 1.1*((np.array([np.max(u) for u in bigamps]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

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
    # give the endogenous production rates. 
    productionrates = [0.1,0.1,0.1] 
    # get upper and lower bounds
    upperbounds = 1.1*((np.array([np.max(u) for u in upperamplitudes]) + np.array(productionrates)) / np.abs(np.array(upperdecayrates))) # calculate upper bounds of domains
    lowerbounds = np.zeros(upperbounds.shape)
    return variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds

def genStringForFixedParams(model,paramtuple):
    variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds = model(*paramtuple)
    xmlstr = convertInputsToXML(variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds)
    return xmlstr

def convertInputsToXML(variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds):
    thresh,ainds,pr = makeboxes.makeParameterArrays(variables, affectedby, thresholds, productionrates)
    doms = makeboxes.getDomains(thresh,lowerbounds,upperbounds)
    lsigs,usigs = makeboxes.getSigmas(doms,thresh,loweramplitudes,upperamplitudes,pr,ainds,maps)
    xmlstr = generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs)
    return xmlstr

def generateXML(lowerbounds,upperbounds,lowerdecayrates,upperdecayrates,doms,lsigs,usigs):
    xmlstr = "<atlas>\n"
    xmlstr += "  <dimension> " + str(len(lowerbounds)) + " </dimension>\n"
    xmlstr += "  <phasespace>\n"
    xmlstr += "    <bounds>\n"
    xmlstr += "      <lower> " + "  ".join([str(l) for l in lowerbounds]) + " </lower>\n"  
    xmlstr += "      <upper> " + "  ".join([str(u) for u in upperbounds]) + " </upper>\n"  
    xmlstr += "    </bounds>\n"
    xmlstr += "  </phasespace>\n"
    xmlstr += "  <gamma>\n"
    xmlstr += "    <lower> " + "  ".join([str(l) for l in lowerdecayrates]) + " </lower>\n"
    xmlstr += "    <upper> " + "  ".join([str(u) for u in upperdecayrates]) + " </upper>\n"
    xmlstr += "  </gamma>\n"
    xmlstr += "  <listboxes>\n"
    for k in range(doms.shape[0]):
        xmlstr += "    <box> <!-- box : " + str(k) + " -->\n"
        xmlstr += "      <bounds>\n"
        xmlstr += "        <lower> " + "  ".join([str(l) for l in doms[k,:,0]]) + " </lower>\n"
        xmlstr += "        <upper> " + "  ".join([str(u) for u in doms[k,:,1]]) + " </upper>\n"
        xmlstr += "      </bounds>\n"
        xmlstr += "      <sigma> \n"
        xmlstr += "        <lower> " + "  ".join([str(l) for l in lsigs[k]]) + " </lower>\n"
        xmlstr += "        <upper> " + "  ".join([str(u) for u in usigs[k]]) + " </upper>\n"
        xmlstr += "      </sigma>\n"
        xmlstr += "    </box>\n"
    xmlstr += "  </listboxes>\n"
    xmlstr += "</atlas>\n"
    return xmlstr

if __name__ == "__main__":
    # xmlstr = genStringForFixedParams(test4DExample1,(8.0,0.6,0.6,0.6,4.0,0.1,12.0,2.5,2.5,2.5,5.0,0.9))
    # print(xmlstr)
    # xmlstr = genStringForFixedParams(Example8D_1,(1,1,1,1,1,1,1,1,1,1,.1,.1,.1,.1,.1,.1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1))
    # print(xmlstr)
    # xmlstr = genStringForFixedParams(Example8D_2,(1,1,1,1,1,1,1,1,1,.1,.1,.1,.1,.1,2,2,2,2,2,2,2,2,2,1,1,1,1,1))
    # print(xmlstr)
    xmlstr = genStringForFixedParams(Example5D_1,(1,1,1,1,1,1,1,.1,2,2,2,2,2,2,2,1))
    print(xmlstr)
