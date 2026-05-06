"""
Linked List Implementation in Python
Author: Logan Stacy
UCF Computer Engineering

This implementation demonstrates:
- Object-oriented approach with classes
- Automatic memory management (garbage collection)
- Python's cleaner syntax compared to C
"""
class Node:
    """
    Node class represents a single element in the linked list. Equivalent to
    C's struct node.
    """

    """Set the data and next node just like in C"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    LinkedList class manages the entire list
    Contains all operations: insert, delete, display, etc.
    """
    def __init__(self):
        self.head = None
    def insert_front(self, item):
        """
        Insert at front of list
        Time complexity: O(1)
        Comparison: In C the function returned a NEW head. In Python, self.head is updated
        directly.
        """
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
    def insert_end(selfself, item):
        """
        Insert at end of List
        Time Complexity: O(n)
        """
        #Case 1: Empty List
        if self.head is None:
            self.head = Node(item)
            return
        #Case 2: Teaverse to end, insert
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
    def insert_sorted(self, item):
        """
        Insert in sorted order (descending)
        Time Complexity: O(n)
        """
        new_node = Node(item)
        #Case 1: Empty List (front)
        if self.head is None or self.head.data > item:
            new_node.next = self.head
            self.head = new_node
            return
        #Case 2: Find insertion point
        current = self.head
        while current.next is not None and current.next.data > item:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def delete(self, item):
        """
        Delete first occurence of item
        Time Complexity: O(n)

        Comparison: In C manual free() is required. In Python, the garbage collector handles memory
        """
        #Case 1: Empty List
        if self.head is None:
            return
        #Case 2: Delete first node
        if self.head.data == item:
            self.head = self.head.next #Old head gets garbage collected
            return
        #Case 3: Find and delete middle/end node
        current = self.head
        while current.next is not None and current.next.data != item:
            current = current.next
        if current.next is None:
            return
        current.next = current.next.next #Deleted node gets garbage collected
    def display(self):
        """Display all elements in list"""
        print("\nPrinting Linked List.....", end="")
        current = self.head
        while current is not None:
            print(current.data, end=" ")
            current = current.next
        print()

    def main():
        """
        Main menu loop - equivalent to C's main()
        """
        ll = LinkedList()

        while True:
            print("\nMenu: 1. insert front, 2. insert end, 3. delete, 5. sorted insert, 4. exit: ", end="")
            try:
                choice = int(input())
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 4:
                print("\nGOOD BYE>>>>")
                break

            elif choice == 1:
                print("\nEnter data: ", end="")
                data = int(input())
                ll.insert_front(data)
                ll.display()

            elif choice == 2:
                print("\nEnter data: ", end="")
                data = int(input())
                ll.insert_end(data)
                ll.display()

            elif choice == 3:
                print("\nEnter data to delete: ", end="")
                data = int(input())
                ll.delete(data)
                ll.display()

            elif choice == 5:
                print("\nEnter data: ", end="")
                data = int(input())
                ll.insert_sorted(data)
                ll.display()

            else:
                print("Invalid option. Please try again.")

    if __name__ == "__main__":
        main()