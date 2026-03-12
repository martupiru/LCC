#Ejercicios Hash Table NAHMAN MARTINA L:13685
from dictionary import *

#ejercicio 4 
def string_permutation(s,p):
    if len(s)!=len(p):
        return False
    else:
        dicS=[None]*(ord("z")-ord("a"))
        dicP=[None]*(ord("z")-ord("a"))
        for i in range(len(s)):
            dicS.Insert(hash_mode(ord(s[i])-ord("a"),len(dicS)),s[i])
        for i in range(len(p)):
            dicP.Insert(hash_mode(ord(p[i])-ord("a"),len(dicP)),p[i])
        for i in range(len(dicS)):
            if dicS[i] !=None:
                if len(dicS[i])!=len(dicP[i]):
                    return False
        return True
    
#ejercicio 5
def list_repetidos(L):
    D=[None]*len(L)
    for i in range (len(L)):
        if search(D,L[i]) !=None:
            return False
        insert(D,L[i],L[i])
    return True
"""El coste de tiempo es O(n^2) ya que entra al bucle n veces y el search es O(n)
 Las operaciones de insert en el diccionario son O(1)"""

#ejercicio 6
def hash_code(code):
    for i in range(len(code)):
        if code[i].isdigit():
            num=num+code[i]
        else:
            num=num+ord(code[i])
    return(hash_mode(num,len(code)))

#ejercicio 7
def compre_char(cadena):
    letra=cadena[0]
    cadena_nueva=''
    cont=1
    for i in range (len(cadena)):
        if i !=0:
            if letra==cadena[i]:
                cont=cont+1
            else:
                cadena_nueva=cadena_nueva+letra+str(cont)
                cont=1
                letra=cadena[i]
    cadena_nueva += letra + str(cont)
    if (len(cadena_nueva)<(len(cadena))):
        return cadena_nueva
    else:
        return cadena
"El costo de tiempo es O(n). Está dado por el for"    

#ejercicio 8
def ocurrencia (cadena,subcadena):
    dictionary=[]
    for i in range (len(cadena)-len(subcadena)+1):
        sublista=[]
       
        for j in range (len(subcadena)):  
            sublista.insert(j,cadena[i+j])
        tupla=(sublista,i)
        dictionary.insert(hash_subcadena(sublista,len(cadena)),tupla)
    haski_p=hash_subcadena(subcadena,len(cadena)) #key de la subcadena
    print(dictionary)
    print((dictionary[haski_p][1]))
    return(dictionary[haski_p][1]) #devuelve la posicion de la cadena donde se encontro la subacadena
"""El costo de tiempo es O(n^2) dado por los for anidados
Las operaciones de insert en el diccionario son O(1)"""

#ejercicio 9
def conjuntos(S,T):
    hash=CreateHashTable(len(T))
    for numeroT in T:
        insert(hash,hash_mode(numeroT,len(T)),numeroT)
    for numeroS in S:
        if search(hash,hash_mode(numeroS,len(T))) != numeroS:
            return False
    return True


