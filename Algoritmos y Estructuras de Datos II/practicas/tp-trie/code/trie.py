#TAD trie NAHMAN MARTINA L:13685
from itertools import cycle
class Trie:
	root = None

class TrieNode:
    parent = None
    children = None   
    key = None
    isEndOfWord = False

#INSERT
def insert(T, elemento):
    if T.root == None:
        T.root = TrieNode()
        T.root.children = []
    current = T.root
    for i in range(len(elemento)):
        new_node = search_children(current.children, elemento[i])
        if new_node != None:
            current = new_node
        else:
            nodo = TrieNode()
            nodo.key = elemento[i]
            nodo.children = []
            current.children.append(nodo)
            nodo.parent = current
            current = nodo
    current.isEndOfWord = True

#SEARCH
def search(T, palabra):
    current = T.root
    for letra in palabra:
        new_node = search_children(current.children, letra)
        if new_node != None:
            current = new_node
        else:
            return False
    if current.isEndOfWord == True:
        return True

def search_children(array, caracter):
    for i in range(len(array)):
        if array[i] != None:
            if array[i].key == caracter:
                return array[i]
    return None

#DELETE
def delete(T,palabra):
    #caso1 El elemento no se encuentra en el trie
    encontrado=search (T,palabra)
    if encontrado == False:
        return False
    
    else:
        #buscar el nodo fin de la palabra
        nodo_final=search_ultimonodo(T,palabra)
        nodo_final.isEndOfWord=False  
        flag = True
        while flag:
           if nodo_final.children != None or len(nodo_final.children)>0  or nodo_final.parent != T.root or nodo_final.isEndOfWord==True:
               flag = False
           else:
               nodo_final=nodo_final.parent
        nodo_final.parent.remove(nodo_final)
        return True
    
def search_ultimonodo(T, palabra):
    current = T.root
    """falta si el len de la palabra el 1 devolver ese"""
    for i in range(len(palabra)-1):
        if i == (len(palabra)-1) and new_node.isEndOfWord == True:
            return new_node
        else:
            new_node = search_children(current.children, palabra[i])

#EJERCICIO 4   
def prefijo(T,p):
    pre=[]
    children=cycle(T.root.children)
    current=next(children)
    for i in range (len(p)):
        while current.key != p[i]:
            children=cycle(current.children)
            current=next(children)
        if current.key == p[i]:
            pre.append(current)
                
    if len(pre) !=0:
        return pre[len(pre)-1]#devuelve el ultimo nodo
    else:
        return None

def patron(T,p,n):
    palabras=[]
    nodo=prefijo(T,p)
    traverse_level(nodo,p,palabras,n)
    return palabras

def traverse_level(nodo,prefijo,palabras,n):
    if nodo.isEndOfWord==True and len(prefijo)==n:
        palabras.append(prefijo)
    for i in range (len(nodo.children)):
        traverse_level(nodo.children[i],prefijo+ nodo.children[i].key,palabras,n)

#EJERCICIO 5
#COMPLEJIDAD O(n)

#Recorre Arbol y nos guarda la palabras 
def traverse(nodo,prefijo,palabras):
    if nodo.isEndOfWord==True:
        palabras.append(prefijo)
    for i in range (len(nodo.children)):
        traverse(nodo.children[i],prefijo+ nodo.children[i].key,palabras)
               
def get_words(T):
    words = []
    traverse(T.root, '', words)
    return words

def is_sublist(lst1, lst2):
    return set(lst1).issubset(set(lst2))

#EJERCICIO 6
def palabras_invertidas(T):
    words= get_words(T)
    return has_inverted_list(words)

""" [::-1] se utiliza para obtener la list invertida"""
def has_inverted_list(lst):
    for sublst in lst:
        if sublst[::-1] in lst:
            return True
    return False

#EJERCICIO 7
def autoCompletar(T, cadena):
    Node= T.root
    cadaux=""
    cont = 0
    aux=NodeFinal(T,cadena,Node,cont)
    Completar=Complete(aux.children,cadaux)
    return Completar

#recorro los nodos hasta encontrar uno que es una lista con mas de un elemto
def Complete(node,cadena):
    if node == None:
        return cadena
    if len(node)>1:
        return cadena
    else:
        for i in range (0,len(node)):
            if node[i].isEndOfWord == True:
                cadena = cadena+node[i].key
                return cadena
            else:
                cadena = cadena+node[i].key
            return Complete(node[i].children,cadena)
        
#recorro el arbol y devuelvo nodo final de palabra(puede no ser endofword)
def NodeFinal(T,element,node,cont):
    if node.children != None:
        if cont<len(element):
            for i in range (0,len(node.children)):
                if node.children[i].key == element[cont]:
                    cont = cont + 1
                    if cont == len(element):
                        return node.children[i]
                    return NodeFinal(T,element,node.children[i],cont)





     