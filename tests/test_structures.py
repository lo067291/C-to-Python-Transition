"""Regression tests for both implementations; Python stdlib + a C11 compiler."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_python(name):
    return runpy.run_path(str(ROOT / "Python-Implementation" / name))


def list_values(linked_list):
    values = []
    current = linked_list.head
    while current is not None:
        values.append(current.data)
        current = current.next
    return values


class PythonStructures(unittest.TestCase):
    def test_stack(self):
        stack = load_python("StackInPython")["Stack"]()
        self.assertTrue(stack.is_empty())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(stack.pop())
            self.assertIsNone(stack.peek())
        for value in (10, -1, 30):
            stack.push(value)
        self.assertEqual(stack.peek(), 30)
        self.assertEqual([stack.pop() for _ in range(3)], [30, -1, 10])
        self.assertTrue(stack.is_empty())

    def test_queue(self):
        queue = load_python("QueueInPython")["Queue"]()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(queue.dequeue())
        for value in (10, -1, 30):
            queue.enqueue(value)
        self.assertEqual([queue.dequeue() for _ in range(3)], [10, -1, 30])
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.rear)
        queue.enqueue(40)
        self.assertEqual(queue.dequeue(), 40)

    def test_hash_table(self):
        table = load_python("HashTableInPython")["HashTable"]()
        self.assertEqual(table._hash("a"), table._hash("k"))
        table.insert("a", 1)
        table.insert("k", 2)
        table.insert("a", 3)
        table.insert("", 4)
        table.insert("long-key-" * 100, 5)
        self.assertEqual(table.get("a"), 3)
        self.assertEqual(table.get("k"), 2)
        self.assertEqual(table.get(""), 4)
        self.assertEqual(table.get("long-key-" * 100), 5)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(table.get("missing"))

    def test_linked_list(self):
        cls = load_python("LinkedListsInPython.py")["LinkedList"]
        linked = cls()
        linked.delete(123)
        linked.insert_end(20)
        linked.insert_front(10)
        linked.insert_end(30)
        self.assertEqual(list_values(linked), [10, 20, 30])
        linked.delete(20)
        linked.delete(10)
        linked.delete(30)
        linked.delete(999)
        self.assertEqual(list_values(linked), [])
        for value in (30, 10, 20, 20, 40):
            linked.insert_sorted(value)
        self.assertEqual(list_values(linked), [10, 20, 20, 30, 40])
        linked.delete(20)
        self.assertEqual(list_values(linked), [10, 20, 30, 40])

    def test_linked_list_menu_and_eof(self):
        path = ROOT / "Python-Implementation/LinkedListsInPython.py"
        for input_text in ("", "abc\n1\nno\n10\n2\n20\n3\n10\n4\n", "1\n"):
            result = subprocess.run([os.sys.executable, str(path)], input=input_text,
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            if input_text.startswith("abc"):
                self.assertIn("Invalid input", result.stdout)
                self.assertIn("10 20", result.stdout)


C_CASES = {
    "StackInC": r'''
        Stack* s = create_stack();
        assert(is_empty(s)); assert(pop(s) == -1); assert(peek(s) == -1);
        push(s, 10); push(s, -1); push(s, 30);
        assert(peek(s) == 30); assert(pop(s) == 30);
        assert(pop(s) == -1); assert(pop(s) == 10); assert(is_empty(s));
        push(s, 50); destroy_stack(s); destroy_stack(NULL);
    ''',
    "QueueInC": r'''
        Queue* q = create_queue();
        assert(is_empty(q)); assert(dequeue(q) == -1);
        enqueue(q, 10); enqueue(q, -1); enqueue(q, 30);
        assert(dequeue(q) == 10); assert(dequeue(q) == -1);
        assert(dequeue(q) == 30); assert(is_empty(q)); assert(q->rear == NULL);
        enqueue(q, 40); assert(dequeue(q) == 40);
        enqueue(q, 50); destroy_queue(q); destroy_queue(NULL);
    ''',
    "HashTableInC": r'''
        HashTable* table = create_table();
        assert(hash("a") == hash("k"));
        char key[] = "a";
        insert(table, key, 1); key[0] = 'z';
        assert(get(table, "a") == 1);
        insert(table, "k", 2); insert(table, "a", 3); insert(table, "", 4);
        assert(get(table, "a") == 3); assert(get(table, "k") == 2);
        assert(get(table, "") == 4); assert(get(table, "missing") == -1);
        char long_key[1001]; memset(long_key, 'x', 1000); long_key[1000] = '\0';
        insert(table, long_key, 5); assert(get(table, long_key) == 5);
        destroy_table(table); destroy_table(NULL);
    ''',
    "LinkedListsInC.c": r'''
        node* head = NULL;
        head = DelList(head, 123);
        head = insert_end(head, 20); head = insert_front(head, 10);
        head = insert_end(head, 30);
        assert(head->data == 10 && head->next->data == 20);
        head = DelList(head, 20); head = DelList(head, 10);
        head = DelList(head, 30); assert(head == NULL);
        int inputs[] = {30, 10, 20, 20, 40};
        int expected[] = {10, 20, 20, 30, 40};
        for (int i = 0; i < 5; i++) head = insert_sorted(head, inputs[i]);
        node* cursor = head;
        for (int i = 0; i < 5; i++) { assert(cursor->data == expected[i]); cursor = cursor->next; }
        assert(cursor == NULL);
        head = DelList(head, 20); head = DelList(head, 999);
        assert(head->next->data == 20 && head->next->next->data == 30);
        destroy_list(head); destroy_list(NULL);
    ''',
}


class CStructures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler = shutil.which(os.environ.get("CC", "gcc"))
        if not cls.compiler:
            raise unittest.SkipTest("C compiler unavailable; install GCC or set CC")
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)

    def compile(self, source, output):
        flags = ["-std=c11", "-Wall", "-Wextra", "-Werror", "-pedantic"]
        if os.environ.get("C_TEST_SANITIZERS") == "1":
            flags += ["-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-g"]
        result = subprocess.run([self.compiler, *flags, "-x", "c", str(source), "-o", str(output)],
                                text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_program(self, path, input_text=""):
        result = subprocess.run([str(path)], input=input_text, text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_operations(self):
        for name, body in C_CASES.items():
            with self.subTest(structure=name):
                source = ROOT / "C-Implementation" / name
                harness = Path(self.temp.name) / (name + "_test.c")
                harness.write_text('#define main demo_main\n#include "' + source.as_posix() +
                                   '"\n#undef main\n#include <assert.h>\nint main(void) {\n' +
                                   body + '\nreturn 0;\n}\n')
                output = harness.with_suffix(".out")
                self.compile(harness, output)
                self.run_program(output)

    def test_demos(self):
        for name in C_CASES:
            with self.subTest(structure=name):
                source = ROOT / "C-Implementation" / name
                output = Path(self.temp.name) / (name + "_demo")
                self.compile(source, output)
                if name == "LinkedListsInC.c":
                    for input_text in ("", "abc\n1\nno\n10\n2\n20\n3\n10\n4\n",
                                       "1\n", "99999999999999999999\n4\n",
                                       "x" * 300 + "\n4\n", "\n4\n"):
                        self.run_program(output, input_text)
                else:
                    self.run_program(output)


if __name__ == "__main__":
    unittest.main()
