function g = makedgraph()
	% Saves Zane's graph as a 0-1 matrix. See main.m for more detail.
	g = zeros(16);
	g(1,:) = 1;
	g(2,[5,6,10]) = 1;
	g(3,[5,7,11]) = 1;
	g(4,[6,7,12]) = 1;
	g(5,[8,13]) = 1;
	g(6,[8,14]) = 1;
	g(7,[8,15]) = 1;
	g([8,13,14,15],16) = 1;
	g(9,[10,11,12]) = 1;
	g(10,[13,14]) = 1;
	g(11,[13,15]) = 1;
	g(12,[14,15]) = 1;
	
	% The following function call adds transitive relationships to the matrix g, using a 
    % breadth-first path search on the graph. 
    g = transitiverelationships(g);
end

