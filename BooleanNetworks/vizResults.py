import numpy as np
import matplotlib as mpl
# mpl.use('Pdf') #comment out if you want to see figures at run time
import matplotlib.pyplot as plt
import cPickle, os, glob
import processResultsInts as pRI

def plots(x,y,show=1,hold=0,stylestr=None,leglabels=None,legloc=4,titlestr=None,xstr=None,ystr=None,xticklabels=None,fname=None,tweak=0):
    if not hold:
        fig = plt.figure(figsize=(12, 9))
    else:
        plt.hold('on')
    if leglabels == None and stylestr == None:
        plt.plot(x,y,linewidth=2.0)  
    else:
        if len(y.shape) == 2 and len(x.shape)==1:
            for k in range(y.shape[1]):
                if leglabels != None and stylestr != None:
                    plt.plot(x,y[:,k],stylestr[k],linewidth=2.0,label=leglabels[k])
                elif leglabels != None and stylestr == None:
                    plt.plot(x,y[:,k],linewidth=2.0,label=leglabels[k])
                elif leglabels == None and stylestr != None:
                    plt.plot(x,y[:,k],stylestr[k],linewidth=2.0)
        elif len(y.shape) == 2 and len(x.shape)==2:
            for k in range(y.shape[1]):
                if leglabels != None and stylestr != None:
                    plt.plot(x[:,k],y[:,k],stylestr[k],linewidth=2.0,label=leglabels[k])
                elif leglabels != None and stylestr == None:
                    plt.plot(x[:,k],y[:,k],linewidth=2.0,label=leglabels[k])
                elif leglabels == None and stylestr != None:
                    plt.plot(x[:,k],y[:,k],stylestr[k],linewidth=2.0)
        else:
            if leglabels != None and stylestr != None:
                plt.plot(x,y,stylestr,linewidth=2.0,label=leglabels)
            elif leglabels != None and stylestr == None:
                plt.plot(x,y,linewidth=2.0,label=leglabels)
            elif leglabels == None and stylestr != None:
                plt.plot(x,y,stylestr,linewidth=2.0)
    if titlestr != None:  
        plt.title(titlestr)
    if xstr != None: 
        plt.xlabel(xstr)
    if ystr != None:
        plt.ylabel(ystr)
    if leglabels != None:
        plt.legend(loc=legloc,prop={'size':18})
    if xticklabels:
        ax = plt.gca()
        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels)
        if tweak:
            plt.setp(ax.get_xticklabels(), fontsize=14)
    mpl.rc('font',size=18)
    if fname != None:
        plt.savefig(fname,format='pdf', bbox_inches="tight")
    if show:
        plt.show()

if __name__ == '__main__':
    maindir = os.path.expanduser('~/SimulationResults/BooleanNetworks/dataset_randinits_x1to10/')
    for k in range(1,5):
        sharpones = []
        broadones = []
        periodiconewave = []
        overlappedonewave = []
        twowaves = []
        for myfile in glob.glob(maindir+'model{0!s}tracks*_results.pickle'.format(k)):
            print(myfile)
            with open(myfile,'r') as of:
                res = cPickle.load(of)
            Ntotalmodified = pRI.countme(res)
            sharpones.append(res['classes']['sharponeloopcountmodified'] / Ntotalmodified[-1])
            broadones.append(res['classes']['oneloopcountmodified'] / Ntotalmodified[-1])
            periodiconewave.append(( res['classes']['sharpperiodiccountmodified'] + res['classes']['periodiccountmodified'] ) / Ntotalmodified[-1])
            overlappedonewave.append(res['classes']['overlappedcountmodified'] / Ntotalmodified[-1])
            twowaves.append(( res['classes']['sharpperiodictwowavescountmodified'] + res['classes']['periodictwowavescountmodified'] + res['classes']['overlappedtwowavescountmodified']) / Ntotalmodified[-1])
        x = np.arange(len(sharpones))
        if len(x) == 4:
            xticklabels=['0.5','1.0','1.5','2.0']
        else:
            xticklabels=['(.5,-.5)','(.5,-1)','(.5,-2)','(1,-.5)','(1,-1)','(1,-2)','(1.5,-.5)','(1.5,-1)','(1.5,-2)','(2,-.5)','(2,-1)','(2,-2)']
        y = np.array([sharpones,broadones,periodiconewave,overlappedonewave,twowaves]).transpose()
        leglabels = ['sharp ones','broad ones','periodic < 2', 'overlapped < 2', 'two waves']
        fname = os.path.join(maindir,'Model{0}Pics.pdf'.format(k))
        if k == 1:
            tweak = 0
        else:
            tweak = 1
        plots(x,y,show=0,hold=0,stylestr=['b','r','g','k','m'],leglabels=leglabels,legloc=0,titlestr='Model {0!s}'.format(k),xstr='Parameter set',ystr='Proportion of tracks',xticklabels=xticklabels,fname=fname,tweak=tweak)
