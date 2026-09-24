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
#include<errno.h>
#include<limits.h>
#include<ctype.h>
#include<string.h>

typedef struct node {
    int data;
    struct node* next;
} node;

// Creates a new node with given data
// Returns pointer to allocated node
node* create_node(int item) {
    node* temp = (node*)malloc(sizeof(node));
    if (temp == NULL) {
        perror("Allocation failed");
        exit(EXIT_FAILURE);
    }
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

// Inserts in ascending order; the existing list must be sorted.
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

void destroy_list(node* head) {
    while (head != NULL) {
        node* next = head->next;
        free(head);
        head = next;
    }
}

// Retry malformed input; return 0 at EOF rather than reusing stale values.
int read_integer(const char* prompt, int* value) {
    char buffer[128];
    for (;;) {
        fputs(prompt, stdout);
        if (fgets(buffer, sizeof(buffer), stdin) == NULL) return 0;
        if (strchr(buffer, '\n') == NULL && !feof(stdin)) {
            int ch;
            while ((ch = getchar()) != '\n' && ch != EOF) {}
            puts("Invalid input. Please enter a number.");
            continue;
        }
        errno = 0;
        char* end;
        long parsed = strtol(buffer, &end, 10);
        if (end == buffer || errno == ERANGE || parsed < INT_MIN || parsed > INT_MAX) {
            puts("Invalid input. Please enter a number.");
            continue;
        }
        while (isspace((unsigned char)*end)) end++;
        if (*end != '\0') {
            puts("Invalid input. Please enter a number.");
            continue;
        }
        *value = (int)parsed;
        return 1;
    }
}

int main(void) {
    node* root = NULL;
    int choice, item;
    while (read_integer("\nMenu: 1. insert front, 2. insert end, 3. delete, "
                        "5. sorted insert (ascending list required), 4. exit: ", &choice)) {
        if (choice == 4) break;
        if (choice != 1 && choice != 2 && choice != 3 && choice != 5) {
            puts("Invalid option. Please try again.");
            continue;
        }
        if (!read_integer("\nEnter data: ", &item)) break;
        if (choice == 1) root = insert_front(root, item);
        else if (choice == 2) root = insert_end(root, item);
        else if (choice == 3) root = DelList(root, item);
        else root = insert_sorted(root, item);
        display(root);
    }
    destroy_list(root);
    puts("\nGOOD BYE>>>>");
    return 0;
}
