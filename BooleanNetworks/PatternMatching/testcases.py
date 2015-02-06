def test0():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED
    # X : X(~Z) : X Z
    # Z : X : X
    # EXAMPLE 0, NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    outedges=[(5,),(3,),(5,),(5,),(3,),(10,),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,5,6,8,13]:
        varsaffectedatwall[k]=0
    for k in [10,11]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test1():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED
    # X : X(~Z) : X Z
    # Z : X : X
    # EXAMPLE 1, HAS STEADY STATE (WALL 17) AND WHITE WALL (WALL 5), SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5),(0.5,0.5)]
    outedges=[(17,),(3,),(17,),(17,),(3,),(10,17),(3,),(10,),(10,),(6,),(13,),(6,8),(13,),(11,),(11,),(13,),(11,),(17,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,5,6,8,13]:
        varsaffectedatwall[k]=0
    for k in [10,11]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test2():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED
    # X : X(~Z) : Z X
    # Z : X : X
    # EXAMPLE 2, NO STEADY STATES, SEE NOTES FOR FLOW ACROSS WALLS
    walldomains=[(0,0.5),(0,1.5),(0.5,0),(0.5,1),(0.5,2),(1,0.5),(1,1.5),(1.5,0),(1.5,1),(1.5,2),(2,0.5),(2,1.5),(2.5,0),(2.5,1),(2.5,2),(3,0.5),(3,1.5)]
    outedges=[(5,),(3,),(5,),(5,),(3,),(8,10),(3,),(10,),(6,),(6,),(13,),(6,),(13,),(11,),(11,),(13,),(11,)]
    varsaffectedatwall=[-1]*len(outedges)
    for k in [3,8,10,11,13]:
        varsaffectedatwall[k]=0
    for k in [5,6]:
        varsaffectedatwall[k]=1
    return outedges,walldomains,varsaffectedatwall

def test3():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED
    # X : ~Z : Y
    # Y : ~X : Z
    # Z : ~Y : X
    # EXAMPLE 3, NEGATIVE FEEDBACK, NO STEADY STATES (ONLY SADDLES), SEE NOTES FOR FLOW ACROSS WALLS
    # INCLUDING BOUNDARY WALLS
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

if __name__=='__main__':
    test3()
