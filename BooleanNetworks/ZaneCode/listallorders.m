function orders = listallorders(g)

	% recursive function
	function orders = recurseunknown(g,unknownpairs,orders)
		while ~isempty(unknownpairs)
			up = unknownpairs(1,:);
			for q = [up;fliplr(up)].'
				g(q(1),q(2)) = 1;
				g = transitiverelationships(g);
				unknownpairs = unknownpairs(2:end,:);
				orders = recurseunknown(g,unknownpairs,orders);
			end
		end
		orders{end+1} = g;
	end

	unknownpairs = makeunknownpairs(g);
	orders = {};
	orders = recurseunknown(g,unknownpairs,orders);
	disp(length(orders))
	save('orders.mat','orders')
end