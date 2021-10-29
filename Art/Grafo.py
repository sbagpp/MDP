def createGraph(n):
    M = []
    for i in range(n):
        M.append([])
        for j in range(n):
            M[i].append(0)
    return M
 
 
def size(G):
    return len(G)
 
 
def insert(G, i, j, w):
    G[i][j] = w
 
 
def delete(G, i, j):
    G[i][j] = 0
 
 
def isEdge(G, i, j):
    return G[i][j] != []
 
 
def weight(G, i, j):
    return G[i][j]
 
 
def getAdjacents(G, i):
    V = []
    for j in range(len(G)):
        if G[i][j] != 0:
            V.append(j)
    return V
 
def getDegreeOf(G,i):
    V = getAdjacents(G,i)
    of = 0
    for j in V:
        of +=weight(G,i,j)
    return of