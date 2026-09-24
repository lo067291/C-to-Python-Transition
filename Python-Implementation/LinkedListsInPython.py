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
    def insert_end(self, item):
        """
        Insert at end of List
        Time Complexity: O(n)
        """
        new_node = Node(item)
        #Case 1: Empty List
        if self.head is None:
            self.head = new_node
            return
        #Case 2: Teaverse to end, insert
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
    def insert_sorted(self, item):
        """
        Insert in ascending order; the existing list must be sorted.
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
        while current.next is not None and current.next.data < item:
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

def read_integer(prompt):
    """Read an integer; return None when input ends."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
        except EOFError:
            return None


def main():
    ll = LinkedList()
    while True:
        choice = read_integer(
            "\nMenu: 1. insert front, 2. insert end, 3. delete, "
            "5. sorted insert (ascending list required), 4. exit: "
        )
        if choice is None or choice == 4:
            print("\nGOOD BYE>>>>")
            break
        if choice not in (1, 2, 3, 5):
            print("Invalid option. Please try again.")
            continue
        data = read_integer("\nEnter data: ")
        if data is None:
            break
        if choice == 1:
            ll.insert_front(data)
        elif choice == 2:
            ll.insert_end(data)
        elif choice == 3:
            ll.delete(data)
        else:
            ll.insert_sorted(data)
        ll.display()


if __name__ == "__main__":
    main()
