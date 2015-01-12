from patternmatch2 import matchPattern 

def testme():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED

    # EXAMPLE 0
    outedges=[(1,4),(),(3,),(5,),(5,),(0,)]
    walldomains=[]
    pattern=[]
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == )
