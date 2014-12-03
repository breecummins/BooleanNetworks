function g = transitiverelationships(g)
	% Adds transitive relationships to g using a breadthfirst search.

	% For every pair of nodes, search for a 
    % directed path between them. If it exists, add the pair to known pairs. 
    % If not, add the pair to unknown pairs.
	N = length(g);
	for k = 1:N
		for m = k+1:N
			ispath = breadthfirst(g,k,m);
			if ispath
				g{k}{2}(end+1)=m;
			else
				ispath = breadthfirst(g,m,k);
				if ispath
					g{m}{2}(end+1)=k;
				end
			end
		end
	end
	for k = 1:N
		g{k}{2} = unique(sort(g{k}{2}));
	end
end

			
