import itertools

def nodesAndSigns(listofedges):
    '''
    Expects a list of tuples of the form (source_node_label,target_node_label,activator).
    
    Labels may be strings or numbers, and each unique label should refer to one and only
    one node. Every node must appear at least once as a source and at least once as a 
    target. This is an assumption of the underlying mathematical model, not a code 
    limitation.
    
    The last tuple element activator = 1 for an activating edge 
                                     = 0 for  a repressing edge

    Returns a tuple of unique nodes and two lists of index tuples, one pair of tuples per 
    node. Given node i, one tuple contains the indices of the activating nodes for node i 
    and the other the repressing nodes for node i.

    '''
    sources = []
    targets = []
    activators = []
    for e in listofedges:
        sources.append(e[0])
        targets.append(e[1])
        activators.append(e[2])
    nodes = set(targets)
    # NEW_FEATURE: I think it is only required to have each node be a source; it does not 
    # necessarily also need to be a target. However, target nodes are the only ones that
    # need maps, and there will be need to be code changes because nodestates and nodes 
    # won't have the same length anymore.
    if nodes != set(sources):
        raise ValueError('All nodes must have at least one incoming and one outgoing edge.')
    nodes = tuple(nodes)
    activatorinds = []
    repressorinds = []
    for n in nodes:
        an = []
        rn = [] 
        for k,t in enumerate(targets):
            if n == t:
                ind = nodes.index(sources[k])
                if activators[k]:
                    an.append(ind)
                else:
                    rn.append(ind)
        activatorinds.append(tuple(an))
        repressorinds.append(tuple(rn))
    return nodes,activatorinds,repressorinds

def _makeNodeStates(basestate,allcombos,alldeps):
    '''
    Helper function for makeMap.

    Return a list of all possible states of n binary variables. The list is roughly ordered
    from low to high, where low means that all activators are off and all repressors are on.

    Note: This algorithm will not scale well. Code should be rewritten using generators
    if 2**n is large.

    '''
    return [tuple([int(not(basestate[j])) if alldeps[j] in c else basestate[j] for j in range(len(basestate))]) for c in allcombos]


def _getSingles(acts,reps,nodestates,template):
    '''
    Helper function for makeMap.

    Return the indices of template = None, provided that only one activator is on or 
    (exclusive or) only one repressor is off.

    '''
    return [ j for j in range(len(nodestates)) if template[j] == None and ( (sum(nodestates[j][:len(acts)])==1 and sum(nodestates[j][len(acts):]) == len(reps)) or (sum(nodestates[j][len(acts):])==len(reps)-1 and sum(nodestates[j][:len(acts)])==0) ) ]

def _updateMap(acts,reps,nodestates,tp,ct,inds,perm):
    '''
    Helper function for makeMap.

    perm is a subset of the map associated with nodestates[inds].
    This function records perm in tp and propagates the consequences 
    forward under an additive assumption. Associated with perm are
    parameter constraints for an underlying Hill function model. 
    The minimal set of constraints is recorded in ct.

    '''
    # Record the constraints consistent with this choice of map.
    actcnstrts = [tuple(itertools.compress(acts,nodestates[s][:len(acts)])) for s in inds]
    repcnstrts = [tuple(itertools.compress(reps,[int(not(n)) for n in nodestates[s][len(acts):]])) for s in inds]
    for k,p in enumerate(perm):
        ct.append((actcnstrts[k],repcnstrts[k],p))
    # Figure out which activators are on and which repressors are off for this map choice.
    # Transform the binary nodestate for the activators and for the repressors into
    # integers for comparison later.
    if len(acts) > 0:
        actons = [s for i,s in enumerate(inds) if perm[i] == 1 and sum(nodestates[s][:len(acts)]) >= 1]
        actints = [int(''.join([str(a) for a in n]),2) for n in [nodestates[k][:len(acts)] for k in actons]]
    if len(reps) > 0:
        repoff = [s for i,s in enumerate(inds) if perm[i] == 1 and sum(nodestates[s][len(acts):]) < len(reps)]
        repints = [int(''.join([str(a) for a in n]),2) for n in [nodestates[k][len(acts):] for k in repoff]]
    # Propagate the 'actons' and 'repoff' forward; i.e., if we have (act, act, rep)  
    # and (1,0,1) maps to 1, then everything else with 1 in the first 
    # place ((1,0,0),(1,1,0),(1,1,1)) must map to 1 as well. Likewise, if last place is 
    # a repressor and (0,0,0) maps to 1, then everything else with a 0 in the 
    # last place must map to 1 as well ((1,0,0), etc).
    for k1,t in enumerate(tp):
        if len(acts) > 0:
            baseactint = int(''.join([str(a) for a in nodestates[k1][:len(acts)]]),2)
            if t == None and any([(baseactint & a) == a for a in actints]):
                tp[k1] = 1
        if len(reps) > 0:
            baserepint = int(''.join([str(a) for a in nodestates[k1][len(acts):]]),2)
            if t == None and any([(baserepint | r) == r for r in repints]):
                tp[k1] = 1
    return tp, ct

def _chooseNewInds(acts,reps,nodestates,tp):
    '''
    Helper function for makeMap.

    Return the indices of template = None, provided that only N activators are on or
    N repressors are off, where N is the minimum number of activators 
    on or repressors off (exclusive or).

    '''
    noneinds = [j for j in range(len(tp)) if tp[j]==None]
    if len(acts) > 0:
        actsums = [sum(nodestates[j][:len(acts)]) for j in noneinds]
        minactsums = min([a for a in actsums if a !=0])
    else:
        minactsums = float('inf')
    if len(reps) > 0:
        repsums = [len(reps) - sum(nodestates[j][len(acts):]) for j in noneinds]
        minrepsums = min([r for r in repsums if r !=0])
    else:
        minrepsums = float('inf')
    if minactsums == minrepsums:
        newinds = [j for k,j in enumerate(noneinds) if actsums[k] == minactsums or repsums[k] == minrepsums]
    elif minactsums < minrepsums:
        newinds = [j for k,j in enumerate(noneinds) if actsums[k] == minactsums]
    else:
        newinds = [j for k,j in enumerate(noneinds) if repsums[k] == minrepsums]
    return newinds

def makeMap(acts,reps):
    '''
    Expects two tuples, one with indices for the activators and one for the repressors
    for a single node.

    Returns a set of Boolean maps consistent with an underlying Hill function model. 
    The output nodestates is the domain for the maps - a length 2**n list of tuples 
    containing all possible states of on/off positions of the activators and repressors. 
    The output maps is a list of lists containing a 0 or 1 for every node state.
    The output constraints is a list of lists containing the minimal parameter constraints 
    required for the corresponding Hill function model.

    '''
    # lowest possible state is all activators off and all repressors on
    alldeps = acts+reps
    basestate = [0]*len(acts) + [1]*len(reps)
    # create all possible on/off combination states for dependencies
    allcombos = itertools.chain(*[itertools.combinations(alldeps,n) for n in range(len(alldeps)+1)])
    nodestates = _makeNodeStates(basestate,allcombos,alldeps)

    def recurseMaps(maps,constraints,inds,templ,ctemp):
        # start by taking combinations of 0's and 1's for the given state indices
        for p in itertools.product([1,0],repeat=len(inds)):
            tp = list(templ)
            ct = list(ctemp)
            for k,j in enumerate(inds):
                tp[j] = p[k]
            tp, ct = _updateMap(acts,reps,nodestates,tp,ct,inds,p)
            nonecount = tp.count(None)
            if nonecount == 0:
                # if the map is complete, record it and continue
                maps.append(tp)
                # if the map is all zeros but 1, add constraint that the sum of all amps
                # beat the threshold
                if sum(tp) == 1:
                    ct.append((acts,reps,1))
                constraints.append(ct)
            elif nonecount == 1:
                # if there are two possible maps, record them and continue
                ind = tp.index(None)
                tp0 = list(tp)
                ct0 = list(ct)
                tp0[ind]=0
                tp[ind]=1
                maps.append(tp0)
                maps.append(tp)
                # find the constraints for these last choices
                acton = tuple(itertools.compress(acts,nodestates[ind][:len(acts)]))
                repoff = tuple(itertools.compress(reps,[int(not(n)) for n in nodestates[ind][len(acts):]]))
                ct0.append((acton,repoff,tp0[ind]))
                ct.append((acton,repoff,tp[ind]))
                # if the map is all zeros but 1, add constraint that the sum of all amps
                # beat the threshold
                if sum(tp0) == 1:
                    ct0.append((acts,reps,1))
                # record the constraints
                constraints.append(ct0)
                constraints.append(ct)
            else:
                # There are at least 4 possible maps, have to recurse. 
                # Find the indices of the smallest number of 'on' activators 
                # or 'off' repressors and run the algorithm again.
                newinds = _chooseNewInds(acts,reps,nodestates,tp)
                maps, constraints = recurseMaps(maps,constraints,newinds,tp,ct)
        return maps, constraints

    # make a template with required 0 at lowest state and 1 at highest state
    template = [None]*len(nodestates)
    basestate = tuple(basestate)
    template[nodestates.index(basestate)] = 0
    highstate = tuple([int(not(b)) for b in basestate])
    template[nodestates.index(highstate)] = 1
    # Fill in the rest of the blanks with all allowable combinations of on/off
    # activators and repressors (allowable means consistent with a Hill function model).
    # Also record the constraints each map imposes on the underlying Hill function
    # model parameters.
    if len(nodestates) > 2:
        singleinds = _getSingles(acts,reps,nodestates,template)
        maps, constraints = recurseMaps([],[],singleinds,template,[])
    else:
        maps = [template]
        constraints = [[(acts,reps,1)]]
    return nodestates, maps, constraints

def prettyOutput(nodes,alldeps,nodestates,maps,constraints,tlabel,aalabels,ralabels):
    deps = tuple([nodes[d] for d in alldeps])
    print("{0}".format(deps).replace("'", "")), 
    print('maps:'),
    L = len(str(deps).replace("'", "") + ' maps:')
    l = len(str(nodestates[0]))
    for k in range(1,len(maps)+1):
        if k < len(maps) and k < 9:
            print('{0} '.format(k)),
        elif k < len(maps) and k >= 9:
            print(k),
        else:
            print(k)
    print('-'*((L+3*len(maps))))
    for k,n in enumerate(nodestates):
        print(n),
        for i in range(len(maps)):
            if i == 0 and i < len(maps)-1:
                print(' '*(L-l) +'{0}'.format(maps[i][k])),
            elif i == 0 and i == len(maps)-1:
                print(' '*(L-l) +'{0}'.format(maps[i][k]))
            elif i < len(maps)-1:
                print(' {0}'.format(maps[i][k])),
            else:
                print(' {0}'.format(maps[i][k]))
    print('-'*((L+3*len(maps))))
    print('Constraints:')
    for j,cl in enumerate(constraints):
        print('Map {0}: '.format(j+1)),
        for k,c in enumerate(cl):
            if c[2] == 1:
                symb = ' > '
            else:
                symb = ' <= '
            als = ['{0}'.format(aalabels[alldeps.index(i)]) for i in c[0]]
            rls = ['{0}'.format(ralabels[alldeps.index(i) - len(aalabels)]) for i in c[1]]
            als.extend(rls)
            if len(als) > 1:
                amps = ' + '.join(als)
            else:
                amps = als[0]
            if k < len(cl) - 1:
                print('{0}{1}{2}, '.format(amps,symb,tlabel)),
            else:
                print('{0}{1}{2}'.format(amps,symb,tlabel))
    print('-'*((L+3*len(maps))))

def translateNetworkToMaps(listofedges):
    '''
    Expects a list of tuples of the form (source_node_label,target_node_label,activator).
    
    Labels may be strings or numbers, and each unique label should refer to one and only
    one node. Every node must appear at least once as a source and at least once as a 
    target. This is an assumption of the underlying mathematical model, not a code 
    limitation.
    
    The last tuple element activator = 1 for an activating edge 
                                     = 0 for  a repressing edge

    Outputs acceptable Boolean maps consistent with the input directed graph.

    '''
    nodes,activatorinds,repressorinds = nodesAndSigns(listofedges)
    thresholdlabels = ['r_'+str(n)+' K_'+str(n) for n in nodes]
    actamplabels = [tuple(['A_'+str(n)+'_'+str(nodes[ind]) for ind in activatorinds[k]]) for k,n in enumerate(nodes)]
    repamplabels = [tuple(['B_'+str(n)+'_'+str(nodes[ind]) for ind in repressorinds[k]]) for k,n in enumerate(nodes)]
    nodedeps = []
    nodedepstates = []
    nodemaps = []
    nodeconstraints = []
    for k,n in enumerate(nodes):
        nodestates, maps, constraints = makeMap(activatorinds[k],repressorinds[k])
        print('Node {0}'.format(n))
        prettyOutput(nodes,activatorinds[k]+repressorinds[k],nodestates,maps,constraints,thresholdlabels[k],actamplabels[k],repamplabels[k])
        nodedeps.append(activatorinds[k]+repressorinds[k])
        nodedepstates.append(nodestates)
        nodemaps.append(maps)
        nodeconstraints.append(constraints)
    return nodes,nodedeps,nodedepstates,nodemaps,nodeconstraints
