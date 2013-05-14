#!/usr/bash python

import networkScripts as nS
import os

nS.randInits(os.path.expanduser('~/temp/dataset_randinits_x3_i4000/'),dt=0.001,xinit=3.0,numinits=4000)