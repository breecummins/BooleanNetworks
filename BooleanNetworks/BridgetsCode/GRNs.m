%07/17/2013
%Bridget

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This is a single step function, for test purpose with an example.%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [ic,steps,map]=GRNs(ic,n,th,pm,dr,steps,md)
%The states of the initial condition   
   state_ic=state(ic,th);
   disp('The state of the initial condition is ');
   map(steps,:)=state_ic;
   X = sprintf('~~~~~~~~~~~~~~~~~~Iteration %d ~~~~~~~~~~~~~~~~~~~',steps);
   disp(X);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%First, locate the initial condition: %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

l=repmat(ic,n,1)-th>0;
%Fix the down-regulate effect:
L=mod(l+md,2);

%disp('The paramter matrix is:');
%disp(pm);

%Identify the corresponding focal points:
fp=(sum(pm.*L,2))'./dr;        
%##############Notice: the focal point is fp/dr############################
disp('The focal points are:');
disp(fp);
disp('The states of the focal point are ');
state_fp=state(fp,th);
if state_fp==state_ic
    disp('&&&&&&&&&&&&&&&&&&&&&&&Sink!Iteration ends&&&&&&&&&&&&&&&&&&&&')
    steps=0;  %%% End the iteration
else
    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Second step, find the closest threshold: %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% For this step there are three speical situation need to consider
temp1=zeros(n);
temp2(n)=0;
next_th(n)=0;
    for nj=1:n
       if state_ic(nj)~=state_fp(nj)
         for ni=1:n
           if th(ni,nj)~=0 %Frist, the threshold is not 0,means regulation happens
          
             if ((fp(nj)-th(ni,nj))*(ic(nj)-th(ni,nj)))<0  %find the inbetween
                temp1(ni,nj)=th(ni,nj);
             end
          end
            temp2(ni)=abs(temp1(ni,nj)-ic(nj));  %closest threshold
         end
   
         if temp1(:,nj)==zeros([n,1])
           next_th(nj)=0; %Second,the variable won't hit any threshold
                      %including decreasing to zero directly
         elseif min(temp2)~=0
            mm=find(temp2==min(temp2));
            next_th(nj)=temp1(mm,nj);
         end
     
   %elseif f(nj)==0
        %next_th(nj)=max(th(:,nj));
    %end
       end
    end
disp('The thresholds will be hit by the next step are:');
disp(next_th);
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%The next step is compute the time %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
%%%%%  if max(next_th)==0
%%%%%   disp('###################Sink!Iteration ends########################')
%%%%%   step=0;  %%% End the iteration
%%%%%   else

t(1:n)=0;
for nj=1:n
    if  and(state_ic(nj)~=state_fp(nj),next_th(nj)~=ic(nj))
     t(nj)=((next_th(nj)-fp(nj)/dr(nj))/(ic(nj)-fp(nj)/dr(nj)))^(1/dr(nj));
               % not exatcly t, but the exp(-t) 
     end
nn=find(t==max(t)); %design to find the maximum to aviod the zeros 
et=t(nn);
end
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Compute the initial condition for the next step%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for nj=1:n
      ic(nj)=fp(nj)/dr(nj)+(ic(nj)-fp(nj)/dr(nj))*et^(dr(nj));
end

disp('The initial condition for next step is:');
disp(ic);
steps=steps+1;
end
end


function states=state(ic,th)
n=length(ic);
states(1:n)=0;
for nj=1:n
        for ni=1:n
            if and(th(ni,nj)~=0,ic(nj)>th(ni,nj))
                states(nj)=states(nj)+1;
            end
        end
end
  disp(states);
end

