#TP COMPLEJIDAD NAHMAN MARTINA 13685
from linkedlist import *
#Ejercicio 4 
def order_list(List):
  #Encuentro el elemento del medio
  pivot = List[len(List)//2]
  menores = []
  mayores = []
  #Recorremos lista y llenamos las otras
  for i in range(len(List)):
    if i == pivot:
      continue
    if List[i] < List[pivot]:
      menores.append(List[i])
    else:
      mayores.append(List[i])
  menores_new = orderList(menores)
  mayores_new = order_list(mayores)
  # + concatena las listas y forma la nueva lista
  return menores_new + [List[pivot]] + mayores_new

#Ejercicio 5 
def ContieneSuma(A, n):
  current = A.head
  aux = A.head
  if aux.value+current.nextNode.value==n:
    return True
  else:
    while current != None and aux != None: #o(n) peor caso-#O(C)
      if current.nextnode != None:
        if aux.value + current.nextnode.value == n:
          return True
        current = current.nextNode
      else:
        aux = aux.nextNode
        current = aux
    return