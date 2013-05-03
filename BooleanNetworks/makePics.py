import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import networkScripts as nS

def preprocess(myfiles):
    oneloops,numtracks,uoneloops,utracks = nS.loadNSort(myfiles)
    props = np.array([float(oneloops[k])/numtracks[k] for k in range(len(oneloops))])
    print('Number of one-loop tracks')
    print(oneloops)
    print('Number of tracks')
    print(numtracks)
    print('Proportions of one-loops')
    print(props)
    print('Number of unique one-loops')
    print([len(u) for u in uoneloops])
    print('Number of unique tracks')
    print([len(u) for u in utracks])
    return props    

def plot2D(Alist,myfiles,titlestr='Model 1',xlabel='A',ylabel='proportion of single loops'):
    props = preprocess(myfiles)
    plt.figure()
    plt.plot(np.array(Alist),props)
    plt.title(titlestr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot3D(Alist,Blist,myfiles,titlestr='Model 2',xlabel='A',ylabel='B',zlabel='proportion of single loops'):
    props = preprocess(myfiles)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # make sure order is preserved with glob
    newB = Blist*len(Alist)
    newA = []
    for k in range(len(Alist)):
        newA.extend([Alist[k]]*len(Blist))
    ax.plot(np.array(newA),np.array(newB),props)
    plt.title(titlestr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()

if __name__ == "__main__":
    # make sure order is preserved with glob
    import os
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model1*')
    plot2D([0.5,1.0,1.5,2.0],myfiles)
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model2*')
    plot3D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles)
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model5*')
    plot3D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles,'Model 5')
