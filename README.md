# C to Python: Data Structures

Side-by-side implementations of four fundamental data structures, exploring how C pointers and structs translate into Python classes and object references.

The project focuses on **memory management, linked structures, algorithmic complexity, and cross-language design**. Both hash tables are implemented manually with separate chaining.

## Implementations

| Structure | C source | Python source | Current behavior |
|---|---|---|---|
| Singly linked list | [LinkedListsInC.c](C-Implementation/LinkedListsInC.c) | [LinkedListsInPython.py](Python-Implementation/LinkedListsInPython.py) | Interactive insertion/deletion menu; Python port has known issues below |
| Stack | [StackInC](C-Implementation/StackInC) | [StackInPython](Python-Implementation/StackInPython) | Linked-node LIFO with push, pop, peek, and empty check |
| Queue | [QueueInC](C-Implementation/QueueInC) | [QueueInPython](Python-Implementation/QueueInPython) | Linked-node FIFO with front/rear references |
| Hash table | [HashTableInC](C-Implementation/HashTableInC) | [HashTableInPython](Python-Implementation/HashTableInPython) | String keys, 10 buckets, separate chaining |

Read the [detailed C/Python comparison](Comparison.md) for implementation-specific tradeoffs and complexity.

## What This Project Demonstrates

- Translating structs and pointer links into classes and object references.
- Updating a C list head through return values versus updating a Python object's head attribute.
- Freeing removed nodes explicitly in C versus releasing references in Python.
- Preserving stack and queue operation order across languages.
- Implementing a string hash and resolving collisions through linked bucket chains.

## Run the Python Demos

Python 3 is required; no third-party packages are used. From the repository root:

```bash
python Python-Implementation/StackInPython
python Python-Implementation/QueueInPython
python Python-Implementation/HashTableInPython
```

These files do not currently have .py extensions, but Python can execute them by filename.

The linked-list entry point is:

```bash
python Python-Implementation/LinkedListsInPython.py
```

It currently raises a NameError at startup; see Known Issues before using it.

## Compile and Run the C Demos

The following commands were checked with GCC on Linux. The GNU C11 setting provides the strdup declaration used by the hash-table implementation.

```bash
mkdir -p build
gcc -std=gnu11 -Wall -Wextra -x c C-Implementation/StackInC -o build/stack
gcc -std=gnu11 -Wall -Wextra -x c C-Implementation/QueueInC -o build/queue
gcc -std=gnu11 -Wall -Wextra -x c C-Implementation/HashTableInC -o build/hash_table
gcc -std=gnu11 -Wall -Wextra C-Implementation/LinkedListsInC.c -o build/linked_list

./build/stack
./build/queue
./build/hash_table
./build/linked_list
```

The `-x c` option identifies the extensionless C files as C source. The commands above use a Unix-style shell.

## Example Outputs

| Demo | Expected sequence |
|---|---|
| Stack | Top: 30; Popped: 30; Popped: 20; not empty |
| Queue | Dequeued: 10; Dequeued: 20; not empty |
| Hash table | apple: 5; banana: 12; cherry: 8 |

The C empty check prints 0 and Python prints False in these examples. The linked-list menu supports front insertion, end insertion, deletion, sorted insertion, and exit.

## Verification and Known Issues

A basic execution check compiled all four C programs and ran their demos. The C linked-list check covered front insertion, end insertion, deletion, and exit. The Python stack, queue, and hash-table demos also ran successfully. These checks are not exhaustive correctness or memory-safety tests.

The current Python linked-list port needs corrections:

- Its main guard is inside the class body and invokes main before LinkedList has finished being defined, causing the startup NameError.
- insert_end declares `selfself` but refers to `self`, and its non-empty branch uses an undefined `new_node`.
- Sorted insertion uses inconsistent comparison directions. The C implementation inserts in ascending order despite a comment that says descending.

Other current limitations:

- The C demos do not check allocation failure or fully free remaining structures on exit.
- The C hash table relies on strdup, so compiler/platform requirements matter.
- Hash tables have fixed capacity and no resizing. Repeated insertion of a key adds another entry; lookup returns the newest matching value.
- C error returns use -1, which is also a possible stored value; Python uses None.

The source implementations are preserved in this documentation update.

## Author

**Logan Stacy**  
Computer Engineering at UCF · Accelerated BS/MS  
CompTIA Security+ · CompTIA Network+

[LinkedIn](https://www.linkedin.com/in/logan-stacy) · [GitHub](https://github.com/lo067291) · [Student email](mailto:lo067291@ucf.edu)
