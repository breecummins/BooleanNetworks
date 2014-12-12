function orders = main(diff12,diff34)

    warning off
    reset(symengine)

	% The ultimate goal of this function is to find all possible linear orders 
    % for the 4D multiplicative case. It is not complete as of 10/24/14.

	% The following function call creates a partial order for the 4D multiplicative case 
    % using the node numbering given by Zane.
    % The lattice with node numbering and equations is in 4DimLatticeWithMult.png. 
    % diff12 = 1 implies b1-a1 < b2-a2, and 0 implies the opposite order. 
    % Analogous for diff34.
    partialorder = {  {1,[2,3,4,9]}, {2,[5,6,10]}, {3,[5,7,11]}, {4,[6,7,12]}, {5,[8,13]}, {6,[8,14]}, {7,[8,15]}, {8,[16]}, {9,[10,11,12]}, {10,[13,14]}, {11,[13,15]}, {12,[14,15]}, {13,[16]}, {14,[16]}, {15,[16]}, {16,[]} };
    [partialorder, algexp, C, D] = makedgraph(partialorder,diff12,diff34);

    unknownpairs = {};
    for k = 1:length(partialorder)
        for m = k+1:length(partialorder)
            if all(partialorder{k}{1} ~= partialorder{m}{2}) && all(partialorder{m}{1} ~= partialorder{k}{2})
                unknownpairs{end+1} = [k,m];
            end
        end
    end

    celldisp(unknownpairs)
    % length(unknownpairs)

    % celldisp(partialorder)

	% % Now we add the edges to the partial order induced by the constraints.  
	% partialorder = symbolicdifferences(partialorder, algexp);
 %    celldisp(partialorder)

	% Now return all total orders that are consistent with the partial order and the 
    % algebraic expressions at the nodes.
    % orders = linearextensions(partialorder,algexp);
    % disp(length(orders))