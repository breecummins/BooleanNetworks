import subprocess 
import json

def exists_FC_XC(jsonparsed):
    fc=False
    xc=False
    for morseset, a in enumerate(jsonparsed["annotations"]):
        if a[0][:2] == "FC":
            fc=True
        elif a[0][:2] == 'XC':
            xc=True
        if fc*xc:
            return morseset
    return False

def exists_FC(jsonparsed):
    for morseset, a in enumerate(jsonparsed["annotations"]):
        if a[0][:2] == "FC":
            return morseset
    return False

def all_FC(jsonparsed):
    allmorsesets=[]
    for morseset, a in enumerate(jsonparsed["annotations"]):
        if a[0] == "FC":
            allmorsesets.append(morseset)
    return tuple(allmorsesets) if allmorsesets else False

def is_FC(jsonparsed):
    a = jsonparsed["annotations"]
    if len(a) == 1 and a[0][0]=="FC":
        return 0
    return False

def is_FP_clock(jsonparsed):
    anns = [a[0] for a in jsonparsed["annotations"]]
    if len(anns) == 2 and (set(anns) == set(["FC","FP"])):
        morseset=anns.index("FC")
        return morseset
    return False

def scan(fname="networks/6D_OneWayForcing.txt",smallestparam=0,largestparam=10**6,getMorseSet=exists_FC,firstonly=True):
    params=[]
    for p in irange(smallestparam,largestparam):
        jsonparsed=json.loads(subprocess.check_output(["dsgrn network "+fname+" morsegraph json "+str(p)],shell=True))
        morseset= getMorseSet(jsonparsed)
        if morseset is not False:
            if firstonly:
                return p,morseset
            else:
                params.append((p,morseset))
    return params

def irange(start, stop=None, step=1):
    """ Generator for a list containing an arithmetic progression of integers.
        range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0.
        When step is given, it specifies the increment (or decrement).
        For example, range(4) returns [0, 1, 2, 3].  The end point is omitted!
        These are exactly the valid indices for a list of 4 elements.

        From https://wiki.python.org/moin/RangeGenerator. Does not have C long 
        integer overflow issue that xrange does.
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
    # print scan("networks/6D_TwoWayForcing.txt",46656,exists_FC,True)
    # print scan("networks/6D_OneWayForcing.txt",5832,exists_FC,False)
    from cProfile import runctx
    # runctx('scan("networks/6D_OneWayForcing.txt",5832,exists_FC,False)',globals(),locals())
    print('check_output')
    runctx('for _ in range(1000): subprocess.check_output(["ls"],shell=True)',globals(),locals())
    print('check_output + dsgrn')
    runctx('for p in range(1000): subprocess.check_output(["dsgrn network networks/6D_OneWayForcing.txt morsegraph json "+str(p)],shell=True)',globals(),locals())
    print('check_output + dsgrn + json')
    runctx('for p in range(1000): json.loads(subprocess.check_output(["dsgrn network networks/6D_OneWayForcing.txt morsegraph json "+str(p)],shell=True))',globals(),locals())



