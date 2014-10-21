function pairs = calcpairs()
	load('dgraph.mat') % returns g, a Boolean matrix (integers 0,1) representation of a digraph
	function ispath = breadfirst()
		ispath = false
	for i = 2:15
		for j = i+1:15
			
