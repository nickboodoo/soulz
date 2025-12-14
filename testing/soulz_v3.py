class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
# FIXME: convert to doubly linked list next
class LinkedList:
    def __init__(self):
        self.head = None
    
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    # FIXME: create a function to append node objects to the list
    def append(self, data):
        pass

    def display(self):
        current = self.head
        while current:
            print(f"{current.data} -> ", end='')
            current = current.next
        print("None")


if __name__ == "__main__":
    print("This is a working new version of soulz")

    new_list = LinkedList()
    new_list.prepend(3)
    new_list.prepend(2)
    new_list.prepend(1)
    
    new_list.display()
