function g = transitiverelationships(g)
	% Adds transitive relationships to g using a breadthfirst search.

	% For every pair of nodes, search for a 
    % directed path between them. If it exists, add the pair to known pairs. 
    % If not, add the pair to unknown pairs.
	N = length(g);
	for k = 2:N-2
		for m = k+1:N-1
			ispath = breadthfirst(g,k,m);
			if ispath
				g(k,m)=1;
			else
				ispath = breadthfirst(g,m,k);
				if ispath
					g(m,k)=1;
				end
			end
		end
	end
end

			
