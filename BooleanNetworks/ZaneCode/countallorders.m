function orders = countallorders(g)

	% recursive function
	function orders = recurseunknown(g,unknownpairs,orders)
		while ~isempty(unknownpairs)
			up = unknownpairs(1,:);
			disp(length(unknownpairs));
			for q = [up;fliplr(up)].'
				g(q(1),q(2)) = 1;
				g = transitiverelationships(g);
				unknownpairs = unknownpairs(2:end,:);
				orders = recurseunknown(g,unknownpairs,orders);
			end
		end
		orders= orders+1;
	end

	unknownpairs = makeunknownpairs(g);
	orders = 0;
	orders = recurseunknown(g,unknownpairs,orders);
	disp(orders)
end