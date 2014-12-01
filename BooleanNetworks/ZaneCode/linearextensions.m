function orders = linearextensions(partialorder,algexp)

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

    function orders = recurseorder(partialorder,order,N,algexp)
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
                % for m = 1:length(partialorder)
                %     if any(m == order)
                %         partialorder{m}{2}(end+1) = s;
                %     end
                % end
                % partialorder = symbolicdifferences(partialorder,algexp);
                orders{end+1} = recurseorder([partialorder(1:k-1),partialorder(k+1:end)],[order,s],N,algexp);
            end
        end
        orders = vertcat(orders{:});
    end

    orders = recurseorder(partialorder,[],length(partialorder),algexp);

    % orders =  recurseorder(3,{ {1,[2]},{2,[]},{3,[]} }, [] );
    % orders = recurseorder( 4,{ {1,[2,3,4]}, {2,[4]}, {3,[4]}, {4,[]} }, [] );
    % orders = recurseorder( 4,{ {1,[3,4]}, {2,[4]}, {3,[4]}, {4,[]} }, [] );
    % disp(orders)

end