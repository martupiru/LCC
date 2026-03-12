#LinkedList Nahman Martina martunahman@gmail.com  L: 13685

class LinkedList:
  head=None
  value=None
  nextNode=None
class Node:
  value=None
  nextNode=None
  
#Función Add
def add(L,element):
	current = L.head
	newNode = Node()
	newNode.value = element

	if current == None:
		L.head = newNode
	else:
		newNode.nextNode = current
		L.head = newNode
	return
  
#Funcion Search
def search(L,element):
	current = L.head
	currentPos = 0

	while current != None:
		if current.value == element:
			return currentPos

		current = current.nextNode
		currentPos += 1
	return
    
#Funcion Insert
def insert(L,element,position):
	current = L.head
	currentPos = 0

	if position == 0:
		add(L,element)
		return position

	elif position > 0:
		if current == None: return
		newNode = Node()
		newNode.value = element

		while current.nextNode != None:
			if currentPos+1 != position:
				current = current.nextNode
				currentPos += 1
			else:
				newNode.nextNode = current.nextNode
				current.nextNode = newNode
				return position
		current.nextNode = newNode
		return currentPos+1
	return
    
#Funcion Delete
def delete(L,element):
	current = L.head
	position = search(L, element)
	if position == None: return
	if position == 0: 
		L.head = L.head.nextNode
		return position

	for i in range(0, position-1):
		current = current.nextNode
	current.nextNode = current.nextNode.nextNode
	return position
  
#Funcion length
def length(L):
	current = L.head
	currentPos = 0
	while current != None:
		current = current.nextNode
		currentPos += 1
	return currentPos

#Función Access
def access(L,position):
	if position >= 0:
		current = L.head

		for i in range(0, position):
			if current == None: return
			current = current.nextNode
		return current.value
	return
  
#Función Update
def update(L,element,position):
	if position >= 0:
		current = L.head

		for i in range(0, position):
			current = current.nextNode
			if current == None: return
		current.value = element
		return position
	return
#funcion para revertir una lista
def revert(L):
  new = LinkedList()
  len = length(L)
  current = L.head

  for i in range(len):
    len -= 1
    add(new, current.value)
    current = current.nextNode
  return new
#funcion para imprimir lista
def print_list(L):
  current = L.head
  currentPos = 0

  while current != None:
    if currentPos != 0: print(end=" -> ")
    print(current.value, end="")
    current = current.nextNode
    currentPos = currentPos + 1
  print()
  return currentPos
#funcion para verificar si dos listas son iguales
def areEqualLists(list1, list2):
  current1 = list1.head
  current2 = list2.head
  equalValues = True

  while current1.nextNode != None and current2.nextNode != None:
    if current1.value != current2.value:
      equalValues = False

    current1 = current1.nextNode
    current2 = current2.nextNode

  return equalValues
def previousNode(L, position):
  count = 0
  current = L.head
  while count < position - 1:
    current = current.nextNode
    count += 1
  return current


def move(L, position_orig, position_dest):
  if position_orig == position_dest: return
  elif position_orig == 0:
    # La head es la posición de origen
    originalNode = L.head

    L.head = L.head.nextNode
    previousDest = previousNode(L, position_dest)

    originalNode.nextNode = previousDest.nextNode
    previousDest.nextNode = originalNode
  elif position_dest == 0:
    # La head es la posición de destino
    previousOrig = previousNode(L, position_orig)
    originalNode = previousOrig.nextNode

    if previousOrig.nextNode != None:
      previousOrig.nextNode = previousOrig.nextNode.nextNode
    else:
      previousOrig.nextNode = None

    originalNode.nextNode = L.head
    L.head = originalNode
  else:
    previousOrig = previousNode(L, position_orig)
    originalNode = previousOrig.nextNode

    if previousOrig.nextNode != None:
      previousOrig.nextNode = previousOrig.nextNode.nextNode
    else:
      previousOrig.nextNode = None

    previousDest = previousNode(L, position_dest)
    originalNode.nextNode = previousDest.nextNode
    previousDest.nextNode = originalNode


def orderList(L):
  current = L.head
  count = 0

  while current.nextNode != None:
    if (current.value > current.nextNode.value):
      move(L, findNode(L, current.nextNode), count)
      return orderList(L)
    else:
      current = current.nextNode
      count += 1


def findNode(L, node):
  current = L.head
  count = 0

  while current != None:
    current = current.nextNode
    count += 1
    if current == node: return count