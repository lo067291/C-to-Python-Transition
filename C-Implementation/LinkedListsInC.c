// Linked List Implementation in C
// Course: COP 3502C - Computer Science 1
// Author: Logan Stacy
// UCF Computer Engineering

// This implementation demonstrates:
// - Manual memory management (malloc/free)
// - Pointer manipulation
// - Struct-based data structures

#include<stdio.h>
#include<stdlib.h>

typedef struct node {
    int data;
    struct node* next;
} node;

// Creates a new node with given data
// Returns pointer to allocated node
node* create_node(int item) {
    node* temp = (node*)malloc(sizeof(node));
    temp->data = item;
    temp->next = NULL;
    return temp;
}

// Inserts node at front of list
// Time complexity: O(1)
node* insert_front(node* head, int item) {
    node* temp = create_node(item);
    temp->next = head;
    return temp;
}

// Inserts node in sorted order (descending)
// Time complexity: O(n)
node* insert_sorted(node* head, int item) {
    node* temp = create_node(item);
    
    // Case 1: Empty list or insert at front
    if (head == NULL || head->data > item) {
        temp->next = head;
        return temp;
    }
    
    // Case 2: Find insertion point
    node* current = head;
    while (current->next != NULL && current->next->data < item) {
        current = current->next;
    }
    
    temp->next = current->next;
    current->next = temp;
    return head;
}

// Inserts node at end of list
// Time complexity: O(n)
node* insert_end(node* root, int item) {
    node* temp = create_node(item);
    
    // Case 1: Empty list
    if (root == NULL) {
        return temp;
    }
    
    // Case 2: Traverse to end
    node* temp2 = root;
    while (temp2->next != NULL) {
        temp2 = temp2->next;
    }
    temp2->next = temp;
    
    return root;
}

// Deletes first occurrence of item from list
// Frees memory of deleted node
// Time complexity: O(n)
node* DelList(node* head, int item) {
    // Case 1: Empty list
    if (head == NULL) return head;
    
    // Case 2: Delete first node
    if (head->data == item) {
        node* temp = head->next;
        free(head);  // IMPORTANT: Manual memory cleanup
        return temp;
    }
    
    // Case 3: Find and delete middle/end node
    node* temp = head;
    while (temp->next != NULL && temp->next->data != item) {
        temp = temp->next;
    }
    
    if (temp->next == NULL) {
        return head;  // Item not found
    }
    
    node* temp2 = temp->next;
    temp->next = temp->next->next;
    free(temp2);  // IMPORTANT: Manual memory cleanup
    
    return head;
}

// Displays all elements in list
void display(node* t) {
    printf("\nPrinting your linked list.......");
    while(t != NULL) {
        printf("%d ", t->data);
        t = t->next;
    }
    printf("\n");
}

int main() {
    node* root = NULL;
    int ch, ele, del;
    
    while(1) {
        printf("\nMenu: 1. insert front, 2. insert end, 3. delete, 5. sorted insert, 4. exit: ");
        scanf("%d", &ch);
        
        if(ch == 4) {
            printf("\nGOOD BYE>>>>\n");
            break;
        }
        if(ch == 1) {
            printf("\nEnter data: ");
            scanf("%d", &ele);
            root = insert_front(root, ele);
            display(root);
        }
        if(ch == 2) {
            printf("\nEnter data: ");
            scanf("%d", &ele);
            root = insert_end(root, ele);
            display(root);
        }
        if(ch == 3) {
            printf("\nEnter data to delete: ");
            scanf("%d", &del);
            root = DelList(root, del);
            display(root);
        }
        if(ch == 5) {
            printf("\nEnter data: ");
            scanf("%d", &ele);
            root = insert_sorted(root, ele);
            display(root);
        }
    }
    
    return 0;
}
