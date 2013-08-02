%%Bridget 07/24

clear;
%Initial setting of the system, threshold, parameter and decay rate matrix
n=4;
th=zeros(n);
th(:,1)=[0.25,0.5,0,0.75];
th(:,2)=[0,0,0.5,0];
th(:,3)=[0.5,0,0,0.5];
th(:,4)=[0.5,0,0,0];
pm=[0.5,0,1,1;1,0,0,0;0,1,0,0;1,0,1,0];
dr=[1,0.5,0.5,0.5];

%The network between different nodes
mu=[1,0,1,0;1,0,0,0;0,1,0,0;1,0,1,0];
md=[0,0,0,1;0,0,0,0;0,0,0,0;0,0,0,0];

%Decide the highest state for each variable:
state_count(n)=ones;
for j=1:n
     state_count(j)=length(unique(th(:,j)));
     if min(unique(th(:,j)))==0
         state_count(j)=state_count(j)-1;
     end
     
end


%Store all the possible states in a matrix
sets = {0:state_count(1),0:state_count(2),0:state_count(3),0:state_count(4)};
[x y1 y2 z] = ndgrid(sets{:});
state = [x(:) y1(:) y2(:) z(:)];
sizes=size(state,1);


state_th=zeros(n);
state_fp=zeros(sizes,n);

%find the steady state one by one
for ni=1:sizes
state_fp(ni,:)=zeros;
l=zeros(n);
%Represent the threthold into a state matrix and locate the each state 
        for j=1:n
            for i=1:n
                state_th(i,j)=length(find(unique(th(:,j))<th(i,j)));
                if th(i,j)==0
                    l(i,j)=0;
                elseif state(ni,j)>=state_th(i,j)
                    l(i,j)=1;
                end
            end
        end
%Based on the location of the given state,compute the focal points
    L=mod(l+md,2);   
    fp(ni,:)=(sum(pm.*L,2))'./dr;
%The states of the corresponding focal points   
for nnj=1:n
        for nni=1:length(unique(th(:,nnj)))
            if fp(ni,nnj)>unique(th(nni,nnj))
                state_fp(ni,nnj)=state_fp(ni,nnj)+1;
            end
        end
        if and(state_fp(ni,nnj)~=0,min(unique(th(:,nnj)))==0)
                state_fp(ni,nnj)=state_fp(ni,nnj)-1;
        end
end

%Compare the state of the focal points and the state of initial condition
if state(ni,:)==state_fp(ni,:)
    %disp('The steady states in this network are the following:');
    %disp(state(ni,:));
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This is wrong, in mutil-throshlod, a source can't be in the middle state%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%if state(ni,:)~=state_fp(ni,:)                                          %
%    %disp('The source states in this network are the following:');       %
%    %disp(state(ni,:));                                                  %
%end                                                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end



%Bridget
%07/29/2013
%Now basded on the code of finding the steady states, all the focal point
%infomation is stored in two matrices, state and state_fp. By comparing the
%states of two neighbor states, we can find out the black walls and white
%walls.
%In this case we are dealing with n=4, there are (4^1)*(2^3)=32 possible
%states. I will creat a 32 by 32 matrix, named dynamic, to store the flow 
%direction bewteen each node.

%e.g. dynamic(i,j)=1 means state i flows to state j
%     dynamic(i,j)=0 means state i won't flow to state j
%         if dynamic(i,j)+dynamic(j,i) =0, white wall
%         if dynamic(i,j)+dynamic(j,i) =2, black wall
 
%First of all, find out how many neignbor one state has.
nb(sizes)=0;
for i=1:sizes
    for j=1:n
        if state(i,j)>0
            nb(i)=nb(i)+1;
        end
        if state(i,j)<state_count(j)
            nb(i)=nb(i)+1;
        end
    end
   
end

next=state;
dynamic=zeros(sizes);

for i=1:sizes
    for j=1:n
        if state_fp(i,j)>state(i,j)
            next(i,j)=state(i,j)+1;
            k=find(ismember(state,next(i,:),'rows'));
            dynamic(i,k)=1;
        elseif state_fp(i,j)<state(i,j);
            next(i,j)=state(i,j)-1;
            k=find(ismember(state,next(i,:),'rows'));
            dynamic(i,k)=1;
        end
        next(i,:)=state(i,:); %Guarantee one change every time
    end
    
end


for i=1:sizes
    for j=1:sizes
        if dynamic(i,j)+dynamic(j,i)==0
            change=find(state(i,:)~=state(j,:));
            if length(change)==1
                if abs(state(i,change)-state(j,change))==1
                    %disp('White wall exists between:');
                    %disp(state(i,:));
                    %disp(state(j,:));
                end
            end
        end
        if dynamic(i,j)+dynamic(j,i)==2
            %disp('Black wall exists between:');
            %%disp(state(i,:));
            %disp(state(j,:));
        end
    end
    
%%% double check the sink/source anwser:
   if dynamic(i,:)==0
        %disp('~~~~~~~~~~~~~~The following state is sink:~~~~~~~~~~~~~~~');
        %disp(state(i,:));    
    elseif sum(dynamic(i,:))==nb(i)
        %disp('~~~~~~~~~~~~~~The following state is source~~~~~~~~~~~~~~');
        %disp(state(i,:)); 
    end
end



%Bridget
%07/30/2013
%Code for the Map in between each wall
%Using a 3-D matrix to store each wall, such as for state NO. 31, which is 
% state [2,1,1,1], 5 walls are around. [2,x,1,1] has an index of (31,2,1)
% which means the 31st state, second variable and first threshold.
% Using 1 as coming in and -1 as coming out

wall=zeros(sizes,n,max(nb));            % wall(wi,wj,wk)

%Check all the coming out walls for each state
for i=1:sizes
    for j=1:sizes
        if dynamic(i,j)==1
            wj=find(state(i,:)~=state(j,:));
            %wk-1 is the state it goes to, avoid wk=0
            wk=state(j,wj)+1;
            %Flow from i to j, means the wall is "out" for state i
            %                                and "in"  for state j
            wall(i,wj,wk)=-1;
            wall(j,wj,wk)=1;
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This is code for the translate work. Hide the code to protect screen.%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% test=0;
% %%% Centered on each state
% for i=1:sizes
%     %disp('~~~~~~~~~~~~~~~~~~~~~~~~STATE~~~~~~~~~~~~~~~~~~~~~~~~~');
%     %disp(state(i,:));
%     for k=1:max(nb)
%         for j=1:n
%             if wall(i,j,k)==1
%                 %disp('Starting from:');
%                 translate(i,j,k,state,n);
%                 if wall(i,:,:)~=-1
%                     %disp('NO OUTLET');
%                 else
%                     %disp('Next step:');
%                     for tj=1:n
%                         for tk=1:max(nb)
%                             if wall(i,tj,tk)==-1
%                                 translate(i,tj,tk,state,n);
%                             end
%                         end
%                     end
%                 end
%             end
%         end
%     end
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%08/01/2013
%Based on all the information from above. Call the function of wallmap.

ic_w=input('Enter the Initial Condition of the Wall:\n');
ic_wall=ic_w;


image=wallmap(ic_wall,wall,th,n,state,dr,fp);






