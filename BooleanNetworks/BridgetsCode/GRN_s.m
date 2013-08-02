%07/16/2013
%Bridget

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This is a single step code, for test purpose with an example.%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Initial input for the network    %%
%Set the number of the variables  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;
clc;

%input for the model set-up: 
%for each element in the matrix, 
%m_ij= 1 means j is activating i
%m_ij=-1 means j is depressing i
%m_ij= 0 means no effect

%    m=zeros(n);
%    for nn = 1:n
%    m(nn,:) = input(['Enter number ' num2str(nn) '\n']);
%    end

% Initial setting:the threshold matrix and the parameter matrix
n=4;
th=zeros(n);
pm=[0.192028349427775,0.525404403859336,0.393456361215266,0.347712671277525;0.138874202829155,0.530344218392863,0.671431139674026,0.149997253831683;0.696266337082995,0.861139811393332,0.741257943454207,0.586092067231462;0.0938200267748656,0.484853333552102,0.520052467390387,0.262145317727807;];

%example:

%model set-up
mu=[1,0,1,0;1,0,0,0;0,1,0,0;1,0,1,0];
md=[0,0,0,1;0,0,0,0;0,0,0,0;0,0,0,0];
m=mu-md;
pm=pm.*(mu+md);
%threshold set-up
th(:,1)=[0.999,1.89,0,2.11];
th(:,2)=[0,0,1.58,0];
th(:,3)=[1.68,0,0,1.58];
th(:,4)=[1.49,0,0,0];

%decay rate set-up
dr=[1,2,3,4]*0.1;

disp('The threshold matrix is:');
disp(th);

%Initial condition:
ic=input('Enter Initial Condition:\n');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Second, locate the initial condition: %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

l=repmat(ic,n,1)-th>0;
%disp('The location of the I.C. is:');
%disp(l);
%Fix the down-regulate effect:
L=mod(l+md,2);
%disp('The location matrix for the I.C. is:');
%disp(L);

%disp('The paramter matrix is:');
%disp(pm);

%Identify the corresponding focal points:
fp=sum(pm.*L,2);
disp('The focal points are:');
disp(fp);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Third step, find the closest threshold: %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% For this step there are three speical situation need to consider
temp1=zeros(n);
temp2(n)=0;
next_th(n)=0;
for nj=1:n
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
disp('The thresholds will be hit by the next step are:');
disp(next_th);
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%The next step is compute the time %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if max(next_th)==0
    disp('Sink!Iteration ends');
else
 t(n)=0;
 et=0;
 for nj=1:n
     if next_th(nj)~=0 %Only compute the time switching domain
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
end

   

