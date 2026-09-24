# C to Python: Implementation Comparison

This comparison describes the actual implementations in this repository. The Python linked-list port currently has the issues listed in the [README](README.md); it should not be treated as a fully working equivalent yet.

## Representation and Updates

| Design point | C implementation | Python implementation |
|---|---|---|
| Node | struct containing data and a next pointer | Node instance containing data and a next reference |
| Empty link | NULL | None |
| Linked-list head update | Return the new head and reassign it in the caller | Assign to self.head |
| Stack | Struct with a top pointer | Object with a top attribute |
| Queue | Struct with front and rear pointers | Object with front and rear attributes |
| Hash table | Array of 10 bucket pointers | List of 10 bucket references |

C passes a pointer argument by value. A function can change the pointed-to data, but assigning to its local pointer does not reassign the caller's pointer variable. The linked-list functions therefore return the new head; another C design could use a pointer-to-pointer.

Python methods update attributes on the referenced instance. Rebinding the local self variable would not replace the caller's reference.

## Memory Management

The C implementations allocate nodes with malloc. Stack pop, queue dequeue, and linked-list deletion call free for removed nodes. The hash table duplicates keys with strdup. However, the demos do not provide full cleanup for all remaining allocations, and allocation failures are not checked.

Python implementations remove links to nodes rather than manually freeing memory. Objects become eligible for automatic reclamation once no longer reachable; these examples do not promise a specific reclamation time.

## Linked Lists

The C list supports front insertion, end insertion, first-match deletion, display, and sorted insertion. End insertion traverses the list because no tail pointer is stored.

The C sorted-insertion conditions implement ascending order, assuming the existing list is sorted. Its descending-order comment is inaccurate. Arbitrary front/end insertion can break that precondition.

The Python port attempts the same operations but has:
- an entry-point indentation problem;
- a selfself/self mismatch and missing new_node in insert_end;
- inconsistent sorted-insertion comparisons.

## Stacks and Queues

Both stacks insert and remove at the head, giving last-in, first-out behavior.

Both queues retain front and rear references, allowing enqueue at the rear and dequeue at the front without traversing the queue. Removing the final node clears both references.

Empty pop/dequeue/peek operations print a message. C returns -1, while Python returns None. Neither implementation uses exceptions or a separate success flag.

## Hash Tables

Both versions use a polynomial-style string hash with multiplier 31, a fixed 10-bucket array/list, and linked-list collision chains.

Insertion prepends an entry without searching for an existing key. Inserting the same key again therefore creates a duplicate; get returns the newest matching entry. There is no deletion or resizing operation.

C accumulates the hash in an unsigned int; Python's accumulator uses arbitrary-precision integers. Because their overflow behavior differs, identical bucket placement across languages is not guaranteed for long keys.

## Complexity of These Implementations

Let n be the number of stored nodes and b be the length of the selected hash bucket. Hash-table entries below describe structural work after hashing, excluding variable-length key copying/comparison and Python integer-arithmetic costs.

| Structure | Operation | Structural work |
|---|---|---|
| Linked list | Insert at front | O(1) |
| Linked list | Insert at end, sorted insertion, deletion, display | O(n) |
| Stack | push, pop, peek, is_empty | O(1) |
| Queue | enqueue, dequeue, is_empty | O(1) |
| Hash table | Prepend an entry | O(1) after hashing/allocation/key copying |
| Hash table | get | O(b) entry visits after hashing |

Both hash implementations must scan the key to compute its hash. C also copies each inserted key. String comparisons during lookup add costs depending on key length.

With a fixed 10 buckets, chain lengths grow as more entries are added. Expected constant-time lookup should not be claimed as n grows without controlling load factor. Worst-case lookup visits all n entries.

## Cross-Language Tradeoffs

C exposes pointer manipulation, ownership, allocation, and explicit cleanup. Python expresses the same linked structure through objects and references with less manual memory-management work.

Neither language removes the algorithm's traversal cost: a tail-less linked list still requires a traversal for end insertion, and a long hash chain still requires sequential searching.

These implementations are learning exercises. Their educational value comes from making those mechanics visible; the repository does not include a measured speed, memory, or code-size benchmark.
