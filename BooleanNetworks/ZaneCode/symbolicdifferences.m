function g = symbolicdifferences(g,algexp)
	for m = 1:length(g)
		nm = g{m}{1};
		for k = m+1:length(g)
			nk = g{k}{1};
			if all(k ~= g{m}{2}) && all(m ~= g{k}{2})
				if isAlways(algexp{nm} < algexp{nk})
					g{m}{2}(end+1) = nk;
				elseif isAlways(algexp{nk} < algexp{nm})
					g{k}{2}(end+1) = nm;
				end
			end
		end
	end
