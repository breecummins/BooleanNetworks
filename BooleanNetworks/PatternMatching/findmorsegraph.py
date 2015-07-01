from subprocess import call
import os
import json

def exists_FC_XC(fname="dsgrn_morsegraph.json"):
    parsed = json.load(open(fname),strict=False)
    fc=False
    xc=False
    for a in parsed["annotations"]:
        if a[0][:2] == "FC":
            fc=True
        elif a[0][:2] == 'XC':
            xc=True
        if fc*xc:
            return True
    return False

def exists_FC(fname="dsgrn_morsegraph.json"):
    parsed = json.load(open(fname),strict=False)
    for a in parsed["annotations"]:
        if a[0][:2] == "FC":
            return True
    return False

def scan(fname="~/GIT/DSGRN/networks/6D_OneWayForcing.txt",largestparam=10**6,checkfor=exists_FC,firstonly=True):
    call(["dsgrn network "+os.path.expanduser(fname)],shell=True)
    params=[]
    for p in irange(largestparam):
        call(["dsgrn morsegraph json "+str(p)+" >dsgrn_morsegraph.json"],shell=True)
        if checkfor() is True:
            if firstonly:
                return p
            else:
                params.append(p)
    return params

def irange(start, stop=None, step=1):
    """ Generator for a list containing an arithmetic progression of integers.
        range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0.
        When step is given, it specifies the increment (or decrement).
        For example, range(4) returns [0, 1, 2, 3].  The end point is omitted!
        These are exactly the valid indices for a list of 4 elements.

        From https://wiki.python.org/moin/RangeGenerator. Does not have C long issue 
        that xrange does.
    """
    if step == 0:
        raise ValueError("irange() step argument must not be zero")

    if stop is None:
        stop = start
        start = 0
    continue_cmp = (step < 0) * 2 - 1

    while cmp(start, stop) == continue_cmp:
        yield start
        start += step


if __name__=='__main__':
    print scan("~/GIT/DSGRN/networks/6D_TwoWayForcing.txt",46656,exists_FC_XC,False)




