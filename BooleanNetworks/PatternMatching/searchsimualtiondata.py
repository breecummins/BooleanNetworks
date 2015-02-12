import os
from patternmatch import callPatternMatch

def simdata_5D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/5D_cycle_1/MGCC_14419/')  
    callPatternMatch(basedir,'5D Cycle 1, MGCC 14419')

def simdata_3D_Example():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Example/MGCC_5/')    
    callPatternMatch(basedir,'3D Example, MGCC 5')

def simdata_3D_Cycle1():
    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_30/')    
    callPatternMatch(basedir,'3D Cycle 1, MGCC 30')

    basedir=os.path.expanduser('~/ProjectData/DatabaseSimulations/3D_Cycle_1_Data/MGCC_45/')    
    callPatternMatch(basedir,'3D Cycle 1, MGCC 45')

if __name__=='__main__':
    simdata_3D_Example()
    simdata_3D_Cycle1()
    simdata_5D_Cycle1()
