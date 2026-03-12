#NAHMAN MARTINA L:13685
#Graph = Array(n,LinkedList())
from collections import deque
#EJERCICIO 1
#lista de vertices y lista de aristas
#recorrer toda la lista de vertices y en ese recorrido que devuelva
#  una lista con todas nodos que tienen como primer componente el vertice con el que estamos 
def createGraph(LA,LV):
    l_ady=[]
    for vertices in LV:
        lis=[]
        lis.append(vertices)
        l_ady.append(lis)
    for vertice in l_ady:
    #recorremos los vertices
        for aristas in LA:
            vertice[0]
            if vertice[0]==aristas[0]:
                vertice.append(aristas[1])
    return(l_ady)

#EJERCICIO 2
#operación existe camino que busca si existe un camino entre los vértices v1 y v2
def existPath(Grafo, v1, v2): 
    list= DFS_raro(Grafo)
    if (v1 in list) and ( v2 in list):
        return True
    else:
        return False

#RECORRIDO DFS? (PROFUNDIDAD)
def DFS_raro(grafo):
    vertice = None
    visitados = []
    dfsRaro(grafo,visitados,vertice)
    return visitados

def dfsRaro(grafo, visitados,vertice):
    for i in range (len(grafo)):
        #chequeamos que los vertices tengan vertices adyacentes
        if len(grafo[i]) != 1:
            for j in range (len(grafo[i])):
                if grafo[i][j] not in visitados:
                    vertice=grafo[i][j]
                    visitados.append(vertice)
                    dfsRaro(grafo, visitados, vertice)
    # Retornar la lista de vértices visitados
    return visitados

#EJERCICIO 3
#Implementa la operación es conexo
def isConnected(Grafo):
    listA= DFS_raro(Grafo)
    if len(listA) == len(Grafo):
        return True
    else:
        return False
    
#EJERCICIO 4
#Implementa la operacion es arbol
#arbol: aciclico / conexo / n-1 aristas
def isTree(Grafo,LA):
    conexo = isConnected(Grafo)
    #chequeo aristas = n-1
    
    if (len(Grafo)-1) == (len(LA)/2):
        checkedge = True

    if (conexo and checkedge) == True:
        return True
    else: return False

#EJERCICIO 5
#Implementa operacion arbol completo
#Arbol completo: existe una arista entre todo par de vértices.
def isComplete(Grafo):
    #verificar si cumple con: n (n-1)/2 aristas
    vertices= Grafo[0]
    for i in range (len(vertices)):
        for j in range(i+1,len(vertices)):
            if vertices[j] not in Grafo[vertices[i]]:
                return False
    # Si se recorren todas las combinaciones posibles de vértices
    # y no se encuentra ninguna que no esté conectada por una arista, se devuelve True
    return True

#EJERCICIO 6 VEEEEEEEEER!!!!!!!
#Implementar una función que dado un grafo 
#devuelva una lista de aristas que si se eliminan el grafo se convierte en un árbol
def convertTree(Grafo):
    aristasArbol = []
    for vertice in Grafo:
        for aristas in Grafo[vertice]:
            Grafo[vertice].pop(vertice)
            Grafo[aristas].pop(aristas)
            
            #verificamos si el grafo es conexo:
            if isConnected(Grafo) == True:
                tupla=(vertice,aristas)
                aristasArbol.append(tupla)
            #restauramos la arista eliminada    
            Grafo[vertice].append(vertice)
            Grafo[aristas].append(aristas)
    return aristasArbol

#RECORRIDO BFS!!!!!
def BFS (graph,V):
    #coloco en la queue el vertice
    queue=[]
    queue.append(V)
    #lista de pendientes
    grayList=[]
    grayList.append(V)
    #lista de recorridos
    blackList=[]

    while len(queue)>0:
        posc=Search_vertice(queue[0],graph)
        aux=queue.pop(0)
        L=graph[posc]
        #si no estan sus elementos en la lista de pendientes los agrega 
        for current in L:
            if search_list(grayList,current)==None:
                grayList.append(current)
                queue.append(current)
        blackList.append(aux)
    
    return blackList
def Search_vertice(V,G):
    #busca un vertice y devuelve el indice
    for i in range(0,len(G)):
        if G[i][0]==V:
            return i
        
def search_list(l,value):
    #devuelve el value o None en caso contario
    for i in range(0,len(l)):
        if value==l[i]:
            return value
    return None
        
#RECORDIDO DFS!!!!!
def DFS(graph):
    grayList=[]
    blackList=[]
    whitelist=[]
    #coloco todos en blanco
    for each in graph:
        whitelist.append(each[0])
    for each in graph:
        vertex=each[0]
        #busco los nodos que son blancos
        if search_list(whitelist,vertex)!=None:
            Dfs_Visit(graph,vertex,grayList,whitelist,blackList)
    blackList.reverse()
    return blackList

def Dfs_Visit(G,V,grayList,whitelist,blackList):
    #saco de los blancos y los pongo en gris
    whitelist.remove(V)
    grayList.append(V)
    posc=search_list(V,G)
    #busco en cada sublista blancos
    for each in G[posc]:
        if search_list(whitelist,each)!=None:
            Dfs_Visit(G,each,grayList,whitelist,blackList)
    blackList.append(V)

#EJERCICIO 7
#número de componentes conexas que componen el grafo.
def countConnections(Grafo):
    verts=[]
    for each in Grafo:
        verts.append(each[0])
    #veo los vertices
    visited=[]
    components=[]
    #bfs asume que no son conexos lo que me sirve para ver los que estan conectados
    for each in verts:
        if each not in visited:
            L=BFS(Grafo,each)
            for each in L:
                visited.append(each)
            components.append(L)
    return len(components)

#EJERCICIO 8 
def convertToBFSTree(Grafo, v):
    Aristas=[]
    if isConnected(Grafo) is True:
        #coloco en la queue el vertice
        queue=[]
        queue.append(v)
        grayList=[]
        grayList.append(v)
        blackList=[]
        while len(queue)>0:
            posc=Search_vertice(queue[0],Grafo)
            aux=queue.pop(0)
            L=Grafo[posc]
            #si no estan sus elementos en la lista gris los agrega 
            for current in L:
                if search_list(grayList,current)==None:
                    grayList.append(current)
                    queue.append(current)
                    Aristas.append((aux,current))
            blackList.append(aux)
    print(blackList)
    print(Aristas)   
    return createGraph(blackList,Aristas)
#EJERCICIO 9
def convertToDFSTree(Grafo):
    grayList=[]
    blackList=[]
    whitelist=[]
    Aristas=[]
    #coloco todos en blanco
    for each in Grafo:
        whitelist.append(each[0])
    for each in Grafo:
        vertex=each[0]
        #busco los nodos que son blancos
        if search_list(whitelist,vertex)!=None:
            DFS_visit_TREE(Grafo,vertex,grayList,whitelist,blackList,Aristas)
    blackList.reverse()
    print(blackList)
    print(Aristas)
    return createGraph(blackList,Aristas)

def DFS_visit_TREE(G,V,grayList,whitelist,blackList,Aristas):
    #saco de los blancos y los pongo en gris
    whitelist.remove(V)
    grayList.append(V)
    posc=Search_vertice(V,G)
    #busco en cada sublista blancos
    for each in G[posc]:
        if search_list(whitelist,each)!=None:
            Aristas.append((each,V))
            DFS_visit_TREE(G,each,grayList,whitelist,blackList,Aristas)
    blackList.append(V)


#EJERCICIO 10???
# Encuentra el camino más corto, en caso de existir, entre dos vértices
def bestRoad(Grafo, v1, v2):
    visitados = []
    queue = deque([v1])
    parent = [v1]
    while queue:
        #popleft() de la cola deque elimina y devuelve el primer elemento de la cola
        values = queue.popleft()
        if values == v2:
            way = []
            while values is not None:
                way.append(values)
                values = parent[values]
            way.reverse()
            return way
        for vecino in Grafo[values]:
            if vecino not in visitados:
                visitados.append(vecino)
                parent[vecino] = values
                queue.append(vecino)
    return None
#EJERCICIO 14 
#PRIM
def PRIM(G):
    # Numero de vertices
    N = len(G)
    selected_node = [0]*N
    U = 0
    selected_node[0] = True
    ListV=[]
    ListA=[]
    while (U < N - 1): #
        vert=search_minimun_edge(N,selected_node,G,ListA)
        selected_node[vert] = True
        U += 1
        ListV.append(vert)
    return createGraph(ListV,ListA)

def search_minimun_edge(N,selected_node,G,ListA):
    minimum = 999999
    a = 0
    b = 0
    for i in range(N):
            if selected_node[i] is True:
                for j in range(N):
                    if selected_node[j] is not True and G[i][j]!=0:  
                        # si hay una arista y el nodo no esta en selectrd
                        if minimum > G[i][j]:
                            minimum = G[i][j]
                            a = i
                            b = j
    aux=(a,b,G[a][b])
    ListA.append(aux)
    return b

#EJERCICIO 15
#KRUSKAL (AACM)
def KRUSKAL(Grafo):
    Arists=[]
    verts=[]
    Makeset=[]
    #veo las aristas, los vertices y la implementacion de make set
    for i in range(0,len(Grafo)):
        if i!=0:
            verts.append(Grafo[0][i])
            Makeset.append([Grafo[0][i]])
            for j in range(0,len(Grafo)):
                if j!=0:
                    a=Grafo[0][i]
                    b=Grafo[j][0]
                    c=Grafo[a+1][b+1]
                    if c!=0 and (((a,b,c) not in Arists) and ((b,a,c) not in Arists)):
                        Arists.append((a,b,c))
    #ordeno pesos
    AS=sort_by_weight(Arists)
    New_arist=[]
    for each in AS:
        a=find_set(each[0],Makeset)
        b=find_set(each[1],Makeset)
        if a is not b:
            New_arist.append(each)
            Union(a,b,Makeset)
    return createGraph(verts,New_arist)

def sort_by_weight(L):
    #ordena por el peso de la arista
    weights=[]
    ArSort=[]
    for each in L:
        weights.append(each[2])
    weights.sort()
    for i in range(0,len(weights)):
        for j in range(0,len(L)):
            if weights[i]==L[j][2]:
                if L[j] not in ArSort: 
                    ArSort.append(L[j])
    return ArSort

def find_set(V,Makeset):
    #busca el conjunto conexo de un vertice dado
    for each in Makeset:
        if V in each:
            return each

def Union(l1,l2,L):
    #une conjuntos conexos
    i=0
    for each in L:
        if l1==each:
            aux=l1
        elif l2==each:
            index=i
        i+=1
    for each in aux:
        L[index].append(each)
    L.remove(l1)

#EJERCIIO 21
#DIJKSTRA

#creamos una clase para los vertice
class Vertex:
    distance=None
    parent=None
    key=None

def shortestPath(Grafo, s, v):
    verts=initRelax(Grafo,s)
    visited=[]
    queue=minqueue(verts)#ordeno por dist
    while len(queue)>0:
        u=queue.pop(0)
        visited.append(u)
        for each in adjunt(u.key,Grafo,verts):# lista de adjuntos
            if each not in visited:
                relax(u,each,Grafo)
        queue=minqueue(queue)
    #bloque para ver S
    a=None
    b=None
    for each in verts:
        if each.key==s:
            a=each
        elif each.key==v:
            b=each
    S_Path=parent_path(b,a)
    return  S_Path

def initRelax(G,s):
    verts=[]
    Nodes=[]
    for i in range(0,len(G)):
        if i!=0:
            verts.append(G[0][i])
    #Relax inicial
    for ve in verts:
        if ve==s:
            newNode=Vertex()
            newNode.key=ve
            newNode.parent=None
            newNode.distance=0
            Nodes.append(newNode)
        else:
            newNode=Vertex()
            newNode.key=ve
            newNode.parent=None
            newNode.distance=9999
            Nodes.append(newNode)
    return Nodes

def adjunt(v,G,verts):
    #lista de vertices adjuntos al v
    adj=[]
    aux=[]
    for i in range(len(G)):
        if i!=0:
            if G[i][0]==v:
                for j in range(0,len(G[i])):
                    if G[i][j]!=0 and j!=0:
                        aux.append(G[0][j])
    for each in verts:
        if each.key in aux:
            adj.append(each)
    return adj

def relax(u,v,G):
    #relaja el vertice actualizando su parent y su distancia
    if v.distance > (u.distance + calculeweight(u.key,v.key,G)):
        v.distance = u.distance + calculeweight(u.key,v.key,G)
        v.parent= u

def calculeweight(u,v,G):
    #calcula el peso de una arista
    a=G[0].index(v)
    a=a
    for i in range(0,len(G)):
        if i!=0 and G[i][0]==u:
            return G[i][a]
        
def minqueue(V):
    #devulve una queue con los nodos ordenados por distancia
    q=[0]*len(V)
    d=[]
    for each in V:
        d.append(each.distance)
    d.sort()
    for i in range(0,len(V)):
        for each in V:
            if d[i]==each.distance and each not in q:
                q[i]=each
    return q

def parent_path(v,s):
    #calcula el camino mas corto mirando los parent
    L=[]
    L.insert(0,v.key)
    aux=True
    while aux!=False:
        if v.parent is not None:
            v=v.parent
            if v.key==s.key:
                aux=False
        else:
            return None
        L.append(v.key)
    return L
