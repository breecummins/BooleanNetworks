import subprocess, os, time, sys

def makeDatabase(networkfile="/share/data/bcummins/DSGRN/networks/3D_Cycle",path2Signatures="/share/data/bcummins/DSGRN/software/Signatures/",script4database="database_script.sh"):
    try:
        os.chdir(path2Signatures)
    except OSError:
        raise OSError("Failed to change directory to Signatures.")
    if networkfile[-4:] == ".txt":
        networkfile = networkfile[:-4]
    subprocess.call(["qsub {} {}".format(script4database,networkfile)],shell=True)

def check4Database(dbname = "3D_Cycle.db", path2Signatures="/share/data/bcummins/DSGRN/software/Signatures/", path2database = "/share/data/CHoMP/Projects/DSGRN/DB/data/"):
    try:
        os.chdir(path2Signatures)
    except OSError:
        raise OSError("Failed to change directory to Signatures.")
    return os.path.isfile(dbname):

def copyDatabase(dbname = "3D_Cycle.db", path2Signatures="/share/data/bcummins/DSGRN/software/Signatures/", path2database = "/share/data/CHoMP/Projects/DSGRN/DB/data/"):
    count = 0
    while not check4Database and count < 1440: # limit wait to 2 hours
        time.sleep(5)
        count += 1
    if not check4Database:
        return False
    else:
        try:
            subprocess.call(["cp {} {}".format(dbname,path2database)])
            return True
        except OSError:
            return False

def queryForStableFCs(dbname = "3D_Cycle.db",path2database = "/share/data/CHoMP/Projects/DSGRN/DB/data/"):
    try:
        os.chdir(path2database)
    except OSError:
        raise OSError("Failed to change directory to CHoMP databases.")
    return subprocess.check_output(['''sqlite3 {} 'select count(*) from Signatures natural join (select distinct(MorseGraphIndex) from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges))' '''.format(dbname)],shell=True)

def getTotalNumberParams(networkfile="/share/data/bcummins/DSGRN/networks/3D_Cycle.txt"):
    if networkfile[-4:] != ".txt":
        networkfile = networkfile + ".txt"
    paramstr = subprocess.check_output(["dsgrn network {} parameter".format(networkfile)],shell=True)
    wordlist = paramstr.split()
    return int(wordlist[2])

def calculateFCratio(dbname,path2database,networkfile):
    numFCparams = queryForStableFCs(dbname,path2database)
    numparams = getTotalNumberParams(networkfile)
    return float(numFCparams) / numparams

def processNetworkFile(networkfile="/share/data/bcummins/DSGRN/networks/3D_Cycle",path2Signatures="/share/data/bcummins/DSGRN/software/Signatures/",script4database="database_script.sh", path2database = "/share/data/CHoMP/Projects/DSGRN/DB/data/"):
    if networkfile[-4:] == ".txt":
        networkfile = networkfile[:-4] 
    dbname = networkfile+".db"
    makeDatabase(networkfile,path2Signatures,script4database)
    success = copyDatabase(dbname, path2Signatures, path2database)
    if success:
        return calculateFCratio(dbname,path2database,networkfile+".txt")
    else:
        raise ValueError('Database not computed after two hours: {}'.format(dbname))

if __name__=="__main__":
    makeAllDatabases(sys.argv[1])