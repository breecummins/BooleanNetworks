#!/usr/bash python

import processResultsArrays as pRA
import processResultsInts as pRI
import modelNetworks as mN
import os

maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_biggerx/')
ugtI,gcI,ubtI,bcI = pRI.loadNSort(maindir+'model2tracks*')    
ugtA,gcA,ubtA,bcA = pRA.loadNSort(maindir+'model2tracks*')    

for u in ugtI:
    if u not in ugtA:
        print(u)
        print(mN.decodeInts(u))
