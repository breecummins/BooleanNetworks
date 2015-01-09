from patternmatch import matchPattern 

def testme():
    # PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED

    # EXAMPLE 0
    outedges=[(1,),(2,),(3,),(0,)]
    walllabels=['uuu','uMu','udu','umu']
    pattern=['uMu','umu','uMu']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(1,2,3,0,1)])

    # EXAMPLE 0
    outedges=[(1,),(2,),(3,),(0,)]
    walllabels=['uuu','uMu','udu','umu']
    pattern=['umu','uMu','umu'] # permuted pattern
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(3,0,1,2,3)])

    # EXAMPLE 1
    outedges=[(1,),(2,3),(3,),(0,)]
    walllabels=['uuu','uMu','udu','umu']
    pattern=['uMu','umu','uMu'] # permuted pattern
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(1, 2, 3, 0, 1), (1, 3, 0, 1)])

    # EXAMPLE 2
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','umu','uMu']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(2,5,6,0,2)])

    # EXAMPLE 2
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','umu','uuM']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(2,5,6,0,1)])

    # EXAMPLE 2: THE FOLLOWING PATTERN DNE
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
    pattern=['uMu','udM','uMd','Mdd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 3
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,9),(10,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
    pattern=['umu','uuM','uMd','Mdd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(6,0,1,3,7,8,9)])

    # EXAMPLE 3: THE FOLLOWING PATTERN DNE
    outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(9,),(10,),(8,)]
    walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
    pattern=['umu','uuM','uMd','Mdd','mdd','udM']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 4
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uuM','uum','uMu','umu','uuM']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(1, 3, 12, 2, 5, 6, 0, 11, 1)])

    # EXAMPLE 4
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uuM','uMd','Mdd','mdd','Mdd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(1, 3, 7, 9, 10, 9)])

    # EXAMPLE 4
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uMu','umu','uuM','uMd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(2, 5, 6, 0, 11, 1, 3, 7), (2, 5, 6, 0, 11, 1, 4)])

    # EXAMPLE 4: THE FOLLOWING PATTERN DNE
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uMu','umu','uuM','uMd','Mdd','umd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 4
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uMd','Mdd','mdd','umd']
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(7, 9, 10, 13)])

    # EXAMPLE 4: REPEATING SEQUENCE FAIL
    outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
    walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
    pattern=['uuM','uMd','Mdd','mdd','Mdd','mdd'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)# == [(1, 3, 7, 9, 10, 9, 10)]) # but search should fail

    # EXAMPLE 5: REPEATING SEQUENCE SUCCESS
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uud','uMd','Mdd','mdd','ddd','mdd']
    pattern=['uMd','Mdd','mdd','Mdd','mdd'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(2, 3, 5, 6, 3, 4), (2, 3, 4, 3, 5, 6)])

    # EXAMPLE 5: LENGTH 1 PATTERN
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uud','uMd','Mdd','mdd','ddd','mdd']
    pattern=['mdd'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match == [(4,), (6,)])

    # EXAMPLE 5: PATTERN HAS ELEMENT THAT IS NOT A WALL
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uud','uMd','Mdd','mdd','ddd','mdd']
    pattern=['uMu'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 5: PATTERN ELEMENT LACKS EXTREMUM
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uud','uMd','Mdd','mdd','ddd','mdd']
    pattern=['umd','uud'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 6: WALL LABELS HAVE TOO MANY EXTREMA
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uud','uMm','Mdd','mdd','ddd','mdd']
    pattern=['umd'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

    # EXAMPLE 7: WALL LABELS HAVE THE WRONG CHARS
    outedges=[(1,),(2,),(3,),(4,5),(0,3),(6,),(3,)]
    walllabels=['umd','uua','uMd','Mdd','mdd','ddd','mdd']
    pattern=['umd'] 
    match = matchPattern(pattern,walllabels,outedges,suppress=1)
    # print(match is None or 'None' in match)

