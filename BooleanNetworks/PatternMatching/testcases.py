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

import subprocess

def test0():
    # X : X(~Z) : X Z
    # Z : X : X
    # NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(0.5,1),(1,0.5),(1,1.5),(1.5,1),(2,0.5),(2,1.5),(2.5,1)]
    outedges=[(1,),(4,),(0,),(4,),(6,),(2,3),(5,)]
    varsaffectedatwall=[0]*len(outedges)
    for k in [4,5]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test1():
    # X : X(~Z) : X Z
    # Z : X : X
    # HAS STEADY STATE AND WHITE WALL, SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(1.5,1),(2,0.5),(2,1.5),(2.5,1)]
    outedges=[(1,),(3,),(0,),(2,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [0,3]:
        varsaffectedatwall[k]=0
    for k in [1,2]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test2():
    # X : X(~Z) : Z X
    # Z : X : X
    # NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(0.5,1),(1,0.5),(1,1.5),(1.5,1),(2,0.5),(2,1.5),(2.5,1)]
    outedges=[(1,),(4,3),(0,),(2,),(6,),(2,),(5,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [0,3,4,5,6]:
        varsaffectedatwall[k]=0
    for k in [1,2]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test3():
    # X : ~Z : Y
    # Y : ~X : Z
    # Z : ~Y : X
    # 3D EXAMPLE, NEGATIVE FEEDBACK, NO STEADY STATES (ONLY SADDLES)
    walldomains=[(1.5,1,0.5),(1,1.5,0.5),(1.5,0.5,1),(0.5,1.5,1),(1,0.5,1.5),(0.5,1,1.5)]
    outedges=[(2,),(0,),(4,),(1,),(5,),(3,)]
    varsaffectedatwall=[2,1,0,0,1,2]
    varnames=['X','Y','Z']
    threshnames=[['Y'],['Z'],['X']]
    f=open('patterns.txt','w')
    f.write('Z min, X max, Y min, Z max, X min, Y max\n Z min, X min, Y max, Y min, Z max, X max')
    f.close()
    return outedges,walldomains,varsaffectedatwall,varnames,threshnames

def test4():
    # X1 : (X1)(~X2) : X1 X2
    # X2 : (X2)(X1) : X2 X1
    # 2D EXAMPLE WITH TWO THRESHOLDS EACH, HAS CYCLES AND 1 OFF FIXED POINT
    walldomains=[(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2,2.5),(2.5,1),(2.5,2)]
    outedges=[(2,),(0,3),(5,),(6,),(1,),(6,),(4,)]
    varsaffectedatwall=[1,0,1,1,1,1,0]
    return outedges,walldomains,varsaffectedatwall

def test5():
    # X1 : (X2)(~X3) : X2
    # X2 : X1 : X1 X3
    # X3 : X2 : X1
    # 3D EXAMPLE WHERE ONE VAR HAS 2 THRESHOLDS, NO FIXED POINT
    walldomains=[(0.5,1,1.5),(0.5,2,1.5),(1,2.5,1.5),(0.5,0.5,1),(0.5,1.5,1),(1.5,2.5,1),(0.5,1,0.5),(1,0.5,0.5),(1,1.5,0.5),(1.5,1,0.5),(1.5,2,0.5)]
    outedges=[(3,),(0,4),(1,),(7,),(6,8),(2,),(7,),(9,),(10,),(10,),(5,)]
    varsaffectedatwall=[0,2,1,0,0,0,0,1,1,0,2]
    f=open('patterns.txt','w')
    f.write('X1 min, X2 min, X3 min, X1 max, X2 max, X3 max\n X1 min, X2 min, X1 max, X3 min, X2 max, X3 max')
    f.close()
    varnames=['X1','X2','X3']
    threshnames=[['X2'],['X1','X3'],['X1']]
    return outedges,walldomains,varsaffectedatwall,varnames,threshnames

def test6():
    # X1 : (X1)(~X3) : X1 X2 X3
    # X2 : X1 : X3
    # X3 : X1(~X2) : X1
    # 3D EXAMPLE WHERE ONE VAR HAS 3 THRESHOLDS, CHOSE PARAM SET WITH FIXED POINT, 2 WHITE WALLS
    walldomains=[(2,0.5,0.5),(2,1.5,0.5),(2,1.5,1.5),(3,0.5,0.5),(3,1.5,0.5),(3,0.5,1.5),(3,1.5,1.5),(1.5,1,0.5),(2.5,1,0.5),(2.5,1,1.5),(3.5,1,0.5),(3.5,1,1.5),(1.5,1.5,1),(2.5,0.5,1),(2.5,1.5,1),(3.5,0.5,1),(3.5,1.5,1)]
    outedges=[(3,8,13),(4,),(12,),(10,15),(16,),(9,),(2,14),(0,),(4,),(2,14),(16,),(6,),(1,7),(9,),(4,),(5,11),(6,)]
    varsaffectedatwall=[1]*3 + [2]*9 + [0]*5
    f=open('patterns.txt','w')
    f.write('X2 min, X1 max, X3 max, X2 max, X1 min, X3 min, X2 min\n X3 max, X3 min, X1 max, X3 max, X2 max, X1 min, X3 min, X2 min\n X1 min, X3 min, X1 max, X3 max\n X2 min, X3 min, X1 max, X3 max, X2 max, X1 min\n X2 min, X3 min, X1 min, X3 max, X2 max, X1 max')
    f.close()
    varnames=['X1','X2','X3']
    threshnames=[['X1','X2','X3'],['X3'],['X1']]
    return outedges,walldomains,varsaffectedatwall,varnames,threshnames

def test7():
    # dsgrn output, repressilator example like test 3
    subprocesscall(["dsgrn network networks/3D_Example.txt domaingraph > dsgrn_domaincells.json".format(specfile)],shell=True)
    subprocesscall(["dsgrn network networks/3D_Example.txt domaingraph json 13 > dsgrn_domaingraph.json".format(specfile,int(param))],shell=True)
    subprocess.call(["dsgrn network networks/3D_Example.txt analyze morseset 0 13 >dsgrn_output.json"],shell=True)
    f=open('patterns.txt','w')
    f.write('Z min, X min, Y min, Z max, X max, Y max\n X max, Y max, Z max, X min, Y min, Z min\n X min, Y max, Z min, X max, Y min, Z max\n X max, Y min, Z max, X min, Y max, Z min')
    f.close()

def test8():
    # dsgrn output, 5D Cycle
    subprocesscall(["dsgrn network networks/5D_Cycle.txt domaingraph > dsgrn_domaincells.json".format(specfile)],shell=True)
    subprocesscall(["dsgrn network networks/5D_Cycle.txt domaingraph json 847328 > dsgrn_domaingraph.json".format(specfile,int(param))],shell=True)
    subprocess.call(["dsgrn network networks/5D_Cycle.txt analyze morseset 3 847328 >dsgrn_output.json"],shell=True)
    f=open('patterns.txt','w')
    f.write('X3 max, X4 max, X3 min, X4 min\n X3 max, X4 min, X3 min, X4 max')
    f.close()