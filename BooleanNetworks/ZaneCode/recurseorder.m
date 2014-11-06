function orders = recurseorder(ord,kp,N)
	if length(ord) == N 
		orders = ord;
	else
		orders = [];
		for k = 1:N
			if ismember(k,ord)
				continue
			else
				for pos = 0:length(ord)
					ord2 = [ord(1:pos),k,ord(pos+1:end)];
					if checkpartialorder(ord2,kp)
						kp1 = addpairs(k,ord2,kp);
						o = recurseorder(ord2,kp1,N)
						orders(end+1,:) = o
					end
				end
			end
		end
	end
end

