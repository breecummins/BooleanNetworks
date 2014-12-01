function [g, algexp] = makedgraph(c12,c34)
	
	% Makes Zane's graph into a partial order. Records algebraic expressions at each node 
	% and records the first two constraints.

	g = {  {1,[2,3,4,9]}, {2,[5,6,10]}, {3,[5,7,11]}, {4,[6,7,12]}, {5,[8,13]}, {6,[8,14]}, {7,[8,15]}, {8,[16]}, {9,[10,11,12]}, {10,[13,14]}, {11,[13,15]}, {12,[14,15]}, {13,[16]}, {14,[16]}, {15,[16]}, {16,[]} };

	syms a1 b1 a2 b2 a3 b3 a4 b4;

	assume( (b1 > a1 > 0) & (b2 > a2 > 0) & (b3 > a3 > 0) & (b4 > a4 > 0) )

	c={a1+a2, b1+a2, a1+b2, b1+b2}; 
	d={a3+a4, b3+a4, a3+b4, b3+b4}; 

	algexp = { c{1}*d{1}, c{1}*d{3}, c{2}*d{1}, c{1}*d{2}, c{2}*d{3}, c{1}*d{4}, c{2}*d{2}, c{2}*d{4}, 
			   c{3}*d{1}, c{3}*d{3}, c{4}*d{1}, c{3}*d{2}, c{4}*d{3}, c{3}*d{4}, c{4}*d{2}, c{4}*d{4} };

    for 
   	for e = d


	if c12
		assumeAlso( c{1} < c{2} < c{3} < c{4} )
	else
		assumeAlso( c{1} < c{3} < c{2} < c{4} )
	end

	if c34
		assumeAlso( d{1} < d{2} < d{3} < d{4} )
	else
		assumeAlso( d{1} < d{3} < d{2} < d{4} )
    end


end

