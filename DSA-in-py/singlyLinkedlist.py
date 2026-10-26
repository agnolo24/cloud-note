class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_end(self, val):
        new_node = Node(val)
        
        # Scenario A: If list is empty, this is the first and only node
        if self.head is None:
            self.head = new_node
            return
        
        # Scenario B: Traverse to the absolute end of the chain
        temp = self.head
        while temp.next is not None:
            temp = temp.next
            
        # CRITICAL FIX: Link the current last node to the new node
        temp.next = new_node 

    def print_list(self):
        temp = self.head
        output = []
        
        # Collect all values first to guarantee they print on one line
        while temp is not None:
            output.append(str(temp.data))
            temp = temp.next
            
        # Join them cleanly with arrows
        print(" -> ".join(output) + " -> None")

# Test execution
my_list = LinkedList()
my_list.insert_at_end(10)
my_list.insert_at_end(20)
my_list.insert_at_end(30)
my_list.insert_at_end(40)

print("Linked List elements:")
my_list.print_list()
