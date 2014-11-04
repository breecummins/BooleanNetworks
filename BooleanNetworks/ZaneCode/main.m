function main()
	% The ultimate goal of this function is to find all possible linear orders 
    % for the 4D multiplicative case. It is not complete as of 10/24/14.

	% The following function call creates a 0-1 matrix representing the partial order 
    % for the 4D multiplicative case using the node numbering given by Zane.
    % The lattice with node numbering and equations is in 4DimLatticeWithMult.png. 
    % In g, if an (i,j) element is 1, this means that the equation in node i is less than the 
    % equation in node j. That is, there is a path in the directed graph from i to j.
	g = makedgraph();

	% The following function call takes a specific ordering of differences 
    % (lowest edges in the lattice) and calculates which previously unknown pairs 
    % are now known, and returns the updated Boolean matrix. 
	c1=1; c2=2; c3=3; c4=4;
	g = addconstraints(g,c1,c2,c3,c4);

	% Now we need an algorithm for determining all consistent sets of orderings of the unknown pairs.
    % Try this one.
    orders = listallorders(g);