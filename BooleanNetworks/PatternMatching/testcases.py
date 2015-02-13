def test0():
    # X : X(~Z) : X Z
    # Z : X : X
    # NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS, BOUNDARY WALLS INCLUDED
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,5,6,8,13]:
        varsaffectedatwall[k]=0
    for k in [10,11]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test1():
    # X : X(~Z) : X Z
    # Z : X : X
    # HAS STEADY STATE (WALL 17) AND WHITE WALL (WALL 5), SEE NOTES FOR FLOW ACROSS WALLS, BOUNDARY WALLS INCLUDED
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5),(0.5,0.5)]
    outedges=[(17,),(3,),(17,),(17,),(3,),(10,17),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,),(17,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,5,6,8,13]:
        varsaffectedatwall[k]=0
    for k in [10,11]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test2():
    # X : X(~Z) : Z X
    # Z : X : X
    # NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS, BOUNDARY WALLS INCLUDED
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    outedges=[(5,),(3,),(5,),(5,),(3,),(8,10),(3,),(10,),(6,),(6,),(13,),(6,),(13,),(11,),(11,),(13,),(11,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,8,10,11,13]:
        varsaffectedatwall[k]=0
    for k in [5,6]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test3():
    # X : ~Z : Y
    # Y : ~X : Z
    # Z : ~Y : X
    # 3D EXAMPLE, NEGATIVE FEEDBACK, NO STEADY STATES (ONLY SADDLES), BOUNDARY WALLS INCLUDED
    walldomains=[(1.5,1,0.5),(1,0.5,0.5),(0.5,1,0.5),(1,1.5,0.5),(1.5,0.5,1),(0.5,0.5,1),(0.5,1.5,1),(1.5,1.5,1),(1.5,1,1.5),(1,0.5,1.5),(0.5,1,1.5),(1,1.5,1.5)]+[(1.5,0,0.5),(2,0.5,0.5),(1.5,0.5,0)]+[(1.5,0,1.5),(2,0.5,1.5),(1.5,0.5,2)]+[(0.5,0,1.5),(0,0.5,1.5),(0.5,0.5,2)]+[(0.5,0,0.5),(0,0.5,0.5),(0.5,0.5,0)]+[(1.5,2,0.5),(2,1.5,0.5),(1.5,1.5,0)]+[(1.5,2,1.5),(2,1.5,1.5),(1.5,1.5,2)]+[(0.5,2,1.5),(0,1.5,1.5),(0.5,1.5,2)]+[(0.5,2,0.5),(0,1.5,0.5),(0.5,1.5,0)]
    outedges=[(4,),(4,),(3,),(0,),(9,),(10,),(3,),(0,),(9,),(10,),(6,),(6,)]+[(4,)]*3+[(9,)]*3+[(10,)]*3+[(1,2,5)]*3+[(0,)]*3+[(7,8,11)]*3+[(6,)]*3+[(3,)]*3
    varsaffectedatwall=[2,1,2,1,0,0,0,0,2,1,2,1]+[-1]*24
    f=open('patterns.txt','w')
    f.write('Z min, X max, Y min, Z max, X min, Y max\n Z min, X min, Y max, Y min, Z max, X max')
    f.close()
    f=open('variables.txt','w')
    f.write('0 X\n 1 Y\n 2 Z')
    f.close()
    f=open('equations.txt','w')
    f.write('X : ~Z : Y\n Y : ~X : Z\n Z : ~Y : X')
    f.close()
    return outedges,walldomains,varsaffectedatwall

def test4():
    # X1 : (X1)(~X2) : X1 X2
    # X2 : (X2)(X1) : X2 X1
    # 2D EXAMPLE WITH TWO THRESHOLDS EACH, HAS CYCLES AND 1 OFF FIXED POINT, BOUNDARY WALLS NOT INCLUDED
    walldomains=[(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1,2.5),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2,2.5),(2.5,1),(2.5,2)]
    outedges=[(),(0,),(7,),(0,),(1,),(7,),(5,8),(10,),(11,),(4,6),(11,),(9,)]
    varsaffectedatwall=[1,0,0,0,0,1,0,1,1,1,1,0]
    return outedges,walldomains,varsaffectedatwall

def test5():
    # X1 : (X2)(~X3) : X2
    # X2 : X1 : X1 X3
    # X3 : X2 : X1
    # 3D EXAMPLE WHERE ONE VAR HAS 2 THRESHOLDS, NO FIXED POINT, BOUNDARY WALLS NOT INCLUDED
    walldomains=[(0.5,1,1.5),(0.5,2,1.5),(1,0.5,1.5),(1,1.5,1.5),(1,2.5,1.5),(1.5,1,1.5),(1.5,2,1.5),(0.5,0.5,1),(0.5,1.5,1),(0.5,2.5,1),(1.5,0.5,1),(1.5,1.5,1),(1.5,2.5,1),(0.5,1,0.5),(0.5,2,0.5),(1,0.5,0.5),(1,1.5,0.5),(1,2.5,0.5),(1.5,1,0.5),(1.5,2,0.5)]
    outedges=[(7,),(0,8),(7,),(0,8),(1,),(3,6,11),(4,),(15,),(13,16),(1,),(18,),(19,),(4,),(15,),(13,16),(18,),(19,),(12,),(19,),(12,)]
    varsaffectedatwall=[0,2,1,1,1,0,2,0,0,0,0,0,0,0,2,1,1,1,0,2]
    f=open('patterns.txt','w')
    f.write('X1 min, X2 min, X3 min, X1 max, X2 max, X3 max\n X1 min, X2 min, X1 max, X3 min, X2 max, X3 max')
    f.close()
    f=open('variables.txt','w')
    f.write('0 X1\n 1 X2\n 2 X3')
    f.close()
    f=open('equations.txt','w')
    f.write('X1 : (X2)(~X3) : X2\n X2 : X1 : X1 X3\n X3 : X2 : X1')
    f.close()
    return outedges,walldomains,varsaffectedatwall

def test6():
    # X1 : (X1)(~X3) : X1 X2 X3
    # X2 : X1 : X3
    # X3 : X1(~X2) : X1
    # 3D EXAMPLE WHERE ONE VAR HAS 3 THRESHOLDS, CHOSE PARAM SET WITH FIXED POINT, 2 WHITE WALLS, BOUNDARY WALLS NOT INCLUDED
    walldomains=[(1,0.5,0.5),(1,1.5,0.5),(1,0.5,1.5),(1,1.5,1.5),(2,0.5,0.5),(2,1.5,0.5),(2,0.5,1.5),(2,1.5,1.5),(3,0.5,0.5),(3,1.5,0.5),(3,0.5,1.5),(3,1.5,1.5),(0.5,1,0.5),(0.5,1,1.5),(1.5,1,0.5),(1.5,1,1.5),(2.5,1,0.5),(2.5,1,1.5),(3.5,1,0.5),(3.5,1,1.5),   (0.5,0.5,1),(0.5,1.5,1),(1.5,0.5,1),(1.5,1.5,1),(2.5,0.5,1),(2.5,1.5,1),(3.5,0.5,1),(3.5,1.5,1)]
    outedges=[(4,20,22),(5,12,14),(),(13,21),(8,16,24),(9,),(2,),(3,15,23),(18,26),(27,),(6,17),(7,25),(20,),(),(4,22),(2,),(9,),(7,25),(27,),(11,),(),(12,),(2,),(5,14),(6,17),(9,),(10,19),(11,)]
    varsaffectedatwall=[0]*4 + [1]*4 + [2]*12 + [0]*8
    f=open('patterns.txt','w')
    f.write('X2 min, X1 max, X3 max, X2 max, X1 min, X3 min, X2 min\n X3 max, X3 min, X1 max, X3 max, X2 max, X1 min, X3 min, X2 min\n X1 min, X3 min, X1 max, X3 max\n X2 min, X3 min, X1 max, X3 max, X2 max, X1 min\n X2 min, X3 min, X1 min, X3 max, X2 max, X1 max')
    f.close()
    f=open('variables.txt','w')
    f.write('0 X1\n 1 X2\n 2 X3')
    f.close()
    f=open('equations.txt','w')
    f.write('X1 : (X1)(~X3) : X1 X2 X3\n X2 : X1 : X3\n X3 : (X1)(~X2) : X1')
    f.close()
    return outedges,walldomains,varsaffectedatwall
