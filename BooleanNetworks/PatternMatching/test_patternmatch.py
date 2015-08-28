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

from patternmatch import matchPattern
import preprocess as pp
import fileparsers as fp
import testcases as tc
from walllabels import makeWallInfo

def testme(showme=1):
    # find all matches
    test0(showme,findallmatches=1)
    test1(showme,findallmatches=1)
    test2(showme,findallmatches=1)
    test3(showme,findallmatches=1)
    test4(showme,findallmatches=1)
    test5(showme,findallmatches=1)
    test6(showme,findallmatches=1)
    test7(showme,findallmatches=1)
    test8(showme,findallmatches=1)
    # find first match only
    test0(showme,findallmatches=0)
    test1(showme,findallmatches=0)
    test2(showme,findallmatches=0)
    test3(showme,findallmatches=0)
    test4(showme,findallmatches=0)
    test5(showme,findallmatches=0)
    test6(showme,findallmatches=0)
    test7(showme,findallmatches=0)
    test8(showme,findallmatches=0)

def test0(showme=1,findallmatches=1):
    wallinfo = makeWallInfo(*tc.test0())

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(0, 1, 4, 6, 5, 2, 0), (3, 4, 6, 5, 3)])
    if showme and not findallmatches: print match[0] in [(0, 1, 4, 6, 5, 2, 0), (3, 4, 6, 5, 3)]

    pattern=['um','md'] #intermediate extrema
    match = matchPattern(pattern,wallinfo,cyclic=0,findallmatches=findallmatches)
    if showme: print 'None' in match

    pattern=['ud','um','Mu'] # acyclic 
    match = matchPattern(pattern,wallinfo,cyclic=0,findallmatches=findallmatches)
    if showme: print match==[(1,4,6)]

def test1(showme=1,findallmatches=1):
    wallinfo = makeWallInfo(*tc.test1())

    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print match==[(0, 1, 3, 2, 0)]

    pattern=['md','um','Mu','dM','Md'] # 'Md' DNE in graph
    match = matchPattern(pattern,wallinfo,cyclic=0,findallmatches=findallmatches)
    if showme: print 'None' in match 

    pattern=['md','Mu','dM','md'] # intermediate extrema
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test2(showme=1,findallmatches=1):
    wallinfo = makeWallInfo(*tc.test2())

    pattern=['dM','md','um','Mu','dM']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(2,0,1,3,2),(2,0,1,4,6,5,2)])
    if showme and not findallmatches: print match[0] in [(2,0,1,3,2),(2,0,1,4,6,5,2)]

    pattern=['Mu','dM','md','um','Mu']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(3,2,0,1,3),(6,5,2,0,1,4,6)])
    if showme and not findallmatches: print match[0] in [(3,2,0,1,3),(6,5,2,0,1,4,6)] 

    pattern=['um','Mu'] #acyclic
    match = matchPattern(pattern,wallinfo,cyclic=0,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(1,4,6),(1,3)])
    if showme and not findallmatches: print match[0] in [(1,4,6),(1,3)]

def test3(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test3()
    wallinfo = makeWallInfo(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin,originalpatterns=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0][0],wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print match==[(0,2,4,5,3,1,0)]
    match = matchPattern(patterns[1][0],wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test4(showme=1,findallmatches=1):
    wallinfo = makeWallInfo(*tc.test4())
    pattern=['md','um','Mu','dM','md']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(1,0,2,5,6,4,1),(1,3,6,4,1)])
    if showme and not findallmatches: print match[0] in [(1,0,2,5,6,4,1),(1,3,6,4,1)]

    pattern=['mdu','umu','Muu','dMu','mdu']
    match = matchPattern(pattern,wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test5(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test5()
    wallinfo = makeWallInfo(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin,originalpatterns=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    match = matchPattern(patterns[0][0],wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme and findallmatches: print set(match)==set([(4, 8, 10, 5, 2, 1, 4), (0, 3, 7, 9, 10, 5, 2, 1, 0), (3, 7, 9, 10, 5, 2, 1, 0, 3), (4, 6, 7, 9, 10, 5, 2, 1, 4)])
    if showme and not findallmatches: print match[0] in [(4, 8, 10, 5, 2, 1, 4), (0, 3, 7, 9, 10, 5, 2, 1, 0), (3, 7, 9, 10, 5, 2, 1, 0, 3), (4, 6, 7, 9, 10, 5, 2, 1, 4)]
    match = matchPattern(patterns[1][0],wallinfo,cyclic=1,findallmatches=findallmatches)
    if showme: print 'None' in match

def test6(showme=1,findallmatches=1):
    outedges,walldomains,varsaffectedatwall,varnames,threshnames=tc.test6()
    wallinfo = makeWallInfo(outedges,walldomains,varsaffectedatwall)
    patternnames,patternmaxmin,originalpatterns=fp.parsePatterns()
    patterns=pp.translatePatterns(varnames,patternnames,patternmaxmin,cyclic=1)
    solutions=[[(0, 13, 9, 2, 12, 7, 0), (0, 3, 15, 11, 6, 2, 12, 7, 0), (0, 3, 15, 5, 9, 2, 12, 7, 0), (0, 3, 10, 16, 6, 2, 12, 7, 0)],[(8,4,16,6,2,12,7,0,8)],[(14,4,16,6,14)],None,[(1,4,16,6,2,12,1)],None]
    patterns=[p for pat in patterns for p in pat]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,wallinfo,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme and findallmatches: print set(match)==set(s)
            if showme and not findallmatches: print match[0] in s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def test7(showme=1,findallmatches=1):
    tc.test7()
    patterns,originalpatterns,wallinfo = pp.preprocess(cyclic=1)
    solutions=[None,None,[(1,2,3,4,5,0,1)],[(4,5,0,1,2,3,4)]]
    patterns=[p for pat in patterns for p in pat]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,wallinfo,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme: print match==s
        else:
            if showme: print 'None' in match and 'Pattern' in match

def test8(showme=1,findallmatches=1):
    tc.test8()
    patterns,originalpatterns,wallinfo = pp.preprocess(cyclic=1)
    solutions=[[(1,2,6,0,1),(1, 3, 4, 5, 6, 0, 1)]]*4+[None]*4
    patterns=[p for pat in patterns for p in pat]
    for p,s in zip(patterns,solutions):
        match = matchPattern(p,wallinfo,cyclic=1,findallmatches=findallmatches)
        if s:
            if showme and findallmatches: print set(match)==set(s)
            if showme and not findallmatches: print match[0] in s
        else:
            if showme: print 'None' in match and 'Pattern' in match


if __name__=='__main__':
    testme()
