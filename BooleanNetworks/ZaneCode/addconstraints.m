function g = calcpairswithconstraints(g,c1,c2,c3,c4)
	% c1 to c4 must be assigned a permutation of the integers 1 to 4

	% The following if statements encode specific 
    % information about the functional form of each node in the graph and their 
    % relationships. For different functions (i.e. the additive case or a different 
    % dimension), the if statements would have to be recoded.

	if c1 < c2
		g{7}{2}(end+1) = 12;
		g{5}{2}(end+1) = 10;
		g{3}{2}(end+1) = 9;
		g{8}{2}(end+1) = 14;
	elseif c2 < c1
		g{12}{2}(end+1) = 7;
		g{10}{2}(end+1) = 5;
		g{9}{2}(end+1) = 3;
		g{14}{2}(end+1) = 8;
	end

	if c3 < c4
		g{4}{2}(end+1) = 2;
		g{7}{2}(end+1) = 5;
		g{12}{2}(end+1) = 10;
		g{15}{2}(end+1) = 13;
	elseif c4 < c3
		g{2}{2}(end+1) = 4;
		g{5}{2}(end+1) = 7;
		g{10}{2}(end+1) = 12;
		g{13}{2}(end+1) = 15;
    end

end

