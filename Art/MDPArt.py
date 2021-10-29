from Grafo import * 
from timeit import default_timer as timer
import operator

def risolutore(name):
    
    #nome del file contente la base dati
    f = open(name, "r")#apro in lettura il file
    #cerco i vlaori di n e m nel file
    line = f.readline()
    n = 0
    m = 0
    whoAsI = line.split(" ")
    m = int(whoAsI[1])
    n = int(whoAsI[0])
    grafo = createGraph(n) #creo il grafo
    for x in f:
        x =  x.split(" ")#divido la stirnga x con una regex per far si che la riga si divisa in nodo i-esimo x[0], nodo j-esimo x[1] e in fine in x[2] vi sará la distanza ta i e j
        i = int(x[0])
        j = int(x[1])
        d =  x[2].split("\n") # essendo che il file é progettato su righe dopo ogni distanza di h aun ritorno a capo, quindi per eliminare ciò uso una regex che divide la stringa contenente la distanza dal ritonro a capo \n
        #per semplicitá al posto di creare un grafo non orientato creo un grafo orientato che presta dij = dji 
        insert(grafo, i , j, float(d[0]))
        insert(grafo, j, i, float(d[0]))
    f.close #chiudo la pipeline del file

    time = {25 : 3, 50 : 5, 100 : 10, 125 : 13 , 150 : 30} #dizionario dei tempi

    minut = time[n]*60 #minuti massimo in cui il programma é in esecuzione

    start = timer()
    nIter = 0
    xbase = None
    setSolution = {}
    foMax = 0
    xBest = None
    finsh  = True
    no =0 
    while(timer()-start <minut and finsh):
        no += 1
        if (xbase == None):
            xbase = init(grafo, m, n)#iniz. del problema
        else:
            xbase = getBase(grafo, m, n, setSolution, xbase.copy())
        if(xbase == None):#se xbase == None anche dopo il processamento di  init or getBase vuol direche ho fino le soluzioni
            finsh = False #fine soluzioni prima del tempo
        else:
            fo = getValueFo(xbase, grafo)
            setSolution[tuple(xbase.copy())] = fo
            if(xBest == None or fo > foMax):
                xBest = xbase.copy()
                foMax = fo
            print(fo)
            #print(start-timer())
            print(xbase)
            
    premessa = name+";"+str(n)+";"+str(m)+";"+str(foMax)+";\n"
    return premessa

def init(grafo, m , n):

    setDensity = {} #correlazione biunivoca tra la densitá di una var e lavariabile
    vectDensity = [] #usato per ordinamento
    density = 0

    for var in range(n):
        density = getDensityByVar(grafo,var)
        setDensity[var] = density
        vectDensity.append(density)

    vectDensity = sorted(vectDensity)
    xbase = []
    iterator = len(vectDensity)-1#parto dal lultimo perche e il piu grande
    var = 0
    while(len(xbase) != m):
        if(setDensity[var] == vectDensity[iterator] and len(xbase)<=m ):
            xbase.append(var)
            iterator -= 1
            var = 0
        else:
            var += 1

    return sorted(xbase)


def getDensityByVar(grafo, var):
    density = 0
    neighbors = getAdjacents(grafo, var)
   #print(neighbors)
    for i in neighbors:
        density += weight(grafo, var, i)

    return density/len(neighbors)

def getValueFo(x,grafo):
    fo = 0
    #print(x)
    for i in x:
        for j in x:
            i = int(i)
            j = int(j)        
            if (i>j): #se il
                fo += weight(grafo, i, j)

    return fo
#se torno come base none vuol dire che ho finito tutte le soluzioni da provare
def getBase(grafo, m, n, setSolution, xbase):
    posExit = 0
    x = xbase.copy()
    setExit = getSetExit(grafo, m, n, x.copy())
    while posExit<len(setExit):
        exit = setExit[posExit][0]
        x.remove(exit)
        enter = getEnter(grafo, m, n, x.copy(), setSolution)
        if(enter != None):
            x.append(enter)
            x = sorted(x)
            return x.copy()
        else:
            x.append(exit)
            x = sorted(x)
            posExit +=1
    y = 0
    return None


def getSetExit(grafo, m, n, xbase):
    x = xbase.copy()
    setFo = {}
    xiter = x.copy()
    for var in xiter:
        x.remove(var)
        setFo[var] = - getValueFo(x, grafo) #metto il segno meno per una questione di comoditá per lordinamento
        x.append(var)
    order = sorted(setFo.items(), key=operator.itemgetter(1))
    return order

def getEnter(grafo, m, n, xbase, setSolution):
    x = xbase.copy()
    setDensity = {}
    for var in range(n):
        if(var not in x):
            x.append(var)
            x = sorted(x)
            if(tuple(x) not in setSolution.keys()):
                setDensity[var] = - getDensityByVar(grafo,var)#metto il segno meno per una questione di comoditá per lordinamento
                x.remove(var)
            else:
                x.remove(var)
    if(len(setDensity)==0):
        return None
    else:
        order = sorted(setDensity.items(), key=operator.itemgetter(1))
        return order[0][0]
    

