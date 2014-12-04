function [knownpairs,unknownpairs] = makeunknownpairs(g)
	knownpairs = [];
	unknownpairs = [];
	N = length(g);
	for m = 1:N
		for n = m+1:N
			if any(n == g{m}{2})
				knownpairs(end+1,:) = [m,n];
			elseif any(m == g{n}{2})
				knownpairs(end+1,:) = [n,m];
			else
				unknownpairs(end+1,:) = [m,n];
			end
		end
	end
end
