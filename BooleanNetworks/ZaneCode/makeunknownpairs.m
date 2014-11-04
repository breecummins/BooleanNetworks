function unknownpairs = makeunknownpairs(g)
	unknownpairs = [];
	N = length(g);
	for m = 2:N-2
		for n = m+1:N-1
			if g(m,n) ~= 1 && g(n,m) ~= 1
				unknownpairs(end+1,:) = [m,n];
			end
		end
	end
end
