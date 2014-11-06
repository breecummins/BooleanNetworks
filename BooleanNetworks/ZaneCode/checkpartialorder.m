function isallowed = checkpartialorder(ord,kp)
	isallowed = true;
	for k = 1:length(ord)
		for m = k+1:length(ord)
			if ismember([ord(m),ord(k)],kp,'rows')
				isallowed = false;
				return
			end
		end
	end
end

