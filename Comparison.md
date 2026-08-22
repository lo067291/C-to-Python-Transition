# C to Python: Detailed Comparison

## Memory Management

**C** requires manual allocation and deallocation for every node:

```c
Node* new_node = (Node*)malloc(sizeof(Node));
// ... use the node ...
free(temp);  // must be called explicitly or memory leaks
```

Forgetting `free()` in any function that removes a node (e.g., `pop()`, 
`dequeue()`, `DelList()`) causes a memory leak - the memory remains 
reserved but inaccessible for the lifetime of the program.

**Python** uses automatic garbage collection. When a node has no more 
references pointing to it, Python reclaims the memory without any 
explicit action:

```python
self.top = self.top.next  # old node is now unreferenced
# Python's garbage collector frees it automatically
```

This is a meaningful tradeoff: C gives precise control over memory 
timing (useful in embedded/real-time systems where you can't afford 
unpredictable GC pauses), while Python trades that control for safety 
and reduced developer burden.

## Struct/Class Definition

**C** defines a node as a struct with an explicit pointer field:

```c
typedef struct Node {
    int data;
    struct Node* next;
} Node;
```

**Python** defines the same concept as a class, using `self` to bind 
attributes to each instance rather than a raw pointer:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

## Function Signatures and Return Values

**C** functions that modify a structure often must return the new head/
root, because C passes pointers by value - the caller's pointer variable 
itself can't be modified by the function:

```c
node* insert_front(node* head, int item) {
    // ...
    return temp;  // caller must reassign: head = insert_front(head, item);
}
```

**Python** methods can modify `self` directly, since `self` is a 
reference to the actual object - no return value is needed to "pass 
back" the update:

```python
def insert_front(self, item):
    new_node = Node(item)
    new_node.next = self.head
    self.head = new_node  # modifies the actual object, no return needed
```

## Hash Table: Manual Implementation vs. Built-in Dict

This repo implements a hash table manually (custom hash function, 
chaining for collision resolution) to demonstrate understanding of how 
hash tables work internally - open addressing vs. chaining, why a good 
hash function distributes keys evenly, and how collisions are resolved.

In real Python code, you would almost always use the built-in `dict` 
instead - it's a highly optimized C-implemented hash table already. 
This manual version exists purely for learning, not as something to 
use in production.

## Complexity Comparison

| Structure | Operation | C | Python (this repo) | Python (built-in) |
|---|---|---|---|---|
| Stack | push/pop | O(1) | O(1) | O(1) (list.append/pop) |
| Queue | enqueue/dequeue | O(1) | O(1) | O(1) (collections.deque) |
| Hash Table | insert/get (avg) | O(1) | O(1) | O(1) (dict) |
| Hash Table | insert/get (worst case) | O(n) | O(n) | O(n), rare in practice |

## Code Verbosity

Roughly, the Python implementations run 20-30% shorter than their C 
equivalents for the same functionality, primarily due to:
- No manual memory management calls
- No explicit type declarations
- Built-in object model reducing struct boilerplate

## When to Use Which

**C** when: performance is critical, memory footprint must be tightly 
controlled, or working in embedded/real-time systems (directly relevant 
to my embedded systems projects - MSP430, TI-RSLK).

**Python** when: development speed matters more than raw performance, 
or working with data/ML pipelines where existing libraries (NumPy, 
Pandas, scikit-learn) already provide optimized implementations of 
these structures.
