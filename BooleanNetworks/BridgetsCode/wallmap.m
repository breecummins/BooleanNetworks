%Bridget
%07/31/2013
%Define the map between walls.

%First, I want to address one of the most important ideas behind this code.
%For a particular wall, there are two regular domains cooresponding to
%it.The flow from the two regular domains defines the different roles of
%this wall. For example, (1,0,1,0)-->(1,1,1,0). The wall y1=\lambda, is an
%incoming wall for (1,1,1,0), but a outgoing wall for (1,0,1,0). So there
%will be two different address in the matrix of the 3-D wall. The value in 
% the matrix stored under the two addresses will have a 1 for incoming wall
% and -1 for the outgoing wall.

%All walls in the code are stored as wall(wi,wj,wk)=1(comes in) or 
%-1(comes out). The input of the function should be a point of initial 
%condition and one value of its coordinate should equal to a threshold. 
%By the wall map list I provided earlier, it will tell us how many outlets
%there can be for the input wall.By the information provided, we can 
%compute what is the travel time for each case and return the image of the
%initial input on the hypeplane. Also for checking purpose, assign the 
%value of 1 or 0 to each ending point as good one or bad one based on 
%during the mapping, does any other thresholds changing happen.


function image=wallmap(ic_wall,wall,th,n,state,dr,fp)
%Identify if the input is a wall, instead of a regular domain
change=0;

%Identify the two regular domains cooresponding to the wall
for i=1:n
    if or(ic_wall(i)~=th(:,i),ic_wall(i)==0)
        %identify the state of the non-threshold coordinate in ic_wall
        ic_state1(i)=f_state(i,ic_wall(i),th);
        ic_state2(i)=ic_state1(i);
    else 
        change=i;    %identify the index of the coordinate of the wall
        ic_state1(i)=find(ic_wall(i)==unique(th(:,i)))-1;
        ic_state2(i)=ic_state1(i)-1;
    end
end
%Identify if the input is a wall, instead of a regular domain
if change==0
    disp('ERROR:Please input a wall instead of a regular domain:');
    disp(th);
else
    

%Find the first component of the index of the 3-D matrix to locate the wall
state1=find(ismember(state,ic_state1,'rows'));
state2=find(ismember(state,ic_state2,'rows'));
%There will be two addresses for the wall, we need to pick out the incoming
%wall, which has the value of 1.Store the state number as 'state_index' and
%the actually state as ic_wstate

if wall(state1,change,ic_state1(change)+1)==1
    ic_wstate=ic_state1;
    state_index=state1;
elseif wall(state1,change,ic_state2(change)+1)==1
    ic_wstate=ic_state1;
    state_index=state1;
    ic_wstate(change)=ic_state2(change);
elseif wall(state2,change,ic_state2(change)+1)==1
    ic_wstate=ic_state2;
    state_index=state2;
elseif wall(state2,change,ic_state1(change)+1)==1
    ic_wstate=ic_state2;
    state_index=state2;
    ic_wstate(change)=ic_state1(change);
else
    disp('@@@@@@@@@@@@@ERROR@@@@@@@@@@@@@@@@@@@@');
end
%disp(state_index);
%Now ic_wstate stores the wall address in the 3-D matrix. What we need to
%do is searching wall(ic_wstate(1),:,:)==-1, which is the possible outlet for
%the wall.

%for loop is based on the second index,which cooresponding to which
%variable is changing. Then in the for loop, it tells us which threshold it
%goes to.

outlet=0;
for i=1:n
    hyper=find(wall(state_index,i,:)==-1);
    %if hyper is not empty, the ith variable of state 'hyper' is the
    %hyperplane it maps to.¡¢
    if hyper
        outlet=outlet+1;
        %To compute the map, the information we need to plug into the equation is
        %the value of the focal point and the time.When we compute the focal point
        %of the wall, the way how we look forward is just using ic_wstate, because
        %that is the next step of the wall. Luckily in the begining of the code 
        %'special_state', I already computed the value of the focal point and I can
        %just pull information from there. ^_^
        for out=1:length(hyper)   
            %fp_hyper=fp(state_index,:);
            th_hyper=unique(th(:,i));
            e_t=((th_hyper(hyper(out))-fp(state_index,i))/(ic_wall(i)-fp(state_index,i)))^(1/dr(i));
            %Now we got the time, the next is plug in
            for si=1:n
                image(outlet,si)=fp(state_index,si)+(ic_wall(si)-fp(state_index,si))*e_t^(dr(si));
            end            
        end
%Here we want to check if the image is a good one or bad one. To check that
% we basically want to compare each value of the image on the hyperplane
% and see if it crossed any thresthold.
%First of all, we have to record the possible changes dimention-wise.
        dim_change(outlet)=i;
    end
end
%disp(dim_change);
if outlet==0
    image='Sink!No outlet';
else
%Check the state of the map on a hyperplane. 
%To check this code, at least one of the image is a good one
% disp('The possible dimention changes are:');
% disp(dim_change);
for size=1:outlet
        temp_check=1;
for check=1:length(dim_change)
    nn=dim_change(check);
        if f_state(nn,image(size,nn),th)~=ic_wstate(nn)
            temp_check=0;
            image(size,n+1)=temp_check;
%             disp('0000000000000');
%             disp(size);
%             disp(check);
%             disp('0000000000000');
        elseif image(size,nn)~=th(:,nn)
             image(size,n+1)=temp_check;
%             disp('111111111111111');
%             disp(size);
%             disp(check);
%             disp('111111111111111');
        else
%             disp('errors');
%             disp('eeeeeeeeeeeeeeee');
%             disp(size);
%             disp(check);
%             disp('eeeeeeeeeeeeeeee');
        end
end
end
end

disp('The image of the initial condition wall on the hyperplane is:');
disp(image);
end
end

%This is a function to find the state of the regular domain part.
function ic_s=f_state(i,ic,th)
 if ic==0
     ic_s=0;
 else

ic_s=0;
th_sorted=unique(th(:,i));
for step=1:length(th_sorted)
    if ic>th_sorted(step)
        ic_s=ic_s+1;
    end
end

%Adjust for the starting state 0
if min(th_sorted)==0
    ic_s=ic_s-1;
end
end
end







