class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        
# FIXME: convert to doubly linked list next
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    
    
    def prepend(self, data):
        new_node = Node(data)
        
        # else:
        #     new_node.next = self.head
        #     self.head.prev = new_node
        #     self.head = new_node
    
    # FIXME: create a function to append node objects to the list
    def append(self, data):
        new_node = Node(data)

        if self.tail is None:
            self.head = self.tail = new_node
        
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

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
