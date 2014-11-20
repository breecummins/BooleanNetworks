from patternmatch8 import matchPattern 

# ASSUME ALL WALLS UNIQUE, ASSUME GIVEN PATTERN EXISTS EXACTLY IN GRAPH

# EXAMPLE 0
outedges=[(1,),(2,),(3,),(0,)]
walllabels=['uuu','uMu','udu','umu']
pattern=['uuu','uMu','udu','umu','uuu']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(0,1,2,3,0)])

# EXAMPLE 0
outedges=[(1,),(2,),(3,),(0,)]
walllabels=['uuu','uMu','udu','umu']
pattern=['uMu','udu','umu','uuu','uMu'] # permuted pattern
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(1,2,3,0,1)])

# ASSUME ALL WALLS UNIQUE, PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH, BUT OTHER WALLS ARE ALLOWED)

# EXAMPLE 1
outedges=[(1,),(2,3),(3,),(0,)]
walllabels=['uuu','uMu','udu','umu']
pattern=['uMu','umu','uMu'] # permuted pattern
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(1, 2, 3, 0, 1), (1, 3, 0, 1)])

# EXAMPLE 2
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
pattern=['uuu','uMu','udu','umu','uuu']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(0,2,5,6,0)])

# EXAMPLE 2
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
pattern=['uMu','udu','umu','uuu','uMu'] # permuted pattern
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(2,5,6,0,2)])

# EXAMPLE 2
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
pattern=['uMu','umu','uuM']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(2,5,6,0,1)])

# EXAMPLE 2: THE FOLLOWING PATTERN DNE
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
pattern=['uMu','udu','udM','uMd','udd','Mdd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)

# EXAMPLE 2: THE FOLLOWING PATTERN DNE
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd']
pattern=['udM','udd','uMd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)

# EXAMPLE 3: THE FOLLOWING PATTERN DNE
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(9,),(10,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
pattern=['udM','udd','uMd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)

# EXAMPLE 3
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(8,9),(10,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
pattern=['umu','uuM','uMd','Mdd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(6,0,1,3,7,8,9)])

# EXAMPLE 3: THE FOLLOWING PATTERN DNE
outedges=[(1,2),(3,),(4,5),(7,),(8,),(4,6),(0,),(8,),(9,),(10,),(8,)]
walllabels=['uuu','uuM','uMu','uud','udM','udu','umu','uMd','udd','Mdd','mdd']
pattern=['umu','uuM','uMd','Mdd','mdd','udM']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)

# PATTERN CONTAINS ALL EXTREMA (INTERMEDIATE EXTREMA NOT ALLOWED IN PATH MATCH), UNIQUENESS NOT REQUIRED

# EXAMPLE 4
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uuM','uum','uMu','umu','uuM']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(1, 3, 12, 2, 5, 6, 0, 11, 1)])

# EXAMPLE 4
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uuM','uMd','Mdd','mdd','Mdd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(1, 3, 7, 9, 10, 9)])

# EXAMPLE 4: THE FOLLOWING PATTERN DNE
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uuM','uMd','Mdd','mdd','Mdd','mdd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)# == [(1, 3, 7, 9, 10, 9, 10)]) # but search should fail

# EXAMPLE 4
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uMu','umu','uuM','uMd','udd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(2, 5, 6, 0, 11, 1, 4, 8)])

# EXAMPLE 4: THE FOLLOWING PATTERN DNE
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uMu','umu','uuM','uMd','Mdd','umd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match is None or 'None' in match)

# EXAMPLE 4
outedges=[(11,2),(3,4),(5,),(7,12),(8,),(6,),(0,),(9,),(8,),(10,),(9,13),(1,),(2,),(3,)]
walllabels=['uuu','uuM','uMu','uud','uMd','udu','umu','uMd','udd','Mdd','mdd','uuu','uum','umd']
pattern=['uMd','Mdd','mdd','umd']
match = matchPattern(pattern,walllabels,outedges,suppress=1)
print(match == [(7, 9, 10, 13)])
