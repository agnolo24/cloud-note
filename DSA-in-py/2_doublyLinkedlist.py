class Node:
    def __init__(self, value):
        self.prev = None # This is to point to the previous node
        self.data = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtEnd(self, value):
        newNode = Node(value)

        if self.head is None:
            self.head = newNode
            return

        temp = self.head
        while temp.next is not None:
            temp = temp.next

        temp.next = newNode
        newNode.prev = temp # pointing to the previous node

    def printLinkedList(self):
        forwardOutput = []
        backwardOutput = []
        temp = self.head

        while temp is not None:
            forwardOutput.append(str(temp.data))
            las = temp
            temp = temp.next

        while las is not None:
            backwardOutput.append(str(las.data))
            las = las.prev

        print(forwardOutput)
        print(backwardOutput)

if __name__ == "__main__":
    linkedList = LinkedList()

    while True:
        inp = input("Enter the value: ")

        if inp == "Qt":
            break

        linkedList.insertAtEnd(inp)

    linkedList.printLinkedList()