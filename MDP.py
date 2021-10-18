from mip import *

name = "SOM-b_1_n100_m10.txt"#nome del file contente la base dati
f = open(name, "r")#apro in lettura il file
#cerco i vlaori di n e m nel file
line = f.readline()

whoAsI = line.split(" ")
m = int(whoAsI[1])
n = int(whoAsI[0])

distance = np.zeros(((n),(n))) #creo una matrice nxn con soli 0
distVect = [] #vettore contente le distanze, utile per la scrittura della F.O.
for x in f:
    x =  x.split(" ")#divido la stirnga x con una regex per far si che la riga si divisa in nodo i-esimo x[0], nodo j-esimo x[1] e in fine in x[2] vi sará la distanza ta i e j
    d =  x[2].split("\n") # essendo che il file é progettato su righe dopo ogni distanza di h aun ritorno a capo, quindi per eliminare ciò uso una regex che divide la stringa contenente la distanza dal ritonro a capo \n
    distVect.append(float(d[0])) #aggiungo al vettore
f.close #chiudo la pipeline del file
model = Model() #creo il modello PL
x = [ model.add_var(name  = "x"+str(i), var_type=BINARY) for i in range(n)] # aggiungo le varibili binarie che assumono il valore 1 se il nodo x[i] fa parte della suluzione, altrimenti x[i] =0
y = [] #vettore contente le variabili yi,j. tali varibile assume un valore appartente ai naturali positivi solo se il nodo x[i] e il nodo x[j] assumono entrambe il valore 1

for g in range(n):
   y +=([model.add_var(name  = "y"+str(g)+","+str(i), var_type = INTEGER) for i in range(g+1, n)]) #aggiungo le varibili yi,j al modello


#per come sono state create le varibili yi,j e per come sono state inserite le distanze di,j all'intenro del vettore distVect. 
#nella posizione distVect[0] vi é la distanza tra il nodo 0 e il nodo 1, e nella posizione y[0] vi é la varibile y0,1 ... e cosi via...
model.objective = maximize(xsum(y[i] * distVect[i] for i in range(len(distVect)))) 



for i in range(n):
    for j in range(i+1, n):
        if (i<j): #condizione necessaria affinche la matrice delle variabili sia triangolare superiore
            varXi = model.var_by_name("x"+str(i)) #prenodo la variabile xi
            varXj = model.var_by_name("x"+str(j)) #prendo la variabile xj
            varYij = model.var_by_name("y"+str(i)+","+str(j)) #prendo la variabile yij
            model += varYij <= 1
            model += varXi + varXj - varYij <=1 #vincolo che mi permette di dire che se xi = xj = 1, allora yj = 1
            model += varYij - varXj <= 0 
            model += varYij - varXi <= 0
            model += varYij >= 0


model += xsum( x[i] for i in range(n)) == m #chiedo che nella soluzione vi siano m nodi

##print (model.objective)
            

sec = 0 #definire il tempo d'esecuzione 
model.optimize(max_seconds = sec) # inzia la soluzione 

premessa = "Le varibili in base nella soluzione sono:\n"

for xi in model.vars:
    if xi.x != 0:
        premessa += str(xi)+"= "+str(xi.x)+"\n"



premessa += "La funzione obbiettivo vale : "+str(model.objective.x)+"\n"

print(premessa)