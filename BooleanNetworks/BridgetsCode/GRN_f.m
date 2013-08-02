%07/17/2013
%Bridget

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Complete codes for the GRN model with an example.%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Initial input for the network    %%
%Set the number of the variables  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;
clc;

%h=input('How are you doing today?\n','s');
%disp('^_^');
%n=input('Set the number of the genes of this model:');

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
%threshold set-up
th(:,1)=[0.999,1.89,0,2.11];
th(:,2)=[0,0,1.58,0];
th(:,3)=[1.68,0,0,1.58];
th(:,4)=[1.49,0,0,0];

%decay rate set-up
dr=[1,2,3,4];

disp('The threshold matrix is:');
disp(th);

%Initial condition:
ici=input('Enter Initial Condition:\n');
ic=ici;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Second, locate the initial condition: %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
steps=1; %The count of steps
[ic,steps,map]=GRNs(ic,n,th,pm,dr,steps,md);
while steps>=1
  [ic,steps,map]=GRNs(ic,n,th,pm,dr,steps,md);
end
disp('The state map we get is the following: ');
disp(map);




