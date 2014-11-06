function [knownpairs,unknownpairs] = makepairs(g)
	knownpairs = [];
	unknownpairs = [];
	N = length(g);
	for m = 2:N-2
		for n = m+1:N-1
			if g(m,n) == 1 
				knownpairs(end+1,:) = [m,n];
			elseif g(n,m) == 1 
				knownpairs(end+1,:) = [n,m];
			else
				unknownpairs(end+1,:) = [m,n];
			end
		end
	end
end
