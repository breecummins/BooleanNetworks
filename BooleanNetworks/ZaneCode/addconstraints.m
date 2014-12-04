function [g,unknownpairs] = addconstraints(diff12,diff34)
	% c1 to c4 must be assigned a permutation of the integers 1 to 4

	% The following if statements encode specific 
    % information about the functional form of each node in the graph and their 
    % relationships. For different functions (i.e. the additive case or a different 
    % dimension), the if statements would have to be recoded.
	g = {  {1,[2,3,4,9]}, {2,[5,6,10]}, {3,[5,7,11]}, {4,[6,7,12]}, {5,[8,13]}, {6,[8,14]}, {7,[8,15]}, {8,[16]}, {9,[10,11,12]}, {10,[13,14]}, {11,[13,15]}, {12,[14,15]}, {13,[16]}, {14,[16]}, {15,[16]}, {16,[]} };
	
	if diff12
		g{7}{2}(end+1) = 12;
		g{5}{2}(end+1) = 10;
		g{3}{2}(end+1) = 9;
		g{8}{2}(end+1) = 14;
	else
		g{12}{2}(end+1) = 7;
		g{10}{2}(end+1) = 5;
		g{9}{2}(end+1) = 3;
		g{14}{2}(end+1) = 8;
	end

	if diff34
		g{4}{2}(end+1) = 2;
		g{7}{2}(end+1) = 5;
		g{12}{2}(end+1) = 10;
		g{15}{2}(end+1) = 13;
	else
		g{2}{2}(end+1) = 4;
		g{5}{2}(end+1) = 7;
		g{10}{2}(end+1) = 12;
		g{13}{2}(end+1) = 15;
    end

    g = transitiverelationships(g);

    [knownpairs,unknownpairs] = makeunknownpairs(g);


end

