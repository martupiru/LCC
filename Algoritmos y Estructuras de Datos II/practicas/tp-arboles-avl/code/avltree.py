#AVL TREE NAHMAN MARTINA L: 13685
class AVLTree:
	root = None

class AVLNode:
    parent = None
    leftnode = None
    rightnode = None
    key = None
    value = None
    bf = None

   
#rotacion izq
def rotateLeft(Tree,avlnode):
    new_root = avlnode.rightnode
    avlnode.rightnode = new_root.leftnode
    if new_root.leftnode != None:
        new_root.leftnode.parent = avlnode
    new_root.parent = avlnode.parent
    if avlnode.parent == None:
        Tree.root = new_root
    else:
        if avlnode.parent.leftnode == avlnode:
            avlnode.parent.leftnode = new_root
        else:
            avlnode.parent.leftnode = new_root
    new_root.leftnode = avlnode
    avlnode.parent = new_root.leftnode

#rotacion derecha
def rotateRight(Tree,avlnode):
    new_root = avlnode.leftnode
    avlnode.leftnode = new_root.rightnode
    if new_root.rightnode != None:
        new_root.rightnode.parent = avlnode
    new_root.parent = avlnode.parent
    if avlnode.parent == None:
        Tree.root = new_root
    else:
        if avlnode.parent.rightnode == avlnode:
            avlnode.parent.rightnode = new_root
        else:
            avlnode.parent.leftnode = new_root
    new_root.rightnode = avlnode
    avlnode.parent = new_root.rightnode

# calcular altura del nodo
def altura(node):
    if node != None:
        return (1+max(altura(node.leftnode),altura(node.rightnode)))
    else:
        return 0
    
#calcular bf de cada nodo
def calculateBalance(AVLTree):
    node = AVLTree.root
    if node != None:
        calculateBalance_node(node)
    return 

def calculateBalance_node(node):
    if node != None:
        node.bf = altura(node.leftnode)-altura(node.rightnode)
        calculateBalance_node(node.leftnode)
        calculateBalance_node(node.rightnode)

#buscamos nodo desbalanceado para rebalancear el arbol
def find_node_desbalance(AVLTree):
    calculateBalance_node(AVLTree)
    node = AVLTree.root
    if node != None:
        return(find_node_desbalanceR(node))
    
def find_node_desbalanceR(node):
    if node != None:
        if node.bf != 1 and node.bf != 0 and node.bf != -1:
            return node
        find_node_desbalanceR(node.leftnode)
        find_node_desbalanceR(node.rightnode)

#rebalanceamos el arbol
def reBalance(AVLTree):
    bf_arbol = calculateBalance_node(AVLTree.root)
    if bf_arbol != 1 and bf_arbol != 0 and bf_arbol != -1:
        node = find_node_desbalance(AVLTree)
        reBalanceR(AVLTree,node)

def reBalanceR(AVLTree,node):
    if node.bf < -1:
        if node.rightnode.bf == 1:
            rotateRight(AVLTree,node.rightnode)
            rotateLeft(AVLTree, node)
        else:
            rotateLeft(AVLTree, node)
    if node.bf > 1:
        if node.leftnode.bf == -1:
            rotateLeft(AVLTree, node.leftnode)
            rotateRight(AVLTree, node)
        else:
            rotateRight(AVLTree, node)

#insert binarytree modificado para AVLT
def insertR(B,newnode, currentnode):
    if newnode.key>currentnode.key:
        if currentnode.rightnode==None:
            newnode.parent=currentnode
            currentnode.rightnode=newnode
            #cuando ya insertamos tenemos que chequear que el arbol siga siendo AVL
            node_desbalance=check_balance_parent(newnode)
            if node_desbalance != None:
                reBalanceR(B, node_desbalance)
            return newnode.key
        else:
            return insertR(newnode, currentnode.rightnode)
    elif newnode.key<currentnode.key:
        if currentnode.leftnode==None:
            newnode.parent=currentnode
            currentnode.leftnode=newnode
            #chequeamos solo subiendo en el arbol
            node_desbalance=check_balance_parent(newnode)
            if node_desbalance != None:
                reBalanceR(B, node_desbalance)

            return newnode.key
        else:
            return insertR(newnode, currentnode.leftnode)
    else:
        return None

def check_balance_parent(node):
    while node != None:
        calculateBalance_node(node)
        if node.bf >1 or node.bf <-1:
            return node
        node=node.parent
    return None

def insert(B,element,key):
    newnode=AVLNode()
    newnode.value=element
    newnode.key=key
    currentnode=B.root
    if B.root==None:
        B.root=newnode
    else:
        return insertR(B,newnode, currentnode)

#Funcion delete
def deleteR(B,deletingnode):
    if deletingnode!=None:
        #Caso 1: Hoja
        if deletingnode.leftnode==None and deletingnode.rightnode==None:
            if deletingnode==B.root:
                B.root=None
                return deletingnode.key
            else:
                padre=deletingnode.parent
                #Me fijo si el nodo a eliminar es el hijo derecho o izquierdo de su padre
                if padre.rightnode==deletingnode:
                    padre.rightnode=None
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key
                else:
                    padre.leftnode=None
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key               
        #Caso 2: Un solo hijo
        #Si es el hijo izquierdo
        elif deletingnode.rightnode==None:
            if deletingnode==B.root:
                B.root=deletingnode.leftnode
                return deletingnode.key
            else:
                padre=deletingnode.parent
                #Me fijo si el nodo a eliminar es el hijo derecho o izquierdo de su padre
                if padre.rightnode==deletingnode:
                    padre.rightnode=deletingnode.leftnode
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key
                else:
                    padre.leftnode=deletingnode.leftnode
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key
        #Si es el hijo derecho            
        elif deletingnode.leftnode==None:
            if deletingnode==B.root:
                B.root=deletingnode.rightnode
                return deletingnode.key
            else:
                padre=deletingnode.parent
                #Me fijo si el nodo a eliminar es el hijo derecho o izquierdo de su padre
                if padre.rightnode==deletingnode:
                    padre.rightnode=deletingnode.rightnode
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key
                else:
                    padre.leftnode=deletingnode.rightnode
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                    return deletingnode.key         
        #Caso 3: Dos hijos
        else:
            aux1=deletingnode.rightnode
            aux2=deletingnode.leftnode
            #Buscamos al mayor de menores
            mayor=mayordemenores(deletingnode)
            #En el caso de que el mayor de menores tenga hijos izquierdos y no sea el hijo izquierdo del nodo a eliminar:
            if mayor.leftnode!=None and mayor!=aux2:
                menor=menorhijoizq(mayor)
                #Para evitar crear un ciclo con padres=hijos
                if menor.parent!=deletingnode.leftnode:
                    menor.leftnode=aux2
            elif mayor.leftnode==None and mayor!=aux2:
                mayor.leftnode=aux2
            mayor.rightnode=aux1        

            if deletingnode==B.root:
                B.root=mayor
            else:
                padre=deletingnode.parent
                mayor.parent=padre 
                if padre.rightnode==deletingnode:
                    padre.rightnode=mayor
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)
                else:
                    padre.leftnode=mayor
                    node_desbalance=check_balance_parent(padre)
                    if node_desbalance != None:
                        reBalanceR(B, node_desbalance)

            return deletingnode.key
    else:
        return None

#Funcion que encuentra el nodo mayor entre los hijos menores de un nodo
def mayordemenores(node):
    currentnode=node.leftnode
    while currentnode.rightnode!=None:
        currentnode=currentnode.rightnode
    currentnode.parent.rightnode=None
    return currentnode

#Funcion que encuentra el ultimo hijo menor dentro de una rama
def menorhijoizq(node):
    if node.leftnode==None:
        return node
    else:
        return menorhijoizq(node.leftnode)

def delete(B,element):
    currentnode=B.root
    deletingnode=searchR(currentnode, element)
    return deleteR(B,deletingnode)

def searchR(currentnode,element):
    if currentnode!=None:
        if element==currentnode.value:
            return currentnode        
        else:
            izq= searchR(currentnode.leftnode,element)
            der= searchR(currentnode.rightnode,element)
            if izq==None and der==None:
                return None
            elif izq==None:
                return der
            elif der==None:
                return izq
    else:
        return None
   
def search(AVL,element):
    currentnode=AVL.root
    result=searchR(currentnode, element)
    if result!=None:
        return result.key
    else:
        return None