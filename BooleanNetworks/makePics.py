import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import networkScripts as nS

def plot2D(Alist,myfiles,titlestr='Model 1',xlabel='A',ylabel='proportion of single loops'):
    oneloops,numtracks,uoneloops,utracks = nS.loadNSort(myfiles)
    props = np.array([oneloops[k]/numtracks[k] for k in range(len(oneloops))])
    print(uoneloops)
    plt.plot(np.array(Alist),props)
    plt.title(titlestr)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot3D(Alist,Blist,myfiles,titlestr='Model 2',xlabel='A',ylabel='B',zlabel='proportion of single loops'):
    oneloops,numtracks,uoneloops,utracks = nS.loadNSort(myfiles)
    props = np.array([oneloops[k]/numtracks[k] for k in range(len(oneloops))])
    print(uoneloops)
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
    plt.zlabel(zlabel)

if __name__ == "__main__":
    # make sure order is preserved with glob
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model1*')
    plot2D([0.5,1.0,1.5,2.0],myfiles)
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model2*')
    plot2D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles)
    myfiles = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset1/model5*')
    plot2D([0.5,1.0,1.5,2.0],[-0.5,-1.0,-2.0],myfiles,'Model 5')
