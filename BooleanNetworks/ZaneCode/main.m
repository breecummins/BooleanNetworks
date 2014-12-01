function orders = main(c12,c34)

    warning on
    reset(symengine)

	% The ultimate goal of this function is to find all possible linear orders 
    % for the 4D multiplicative case. It is not complete as of 10/24/14.

	% The following function call creates a partial order for the 4D multiplicative case 
    % using the node numbering given by Zane.
    % The lattice with node numbering and equations is in 4DimLatticeWithMult.png. 
    % g is a cell array of cell arrays. Each element in g is of the form {i,[j1,j2,...,jn]},
    % meaning that there is a directed edge from i to j1 and to j2, etc., or that i < j1, 
    % i< j2, etc.
    % algexp is a cell array of symbolic expressions for the algebraic labels of each node. 
    % For example, algexp{1} = (a1+a2)*(a3+a4).
    % Also assumptions are set in this function. c12 = 1 implies b1-a1 < b2-a2, and =0
    % implies the opposite order. Analogously for c34.
	[partialorder, algexp] = makedgraph(c12,c34);

	% % Now we add the edges to the partial order induced by the constraints.  
	% partialorder = symbolicdifferences(partialorder, algexp);
 %    celldisp(partialorder)

	% Now return all total orders that are consistent with the partial order and the 
    % algebraic expressions at the nodes.
    % orders = linearextensions(partialorder,algexp);
    % disp(length(orders))