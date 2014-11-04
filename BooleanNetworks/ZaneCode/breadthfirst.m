function ispath = breadthfirst(g,first,last)

	import java.util.LinkedList % This seemed like the easiest implementation of a queue - could probably also use cell arrays, but I thought they were a pain.
	
	% Breadth-first search for a directed path between two nodes, first and last. g is described in main.m.
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

