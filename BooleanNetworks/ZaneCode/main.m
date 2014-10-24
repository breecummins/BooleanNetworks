function main()
	% The ultimate goal of this function is to find all possible linear orders for the 4D multiplicative case. It is not complete as of 10/24/14.

	% The following function call creates a 0-1 matrix representing the partial order lattice for the 4D multiplicative case using the node numbering given by Zane. The lattice with node numbering and equations is in 4DimLatticeWithMult.png. The matrix, named g, is saved in a function dgraph.mat. If an (i,j) element in the matrix has 1, this means that the equation in node i is less than the equation in node j. That is, there is an edge in the lattice from i to j.
	makedgraph();

	% The following function call calculates the pairs of nodes whose ordering is either known or unknown, using only information from the partial order lattice. This includes not only the direct edges recorded in the matrix, but transitive relationships as well, using a breadth-first path search on the graph. Note that the variables known and unknown are mx2 and nx2 matrices, where each row is a pair. In the known matrix, the first element is less than the second element by convention. Example: [ 8, 4 ] in known means that the equation at node 8 is less than the equation at node 4. In the unknown matrix, either relationship may be true.
	[unknownpairs,knownpairs] = calcpairsfrompartialorder('dgraph.mat');

	% The following function call takes a specific ordering of differences (lowest edges in the lattice) and calculates which previously unknown pairs are now known, and returns the updated matrices. 
	c1=1; c2=2; c3=3; c4=4;
	[unknownpairs,knownpairs] = calcpairswithconstraints(unknownpairs,knownpairs,c1,c2,c3,c4);

	% Now we need an algorithm for determining all consistent sets of orderings of the unknown pairs.