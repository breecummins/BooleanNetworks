# The MIT License (MIT)

# Copyright (c) 2015 Breschine Cummins

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import itertools

def makeWallInfo(outedges,walldomains,varsaffectedatwall):
    # This function creates the dictionary used in the core recursive call for the pattern matching.
    inedges=[tuple([j for j,o in enumerate(outedges) if node in o]) for node in range(len(outedges))]   
    # make every triple and the list of associated wall labels; store in dict indexed by (inedge,wall)
    wallinfo={}
    for currentwall,(ie,oe) in enumerate(zip(inedges,outedges)):
       for previouswall,nextwall in itertools.product(ie,oe):
            # construct the wall label for every permissible triple
            triple=(previouswall,currentwall,nextwall)
            inandoutedges=(outedges[previouswall],inedges[currentwall],outedges[currentwall],inedges[nextwall])
            varatwall=varsaffectedatwall[currentwall]
            labels=pathDependentLabelConstruction(triple,inandoutedges,walldomains,varatwall)
            # Put the result in the dictionary.
            key=(previouswall,currentwall)
            value=(nextwall,labels)
            # If the key already exists, append to its list. Otherwise start the list.
            if key in wallinfo:
                wallinfo[key].append(value)
            else:
                wallinfo[key]=[value]
    return wallinfo

def pathDependentLabelConstruction(triple,inandoutedges,walldomains,varatwall):
    # make a label for the given triple
    if triple[1]==triple[2]: # can't handle steady states
        raise RunTimeError('Debug: Wall has a self-loop.')
    walllabels=['']
    # for every variable find allowable letters for triple
    for varind in range(len(walldomains[0])): 
        isvaratwall = varind==varatwall
        varvalues=tuple([walldomains[k][varind] for k in triple])
        # try simple algorithm first
        chars=getChars(isvaratwall,varvalues) 
        if chars is None:
            # now try complex algorithm
            if isvaratwall:
                # use extra information to get the characters when extrema are allowed
                chars=getCharsExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
            else:
                # use extra information to get the characters when extrema are not allowed
                chars=getCharsNoExtrema(*getAdditionalWallInfo(varind,varvalues,inandoutedges,walldomains))
                if chars==[1]:
                    print varind,varvalues,inandoutedges
        # make every combination of characters in the growing labels
        walllabels=[l+c for l in walllabels for c in chars]
    return tuple(walllabels)

def getChars(isvaratwall,(prev,curr,next)):
    chars=None
    if prev<curr<next:
        chars = ['u']
    elif prev>curr>next:
        chars = ['d']
    elif isvaratwall: # extrema allowed
        if prev<curr>next:
            chars=['M'] 
        elif prev>curr<next:
            chars=['m']
    elif not isvaratwall: # extrema not allowed
        if prev<curr>next or prev>curr<next:
            raise ValueError('Debug: Extrema are not allowed for variables that are not affected at threshold.')
        elif prev<curr==next or prev==curr<next:
            chars = ['u']
        elif prev>curr==next or prev==curr>next:
            chars = ['d']
    return chars

def infoFromWalls(varind,varval,wallinds,walldomains):
    # We want the difference between the value at the current wall, varval,
    # and the value at all adjacent walls to have the same sign (or zero,
    # but not all can be zero).
    # return isgreaterthan, islessthan 
    signs = [cmp(varval - walldomains[k][varind],0) for k in wallinds]
    if set([-1,1]).issubset(signs):
        return False,False,True
    elif set([1]).issubset(signs):
        return True,False,False
    elif set([-1]).issubset(signs):
        return False,True,False
    else:
        return False,False,False

def getAdditionalWallInfo(varind,(prevval,currval,nextval),(prev_out,curr_in,curr_out,next_in),walldomains):
    prev_gt_out,prev_lt_out,contradictoryp=infoFromWalls(varind,prevval,prev_out,walldomains)
    curr_gt_in,curr_lt_in,contradictoryci=infoFromWalls(varind,currval,curr_in,walldomains)
    curr_gt_out,curr_lt_out,contradictoryco=infoFromWalls(varind,currval,curr_out,walldomains)
    next_gt_in,next_lt_in,contradictoryn=infoFromWalls(varind,nextval,next_in,walldomains)
    contradictory=[contradictoryp,contradictoryci,contradictoryn,contradictoryco]
    return prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in,contradictory

def getCharsExtrema(prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in,contradictory):
    if (prev_gt_out or curr_lt_in) and (next_gt_in or curr_lt_out):
        chars=['m'] 
    elif (prev_gt_out or curr_lt_in) and not any(contradictory[2:]):
        chars=['m','d'] 
    elif not any(contradictory[:2]) and (next_gt_in or curr_lt_out):
        chars=['m','u'] 
    elif (prev_lt_out or curr_gt_in) and (next_lt_in or curr_gt_out):
        chars=['M'] 
    elif (prev_lt_out or curr_gt_in) and not any(contradictory[2:]):
        chars=['M','u'] 
    elif not any(contradictory[:2]) and (next_lt_in or curr_gt_out):
        chars=['M','d'] 
    else:
        chars=['M','m','d','u']
    return chars

def getCharsNoExtrema(prev_gt_out,prev_lt_out,curr_gt_in,curr_lt_in,curr_gt_out,curr_lt_out,next_gt_in,next_lt_in,contradictory):
    if any(contradictory) or ( (prev_gt_out or curr_lt_in) and (next_gt_in or curr_lt_out) ) or ( (prev_lt_out or curr_gt_in) and (next_lt_in or curr_gt_out) ):
        chars=['d','u']
    elif prev_gt_out or curr_lt_in or next_lt_in or curr_gt_out:
        chars=['d']
    elif prev_lt_out or curr_gt_in or next_gt_in or curr_lt_out:
        chars=['u']
    else:
        chars=['d','u']
    return chars




