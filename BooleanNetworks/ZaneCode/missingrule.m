function is_ab_lt_cd = missingrule(a,b,c,d,algexp,C,D)
	% assuming all a,b,c,d > 0, variables symbolic
	
	function istrue = simplerule(a,b,c,d)
		istrue = false;
		if isAlways(a < c) && isAlways(b < d)
			istrue = true;
		end
	end

	is_ab_lt_cd = isAlways(a*b<c*d);

	if ~is_ab_lt_cd
		if simplerule(a,b,c,d)
			is_ab_lt_cd = true;
		else
			for k = 1:length(algexp) % would have to be a recursive function for dim higher than 4D
				m = C{algexp{k}(1)};
				n = D{algexp{k}(2)};
				if simplerule(a,b,m,n) && simplerule(m,n,c,d)	
					is_ab_lt_cd = true;
				end
			end
		end
	end

	if is_ab_lt_cd
		assumeAlso(a*b < c*d)
	end

end
