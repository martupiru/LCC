#TAD ARBOL Nahman Martina martunahman@gmail.com  L: 13685
from linkedlist import *
class Node:
    value = None
    nextNode = None
class LinkedList:
    head = None
def enqueue(Q,element):
  add(Q, element)
def dequeue(Q):
  if Q.head!= None:
    current=Q.head
    while current!=None:
      node=current
      current=current.nextNode
    value=node.value
    delete(Q,value)
    return value
  else:
    return None