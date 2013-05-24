import processResultsArrays as pRA
import processResultsInts as pRI
import modelNetworks as mN
import os

def checkme():
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
    results = pRI.loadNSort(maindir+'model4tracks*_ints.pickle')  
    pRI.printme(results)  
    results = pRA.loadNSort(maindir+'model4tracks*_arrays.pickle')    
    pRA.printme(results)  

    # for u in ugtI:
    #     if u not in ugtA:
    #         print(u)
    #         print(mN.decodeInts(u))

if __name__ == '__main__':
    checkme()