function [unknownpairs,knownpairs] = calcpairsfrompartialorder(filename)
	% Returns the pairs with known and unknown orderings depending on the graph structure.

	import java.util.LinkedList % This seemed like the easiest implementation of a queue - could probably also use cell arrays, but I thought they were a pain.
	
	load(filename) % Returns g, a Boolean matrix (integers 0,1) representation of a digraph.

	% Internal function: Breadth-first search for a directed path between two nodes.
	function ispath = breadthfirst(first,last)
		ispath = false;
		queue = java.util.LinkedList();
		queue.add([first]);  
		while ~queue.isEmpty()
			temppath = queue.remove(); % The methods .add(), .remove(), and .isEmpty() are specific to the Java linked list and will not necessarily work with Matlab data structures
			if temppath(end) == last;
				ispath = true;
				break % If a path is found, stop searching and report that first < last.
			else
				for node = find(g(temppath(end),:)>0)
					if ~ismember(node,temppath)
						newpath=cat(1,temppath,node);
						queue.add(newpath);
					end
				end
			end
		end
	end

	% Main body of this function call. For every pair of nodes, search for a directed path between them. If it exists, add the pair to known pairs. If not, add the pair to unknown pairs.
	unknownpairs = [];
	knownpairs = [];
	N = length(g);
	for k = 2:N-2
		for m = k+1:N-1
			ispath = breadthfirst(k,m);
			if ispath
				knownpairs(end+1,:) = [k,m];
			else
				ispath = breadthfirst(m,k);
				if ispath
					knownpairs(end+1,:) = [m,k];
				else
					unknownpairs(end+1,:) = [k,m];
				end
			end
		end
	end
end

			
