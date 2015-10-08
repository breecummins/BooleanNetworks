from subprocess import call
import patternmatch as pm

# Given a Morse graph number MGN for a database DATABASEFILE (.db), do the following database searches:
# 
# The following gives the list of parameters in the file PARAMFILE (.txt)
# sqlite3 /share/data/CHomP/Projects/DSGRN/DB/data/DATABASEFILE 'select ParameterIndex from Signatures where MorseGraphIndex=MGN' > ./PARAMFILE
#
# The following finds the Morse set number:
# sqlite3 /share/data/CHomP/Projects/DSGRN/DB/data/DATABASEFILE 'select * from MorseGraphAnnotations where MorseGraphIndex=MGN'
#
# So far the Morse set number is entered by hand, but I should write a parser eventually.

def patternSearch(morseset=0,specfile="networks/5D_Model_B.txt",paramfile="5D_Model_B_FCParams.txt",resultsfile='results_5D_B.txt',printtoscreen=0):
    R=open(resultsfile,'w',0)
    P=open(paramfile)
    for param in P.readlines():
        if printtoscreen:
            print '\nParameter: '+param
        # shell call to dsgrn to produce dsgrn_output.json, which is the input for the pattern matcher
        call(["dsgrn network {} analyze morseset {} {} >dsgrn_output.json".format(specfile,morseset,int(param))],shell=True)
        try:
            patterns,matches=pm.callPatternMatch(writetofile=0,returnmatches=1,printtoscreen=printtoscreen)
        except ValueError:
            print 'Problem parameter is {}'.format(param)
            raise
        for pat,match in zip(patterns,matches):
            R.write("Parameter: {}, Morseset: {}".format(param,morseset)+'\n')
            R.write("Pattern: {}".format(pat)+'\n')
            R.write("Results: {}".format(match)+'\n')
    R.close()
    P.close()

def patternSearchSingle(parameter,morseset=0,specfile="networks/5D_Model_B.txt",resultsfile='results.txt',printtoscreen=0):
    R=open(resultsfile,'w',0)
    # shell call to dsgrn to produce dsgrn_output.json, which is the input for the pattern matcher
    call(["dsgrn network {} analyze morseset {} {} >dsgrn_output.json".format(specfile,morseset,parameter)],shell=True)
    try:
        patterns,matches=pm.callPatternMatch(writetofile=0,returnmatches=1,printtoscreen=printtoscreen)
    except ValueError:
        print 'Problem parameter is {}'.format(parameter)
        raise
    for pat,match in zip(patterns,matches):
        R.write("Parameter: {}, Morseset: {}".format(param,morseset)+'\n')
        R.write("Pattern: {}".format(pat)+'\n')
        R.write("Results: {}".format(match)+'\n')
    R.close()

if __name__=='__main__':
    parameter=116014
    patternSearchSingle(parameter,specfile="networks/5D_Malaria_20hr.txt",resultsfile='results_malaria_param{}.txt'.format(parameter))

