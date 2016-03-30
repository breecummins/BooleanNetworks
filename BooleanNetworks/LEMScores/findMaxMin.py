import parseLEMscores as LEM
import numpy as np
np.set_printoptions(linewidth=100)
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
matplotlib.rc('font', **font)

genelist,timeseries=LEM.generateMasterList()
requestedgenes = [248,366,176]#[248,100,118,345,14,154,411,17,340,366,176,406,111,288,171]
requestedtimeseries=[]
for g in requestedgenes:
    M=max(timeseries[g])
    requestedtimeseries.append([t/M for t in timeseries[g]])
extrema=[[] for _ in range(len(requestedtimeseries[0]))]
for ts in requestedtimeseries:
    M=ts.index(max(ts))
    m=ts.index(min(ts))
    for i in range(len(ts)):
        extrema[i].append(1 if i==M else -1 if i==m else 0)

print np.array([requestedgenes]+extrema).transpose()

NUM_COLORS = 3

cm = plt.get_cmap('gist_rainbow')
# cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
# scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.set_color_cycle([scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
for name,rts in zip(requestedgenes,requestedtimeseries):
    plt.plot(range(0,61,3),rts,label=str(name),linewidth=2)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
plt.xlabel('time')
plt.ylabel('expression')
plt.show()
