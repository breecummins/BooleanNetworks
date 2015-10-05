import processResultsArrays as pRA
import processResultsInts as pRI
import modelNetworks as mN
import os

def checkme():
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    resultsI = pRI.loadNSort(maindir+'model4tracks*_ints.pickle')  
    # pRI.printme(resultsI)  
    resultsA = pRA.loadNSort(maindir+'model4tracks*_arrays.pickle')    
    # pRA.printme(resultsA)

    # for i,u in enumerate(resultsA['uniqbadtracks']):
    #     ue = mN.encodeInts(u)
    #     for k,b in enumerate(resultsI['uniqbadtracks']):
    #         if ue == b:
    #             ind = k
    #             break
    #     if resultsA['translatedbadtracks'][i] != [] and resultsI['translatedbadtracks'][ind] == []:
    #         print(ue)
    #         print(u)

if __name__ == '__main__':
    checkme()