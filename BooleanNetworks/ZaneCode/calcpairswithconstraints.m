function [unknownpairs,knownpairs] = calcpairswithconstraints(unknownpairs,knownpairs,c1,c2,c3,c4)
	% c1 to c4 must be assigned a permutation of the integers 1 to 4

	% The following 4 internal functions retrieve known relationships between nodes.
	function inds = searchup(k)
		inds=[];
		for m = 1:length(knownpairs)
			p=knownpairs(m,:);
			if p(1) == k
				inds(end+1) = p(2);
			end
		end
	end

	function inds = searchdown(k)
		inds=[];
		for m = 1:length(knownpairs)
			p=knownpairs(m,:);
			if p(2) == k
				inds(end+1) = p(1);
			end
		end
	end

	function addpairsup(P)
		knownpairs(end+1,:) = P;
		inds = searchup(P(2));
		for k = inds
			p = [P(1),k];
			if ~ismember(p,knownpairs,'rows')
				knownpairs(end+1,:) = p;
			end
		end
	end
				
	function addpairsdown(P)
		knownpairs(end+1,:) = P;
		inds = searchdown(P(1));
		for k = inds
			p = [k,P(2)];
			if ~ismember(p,knownpairs,'rows')
				knownpairs(end+1,:) = p;
			end
		end
	end

	% Main body of the function: The following if statements encode specific information about the functional form of each node in the graph and their relationships. For different functions (i.e. the additive case or a different dimension), the if statements would have to be recoded.

	if c1 < c2
		addpairsup([7,12])
		addpairsup([5,10])
		addpairsup([3,9])
		addpairsdown([8,14])
	elseif c2 < c1
		addpairsup([9,3])
		addpairsup([10,5])
		addpairsup([12,7])
		addpairsdown([14,8])
	end

	if c3 < c4
		addpairsup([4,2])
		addpairsup([7,5])
		addpairsup([12,10])
		addpairsdown([15,13])
	elseif c4 < c3
		addpairsup([10,12])
		addpairsup([5,7])
		addpairsup([2,4])
		addpairsdown([13,15])
	end

	% Many previously unknown pairs are now known, so we remove them from the unknown pairs list.

	newunknownpairs = [];
	for m = 1:length(unknownpairs)
		u = unknownpairs(m,:);
		if ~ismember(u,knownpairs,'rows') && ~ismember(fliplr(u),knownpairs,'rows')
			newunknownpairs(end+1,:) = u;
		end
	end
	unknownpairs = newunknownpairs;
end

