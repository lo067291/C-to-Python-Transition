# C to Python: Data Structures

Side-by-side implementations of four fundamental data structures, exploring how C pointers and structs translate into Python classes and object references.

The project focuses on **memory management, linked structures, algorithmic complexity, and cross-language design**. Both hash tables are implemented manually with separate chaining.

## Implementations

| Structure | C source | Python source | Current behavior |
|---|---|---|---|
| Singly linked list | [LinkedListsInC.c](C-Implementation/LinkedListsInC.c) | [LinkedListsInPython.py](Python-Implementation/LinkedListsInPython.py) | Interactive insertion/deletion menu; ascending sorted insertion |
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

Both linked-list menus accept integer input, retry invalid entries, and exit cleanly at end-of-input.

## Compile and Run the C Demos

The following commands were checked with GCC on Linux. All four implementations compile as standard C11; the hash table uses malloc and strcpy to copy keys.

```bash
mkdir -p build
gcc -std=c11 -Wall -Wextra -x c C-Implementation/StackInC -o build/stack
gcc -std=c11 -Wall -Wextra -x c C-Implementation/QueueInC -o build/queue
gcc -std=c11 -Wall -Wextra -x c C-Implementation/HashTableInC -o build/hash_table
gcc -std=c11 -Wall -Wextra C-Implementation/LinkedListsInC.c -o build/linked_list

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

## Verification

Run the regression suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The suite uses the Python standard library and GCC (or a compiler selected with the CC environment variable). If no compiler is available, C tests are explicitly skipped.

Seven test methods cover Python operations and menu input, plus compiled C operation harnesses and demos. Cases include:

- Stack LIFO and queue FIFO order, empty operations, and queue reuse after draining.
- Hash collisions, duplicate-key lookup, empty/long string keys, and missing keys.
- Linked-list front/end insertion, ascending sorted insertion with duplicates, and deletion.
- Invalid menu input and end-of-input handling.
- C cleanup of populated and empty structures.

C tests compile with C11, strict warnings, and warnings treated as errors. The suite passed normally and with AddressSanitizer/UndefinedBehaviorSanitizer enabled. LeakSanitizer could not run in the review environment because of its ptrace restriction; leak detection was disabled for the successful sanitizer run.

On a compatible local system, enable sanitizer checks with:

```bash
C_TEST_SANITIZERS=1 python -m unittest discover -s tests -v
```

## Implementation Notes

- Both sorted-insertion methods expect an already ascending list. Arbitrary front/end insertion can break that precondition.
- C allocation failures are checked and terminate the demo with an error. Each demo releases its remaining nodes and container on normal exit.
- Hash tables have 10 fixed buckets and no resizing. Repeated insertion of a key adds another entry; lookup returns the newest matching value.
- C error returns use -1, which is also a possible stored value; Python uses None.
- C and Python numeric types and hash-overflow behavior differ; the examples are not a cross-language binary-compatibility specification.

## Author

**Logan Stacy**  
Computer Engineering at UCF · Accelerated BS/MS  
CompTIA Security+ · CompTIA Network+

[LinkedIn](https://www.linkedin.com/in/logan-stacy) · [GitHub](https://github.com/lo067291) · [Student email](mailto:lo067291@ucf.edu)
