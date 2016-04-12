import subprocess, os, glob

def queryForStableFCs(dbname):
    return subprocess.check_output(['''sqlite3 {} 'select count(*) from Signatures natural join (select distinct(MorseGraphIndex) from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges))' '''.format(dbname)],shell=True)

def getTotalNumberParams(networkfile="/share/data/bcummins/DSGRN/networks/3D_Cycle.txt"):
    if networkfile[-4:] != ".txt":
        networkfile = networkfile + ".txt"
    paramstr = subprocess.check_output(["dsgrn network {} parameter".format(networkfile)],shell=True)
    wordlist = paramstr.split()
    return int(wordlist[2])

def calculateFCratio(dbname,networkfile):
    numFCparams = queryForStableFCs(dbname)
    numparams = getTotalNumberParams(networkfile)
    return float(numFCparams) / numparams

def main():
    path2database = '/share/data/bcummins/DSGRN/software/Signatures'
    try:
        os.chdir(path2database)
    except OSError:
        raise OSError("Failed to change directory to CHoMP databases.")
    names = []
    ratios = []
    for dbname in glob.glob('databases/*.db'):
        name = dbname[9:-3]
        rat = calculateFCratio(dbname,'networks/'+ dbname +'.txt')
        names.append(name)
        ratios.append(rat)
    # TODO: sort list and write to file




if __name__=="__main__":
    pass
    #write to take each file from DIR and calculate ratio; then sort according to ratio; save filename and percent in .txt file