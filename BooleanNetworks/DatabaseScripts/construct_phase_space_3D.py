#!/Users/arnaud/anaconda/bin/python
import numpy as np
import random

import sys

# seed the random generator with the argument at the command line
random.seed ( sys.argv[1] );

print "<atlas>"

# phase space bounds
lbps = np.array ( [ 0.0, 0.0, 0.0 ] )
ubps = np.array ( [ 10.0, 10.0, 10.0 ] )

dimension = lbps . shape[0]

print "  <dimension> ",dimension," </dimension>"

print "  <phasespace>"
print "    <bounds>"
print "      <lower> ", lbps[0], " ", lbps[1], " ", lbps[2], " </lower>"  
print "      <upper> ", ubps[0], " ", ubps[1], " ", ubps[2], " </upper>"  
print "    </bounds>"
print "  </phasespace>"

#gamma = np.array ( [ -1.0, -1.0, -1.0 ] );

print "  <gamma>"
print "    <lower> -1.5 -1.5 -1.5 </lower>"
print "    <upper> -0.5 -0.5 -0.5 </upper>"
print "  </gamma>"

# for the random sigma error bar
delta=0.1

# thresholds in each direction 
theta1 = np.array ( [ 0.25, 0.5, 0.75 ] )
theta2 = np.array ( [ 0.5 ] )
theta3 = np.array ( [ 0.5 ] )

# prepend / append phase space bounds
theta1=np.hstack((lbps[0],theta1))
theta1=np.hstack((theta1,ubps[0]))

theta2=np.hstack((lbps[1],theta2))
theta2=np.hstack((theta2,ubps[1]))

theta3=np.hstack((lbps[2],theta3))
theta3=np.hstack((theta3,ubps[2]))

# number of thresholds in each direction
# phase space bounds included 
n1 = theta1 . shape[0]
n2 = theta2 . shape[0]
n3 = theta3 . shape[0]

print "  <listboxes>"

for k in range(len(theta3)-1):
  for j in range(len(theta2)-1):
    for i in range(len(theta1)-1):

      # print in xml format
      print "    <box> <!-- box : ", k*(len(theta2)-1)*(len(theta1)-1)+j*(len(theta1)-1)+i, " -->"
      print "      <bounds>"
      print "        <lower> ", theta1[i], " ", theta2[j], " ", theta3[k], " </lower>"
      print "        <upper> ", theta1[i+1], " ", theta2[j+1], " ", theta3[k+1], " </upper>"
      print "      </bounds>"
      #---
      sigmax = random.uniform(lbps[0],ubps[0]);
      sigmay = random.uniform(lbps[1],ubps[1]);
      sigmaz = random.uniform(lbps[2],ubps[2]);

      print "      <sigma> "
      print "        <lower> ", sigmax-delta/2.0, " ", sigmay-delta/2.0," ", sigmaz-delta/2.0, " </lower>"
      print "        <upper> ", sigmax+delta/2.0, " ", sigmay+delta/2.0," ", sigmaz+delta/2.0, " </upper>"
      print "      </sigma>"
      
      #---
      print "    </box>"

print "  </listboxes>"
print "</atlas>"

