function [partialorder, algexp, C, D] = makedgraph(partialorder,diff12,diff34)
	
	% Makes Zane's graph into a partial order. Records algebraic expressions at each node 
	% and records the first two constraints.

	syms aa12 ba12 ab12 bb12 aa34 ba34 ab34 bb34;

	% assume( (b1 > a1 > 0) & (b2 > a2 > 0) & (b3 > a3 > 0) & (b4 > a4 > 0) )

	% c={a1+a2, b1+a2, a1+b2, b1+b2}; 
	% d={a3+a4, b3+a4, a3+b4, b3+b4}; 

	C={aa12, ba12, ab12, bb12}; 
	D={aa34, ba34, ab34, bb34}; 

	algexp = { [1,1]; [1,3]; [2,1]; [1,2]; [2,3]; [1,4]; [2,2]; [2,4]; 
			   [3,1]; [3,3]; [4,1]; [3,2]; [4,3]; [3,4]; [4,2]; [4,4] };

	if diff12
		assumeAlso( 0 < C{1} < C{2} < C{3} < C{4} )
	else
		assumeAlso( 0 < C{1} < C{3} < C{2} < C{4} )
	end

	if diff34
		assumeAlso( D{1} < D{2} < D{3} < D{4} )
	else
		assumeAlso( D{1} < D{3} < D{2} < D{4} )
    end

	partialorder = symboliccomparisons(partialorder,algexp,C,D);
end

