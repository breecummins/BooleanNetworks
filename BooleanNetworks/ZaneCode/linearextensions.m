function linext = linearextensions(N,partialorder,order)

    function leastvals = least(partialorder)
        remaining = [];
        known = [];
        for c = partialorder
            remaining(end+1)=c{1}{1};
            m = c{1}{2};
            known(end+1:end+length(m)) = m;
        end
        leastvals = setdiff(remaining,intersect(remaining,unique(known)));
    end

    function orders = recurseorder(N,partialorder,order)
        if length(order) == N
            orders = order;
            return
        else
            orders={};
            for s = least(partialorder)
                for k = 1:length(partialorder)
                    if partialorder{k}{1} == s
                        break
                    end
                end
                orders{end+1} = recurseorder(N,[partialorder(1:k-1),partialorder(k+1:end)],[order,s]);
            end
        end
        orders = vertcat(orders{:});
    end

    % orders =  recurseorder(3,{ {1,[2]},{2,[]},{3,[]} }, [] );
    % orders = recurseorder( 4,{ {1,[2,3,4]}, {2,[4]}, {3,[4]}, {4,[]} }, [] );
    orders = recurseorder( 4,{ {1,[3,4]}, {2,[4]}, {3,[4]}, {4,[]} }, [] );
    disp(orders)

end