function kp = addpairs(k,ord,kp)
	pos = find(ord == k);
	for q = ord(1:pos-1)
		if ~ismember([q,k],kp,'rows')
			kp(end+1,:) = [q,k];
		end
	end
	for q = ord(pos+1:end)
		if ~ismember([k,q],kp,'rows')
			kp(end+1,:) = [k,q];
		end
	end
end


