import numpy as np

def translateToOrthants(timeseries):
    trajectory = np.int8(timeseries > 0)
    short = trajectory[0,:].reshape((1,timeseries.shape[1]))
    for k in range(1,timeseries.shape[0]):
        if np.any(trajectory[k,:] != short[-1,:]):
            short = np.vstack([short,trajectory[k,:]])
    return short

def translateToOrthants(timeseries):
    trajectory = np.int8(timeseries > 0)
    short = trajectory[0,:].reshape((1,timeseries.shape[1]))
    for k in range(1,timeseries.shape[0]):
        if np.any(trajectory[k,:] != short[-1,:]):
            short = np.vstack([short,trajectory[k,:]])
    return short

def encodeInts(track,N=5):
    '''
    Takes an nxN numpy array of ones and zeros and returns an n-tuple of ints.
    Each int is between 0 and 2**N -1, the int representation of each row
    read as a binary number.

    '''
    binstr = ''.join([str(i) for i in track.flat])
    return tuple([int(binstr[N*k:N*(k+1)],2) for k in range(track.shape[0])])

def decodeInts(tupints,N=5):
    '''
    Takes a tuple of integers in the range 0-31 and constructs an nx5 numpy
    array. Each row is the binary representation of the corresponding int.

    '''
    los = map(lambda b: bin(b)[2:].zfill(N),tupints)
    return np.array([[int(i[j]) for j in range(N)] for i in los])


