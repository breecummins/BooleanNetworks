function g = calcpairswithconstraints(g,c1,c2,c3,c4)
	% c1 to c4 must be assigned a permutation of the integers 1 to 4

	% The following if statements encode specific 
    % information about the functional form of each node in the graph and their 
    % relationships. For different functions (i.e. the additive case or a different 
    % dimension), the if statements would have to be recoded.

	% direct relationships
	if c1 < c2
		g(7,12)	= 1;
		g(5,10)	= 1;
		g(3,9)	= 1;
		g(8,14) = 1;
	elseif c2 < c1
		g(12,7) = 1;
		g(10,5) = 1;
		g(9,3) = 1;
		g(14,8) = 1;
	end

	if c3 < c4
		g(4,2) = 1;
		g(7,5) = 1;
		g(12,10) = 1;
		g(15,13) = 1;
	elseif c4 < c3
		g(2,4) = 1;
		g(5,7) = 1;
		g(10,12) = 1;
		g(13,15) = 1;
    end

    % transitive relationships
	g = transitiverelationships(g);
    
end

