#TAD ARBOL Nahman Martina martunahman@gmail.com  L: 13685
from linkedlist import *
from myqueue import *

class BinaryTree:
    root = None


class BinaryTreeNode:
    key = None
    value = None
    leftnode = None
    rightnode = None
    parent = None

''' Descripción: Busca un elemento en el TAD árbol binario.
Salida: Devuelve la key asociada a la primera instancia del elemento. Devuelve None si el elemento no se encuentra. '''


def Search(B, element): 
    node = SearchNodeR(B.root, element)
    if node == None: return
    else: return node.key

# Función recursiva de search
def SearchNodeR(node, element):
    if node == None: return

    if node.value == element:
        return node

    right = SearchNodeR(node.rightnode, element)
    if right != None:
        return right

    left = SearchNodeR(node.leftnode, element)
    if left != None:
        return left

''' Descripción: Busca un elemento en el TAD árbol binario.
Salida: Devuelve el nodo asociada a la primera instancia del elemento. Devuelve None si el elemento no se encuentra. '''


def SearchNode(B, element):
    return SearchNodeR(B.root, element)


''' Descripción: Inserta un elemento con una clave determinada del TAD árbol binario.
Salida: Si pudo insertar con éxito devuelve la key donde se inserta el elemento. En caso contrario devuelve None. '''


def Insert(B, element, key): 
    newNode = BinaryTreeNode()
    newNode.key = key
    newNode.value = element

    if (B.root == None):
        B.root = newNode
        return key
    return InsertR(newNode, B.root)


# Función recursiva de insert
def InsertR(newNode, currentNode):
    if newNode.key > currentNode.key:
        if currentNode.rightnode == None:
            newNode.parent = currentNode
            currentNode.rightnode = newNode
            return newNode.key
        else:
            right = InsertR(newNode, currentNode.rightnode)
            if right != None:
                return right
    else:
        if currentNode.leftnode == None:
            newNode.parent = currentNode
            currentNode.leftnode = newNode
            return newNode.key
        else:
            left = InsertR(newNode, currentNode.leftnode)
            if left != None:
                return left


''' Descripción: Elimina un elemento del TAD árbol binario.
Poscondición: Se debe desvincular el Node a eliminar.
Salida: Devuelve clave (key) del elemento '''


def Delete(B, element): 
    node = SearchNode(B, element)
    if node == None: return
    else: return DeleteCurrentCase(B, node)


# Valida y ejecuta los distintos casos de delete
def DeleteCurrentCase(B, node):
    if node.rightnode == None:
        if node.leftnode == None:

            # Caso 1: El nodo a eliminar es una hoja
            if node.parent.leftnode != None and node.parent.leftnode == node:
                node.parent.leftnode = None
                return node.key
            elif node.parent.rightnode != None and node.parent.rightnode == node:
                node.parent.rightnode = None
                return node.key

        # Caso 2: El nodo a eliminar tiene un hijo del lado izquierdo
        if node.parent.leftnode != None and node.parent.leftnode == node:
            node.parent.leftnode = node.leftnode
            return node.key
        elif node.parent.rightnode != None and node.parent.rightnode == node:
            node.parent.rightnode = node.leftnode
            return node.key

    else:
        # Caso 2: El nodo a eliminar tiene un hijo del lado derecho
        if node.leftnode == None:
            if node.parent.leftnode == node:
                node.parent.leftnode = node.rightnode
                return node.key
            elif node.parent.rightnode == node:
                node.parent.rightnode = node.rightnode
                return node.key
        else:
            # Caso 3: El nodo a eliminar tiene dos hijos
            ''' # eliminar el menor de sus mayores   '''
            changeNode = SmallerOf(node.rightnode)

            node.value = changeNode.value
            oldKey = node.key
            node.key = changeNode.key

            if changeNode.parent.leftnode == changeNode:
                changeNode.parent.leftnode = None
            elif changeNode.parent.rightnode == changeNode:
                changeNode.parent.rightnode = None

            return oldKey

            # o eliminar el mayor de sus menores
            changeNode = Bigger(node.leftnode)

            node.value = changeNode.value
            oldKey = node.key
            node.key = changeNode.key

            if changeNode.parent.leftnode == changeNode:
                changeNode.parent.leftnode = None
            elif changeNode.parent.rightnode == changeNode:
                changeNode.parent.rightnode = None

            return oldKey


# Devuelve el elemento con menor key desde un nodo dado
def Smaller(node):
    if node.leftnode != None:
        current = Smaller(node.leftnode)
        if current != None:
            return current
    else:
        return node


# Devuelve el elemento con mayor key desde un nodo dado
def Bigger(node):
    if node.rightnode != None:
        current = Bigger(node.rightnode)
        if current != None:
            return current
    else:
        return node


def SmallerOf(node):
    if node.leftnode != None:
        changeNode = SmallerOf(node.leftnode)
        if changeNode != None:
            return changeNode
    elif node.rightnode != None:
        changeNode = SmallerOf(node.rightnode)
        if changeNode != None:
            return changeNode
    else:
        return node


def BiggerOf(node):
    if node.rightnode != None:
        changeNode = BiggerOf(node.rightnode)
        if changeNode != None:
            return changeNode
    elif node.leftnode != None:
        changeNode = BiggerOf(node.leftnode)
        if changeNode != None:
            return changeNode
    else:
        return node


'''Descripción: Elimina una clave del TAD árbol binario.
Poscondición: Se debe desvincular el Node a eliminar.
Salida: Devuelve clave (key) a eliminar. Devuelve None si el elemento a eliminar no se encuentra. '''


def DeleteKey(B, key):
    node = SearchKeyR(B.root, key)
    if node == None: return
    else: return DeleteCurrentCase(B, node)


# Función recursiva de searchKey
def SearchKeyR(node, key):
    if node == None: return

    if node.key == key:
        return node

    right = SearchKeyR(node.rightnode, key)
    if right != None:
        return right

    left = SearchKeyR(node.leftnode, key)
    if left != None:
        return left


''' Descripción: Permite acceder a un elemento del árbol binario con una clave determinada.
Salida: Devuelve el valor de un elemento con una key del árbol binario, devuelve None si no existe elemento con dicha clave. '''


def Access(B, key):
    node = SearchKeyR(B.root, key)
    if node == None: return
    else: return node.value


''' Descripción: Permite cambiar el valor de un elemento del árbol binario con una clave determinada.
Entrada: El árbol binario (BinaryTree) y la clave (key) sobre la cual se quiere asignar el valor de element.
Salida: Devuelve None si no existe elemento para dicha clave. Caso contrario devuelve la clave del nodo donde se hizo el update. '''


def Update(B, element, key):
    node = SearchKeyR(B.root, key)
    if node == None: return
    else:
        node.value = element
        return node.key


''' Descripción: Recorre un árbol binario en orden
Entrada: El árbol binario (BinaryTree)
Salida: Devuelve una lista (LinkedList) con los elementos del árbol en orden. Devuelve None si el árbol está vacío. '''

#IRD
def traverseInOrder(B):
    L = LinkedList()
    traverseInOrderR(B.root, L)
    return revert(L)


# Función recursiva de traverseInOrder
def traverseInOrderR(node, L):
    if node != None:
        traverseInOrderR(node.leftnode, L)
        add(L, node.value)
        traverseInOrderR(node.rightnode, L)


''' Descripción: Recorre un árbol binario en post-orden
Entrada: El árbol binario (BinaryTree)
Salida: Devuelve una lista (LinkedList) con los elementos del árbol en post-orden. Devuelve None si el árbol está vacío. '''

#IDR
def traverseInPostOrder(B):
    L = LinkedList()
    traverseInPostOrderR(B.root, L)
    return revert(L)


#Funcion recursiva de traverseInPostOrder
def traverseInPostOrderR(node, L):
    if node != None:
        traverseInPostOrderR(node.leftnode, L)
        traverseInPostOrderR(node.rightnode, L)
        add(L, node.value)


''' Descripción: Recorre un árbol binario en pre-orden
Entrada: El árbol binario (BinaryTree)
Salida: Devuelve una lista (LinkedList) con los elementos del árbol en pre-orden. Devuelve None si el árbol está vacío. '''

#RID
def traverseInPreOrder(B):
    L = LinkedList()
    traverseInPreOrderR(B.root, L)
    return revert(L)


# Función recursiva de traverseInPreOrder
def traverseInPreOrderR(node, L):
    if node != None:
        add(L, node.value)
        traverseInPreOrderR(node.leftnode, L)
        traverseInPreOrderR(node.rightnode, L)


from myqueue import enqueue, dequeue
''' Descripción: Recorre un árbol binario en modo primero anchura/amplitud
Entrada: El árbol binario (BinaryTree)
Salida: Devuelve una lista (LinkedList) con los elementos del árbol ordenados de acuerdo al modo primero en amplitud. Devuelve None si el árbol está vacío. '''


def traverseBreadFirst(B):
    queue = LinkedList()
    valuesQueue = LinkedList()
    enqueue(queue, B.root)
    while queue.head != None:
        node = dequeue(queue)
        enqueue(valuesQueue, node.value)

        if node.leftnode != None:
            enqueue(queue, node.leftnode)
        if node.rightnode != None:
            enqueue(queue, node.rightnode)
    return revert(valuesQueue)
