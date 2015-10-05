#!/usr/bash python

import networkScripts as nS
import os

nS.alterParams(os.path.expanduser('~/temp/dataset_perdt/'),per=[0.0,-0.02,0.02,0.04],dt=0.0005)