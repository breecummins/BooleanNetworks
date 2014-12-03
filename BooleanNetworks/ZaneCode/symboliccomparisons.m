function g = symboliccomparisons(g,algexp,C,D)
	for m = 1:length(g)
		nm = g{m}{1};
		for k = m+1:length(g)
			nk = g{k}{1};
			if all(k ~= g{m}{2}) && all(m ~= g{k}{2})
				if missingrule(C{algexp{nm}(1)},D{algexp{nm}(2)},C{algexp{nk}(1)},D{algexp{nk}(2)},algexp,C,D)
					g{m}{2}(end+1) = nk;
				elseif missingrule(C{algexp{nk}(1)},D{algexp{nk}(2)},C{algexp{nm}(1)},D{algexp{nm}(2)},algexp,C,D)
					g{k}{2}(end+1) = nm;
				end
			end
		end
	end
