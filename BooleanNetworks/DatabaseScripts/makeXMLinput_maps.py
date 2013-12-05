import numpy as np
import makeboxes

def Example8D_1(paramlist):
    # name params
    A1 = paramlist[0];A2=paramlist[1];A3=paramlist[2];A4=paramlist[3];A5=paramlist[4];A6=paramlist[5];A7 = paramlist[6];A8=paramlist[7];A9=paramlist[8];A10=paramlist[9]
    B1=paramlist[10];B2=paramlist[11];B3=paramlist[12];B4=paramlist[13];B5=paramlist[14];B6=paramlist[15]
    A1max = paramlist[16];A2max=paramlist[17];A3max=paramlist[18];A4max=paramlist[19];A5max=paramlist[20];A6max=paramlist[21];A7max = paramlist[22];A8max=paramlist[23];A9max=paramlist[24];A10max=paramlist[25]
    B1max=paramlist[26];B2max=paramlist[27];B3max=paramlist[28];B4max=paramlist[29];B5max=paramlist[30];B6max=paramlist[31]
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


def test4DExample1(paramlist):
    # name params
    A = paramlist[0];B=paramlist[1];C=paramlist[2];D=paramlist[3];E=paramlist[4];F=paramlist[5]
    Amax = paramlist[6];Bmax=paramlist[7];Cmax=paramlist[8];Dmax=paramlist[9];Emax=paramlist[10];Fmax=paramlist[11]
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

def test4DExample2(paramlist):
    # name params
    A = paramlist[0];B=paramlist[1];Amax=paramlist[2];Bmax=paramlist[3]
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

def test4DExample3(paramlist):
    # name params
    A = paramlist[0];B=paramlist[1];Amax=paramlist[2];Bmax=paramlist[3]
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

def genStringForFixedParams(model,paramlist):
    variables, affectedby, maps, thresholds, loweramplitudes, upperamplitudes, lowerdecayrates, upperdecayrates, productionrates, upperbounds, lowerbounds = model(paramlist)
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
    xmlstr = genStringForFixedParams(Example8D_1,[1,1,1,1,1,1,1,1,1,1,.1,.1,.1,.1,.1,.1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1])
    print(xmlstr)
