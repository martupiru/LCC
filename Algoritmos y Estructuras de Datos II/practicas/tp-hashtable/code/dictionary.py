#TP HASH TABLE NAHMAN MARTINA L:13685

def CreateHashTable(Dim):
    Hash=[]
    #crea un Hash de M posciones
    for i in range (0,Dim):
        L=[]
        Hash.append(L)
    return Hash

def printHashTable(D):
    count=0
    for each in D:
        print("[",count,"]","--->",end="")
        print(each)
        print("----")
        count+=1
        
#haski
def hash_mode(k,m):
    return (k%m)
def hash_subcadena(k,m):
    for i in range (len(k)):
        sum = ord(k[i])*(10**i)
    return(sum%m)


def insert(D,key,value):
    if len(D)==0 or D==None:
        print("crear tabla hash con la funcion CreateHashTable")
        return None
    else:
        index=hash_mode(key,len(D))
        if D[index]==None:
            list=[]
            tupla=(key,value)
            list.append(tupla)
            D[index]=list
        else:
            tupla=(key,value)
            D[index].append(tupla)

def search(D,key):
    index=hash_mode(key,len(D))
    for elemento in D[index]:
        if elemento[0]==key:
            return (elemento[1])

def delete (D,key):
    if search(D,key)!=None:
        index=hash_mode(key,len(D))
        for i in range (len(D[index])):
            if D[index][i][0]==key:
                #pop elimina el elemento
                D[index].pop(i)
                return D
                


