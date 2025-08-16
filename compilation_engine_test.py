import unittest
from compilation_engine import CompilationEngine

class CompilationEngineTest(unittest.TestCase):

    def test_compile_class_variable_declaration(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'this', 'type': 'int', 'index': 0}
        }

        self.assertEqual(ce.symbol_table.class_table, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'this', 'type': 'int', 'index': 0},
            'count': {'scope': 'static', 'type': 'int', 'index': 0},
        }

        self.assertEqual(ce.symbol_table.class_table, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'this', 'type': 'int', 'index': 0},
            'y': {'scope': 'this', 'type': 'int', 'index': 1},
            'count': {'scope': 'static', 'type': 'int', 'index': 0},
        }

        self.assertEqual(ce.symbol_table.class_table, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (',', 'symbol'),
            ('sCount', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('boolean', 'keyword'),
            ('is', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'this', 'type': 'int', 'index': 0},
            'y': {'scope': 'this', 'type': 'int', 'index': 1},
            'z': {'scope': 'this', 'type': 'int', 'index': 2},
            'count': {'scope': 'static', 'type': 'int', 'index': 0},
            'sCount': {'scope': 'static', 'type': 'int', 'index': 1},
            'is': {'scope': 'static', 'type': 'boolean', 'index': 2},
        }

        self.assertEqual(ce.symbol_table.class_table, expected)

    def test_compile_subroutine_argument_dec(self):
        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (',', 'symbol'),
            ('sCount', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('boolean', 'keyword'),
            ('is', 'identifier'),
            (';', 'symbol'),
            ('constructor', 'keyword'),
            ('Point', 'identifier'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {}

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (',', 'symbol'),
            ('sCount', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('boolean', 'keyword'),
            ('is', 'identifier'),
            (';', 'symbol'),
            ('constructor', 'keyword'),
            ('Point', 'identifier'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('ax', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('ay', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('az', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'ax': {'scope': 'argument', 'type': 'int', 'index': 0},
            'ay': {'scope': 'argument', 'type': 'int', 'index': 1},
            'az': {'scope': 'argument', 'type': 'int', 'index': 2},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('method', 'keyword'),
            ('void', 'keyword'),
            ('draw', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'this': {'scope': 'argument', 'type': 'Point', 'index': 0},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('method', 'keyword'),
            ('int', 'keyword'),
            ('distance', 'identifier'),
            ('(', 'symbol'),
            ('Point', 'identifier'),
            ('other', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'this': {'scope': 'argument', 'type': 'Point', 'index': 0},
            'other': {'scope': 'argument', 'type': 'Point', 'index': 1},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('method', 'keyword'),
            ('int', 'keyword'),
            ('distance', 'identifier'),
            ('(', 'symbol'),
            ('Point', 'identifier'),
            ('other', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('eps', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'this': {'scope': 'argument', 'type': 'Point', 'index': 0},
            'other': {'scope': 'argument', 'type': 'Point', 'index': 1},
            'eps': {'scope': 'argument', 'type': 'int', 'index': 2},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('method', 'keyword'),
            ('int', 'keyword'),
            ('distance', 'identifier'),
            ('(', 'symbol'),
            ('Point', 'identifier'),
            ('other', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('eps', 'identifier'),
            (',', 'symbol'),
            ('boolean', 'keyword'),
            ('start', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'this': {'scope': 'argument', 'type': 'Point', 'index': 0},
            'other': {'scope': 'argument', 'type': 'Point', 'index': 1},
            'eps': {'scope': 'argument', 'type': 'int', 'index': 2},
            'start': {'scope': 'argument', 'type': 'boolean', 'index': 3},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('square', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {}

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('square', 'identifier'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'argument', 'type': 'int', 'index': 0},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

    def test_compile_subroutine_variable_dec(self):
        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('square', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {}

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('square', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'local', 'type': 'int', 'index': 0}
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('square', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('boolean', 'keyword'),
            ('finished', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = {
            'x': {'scope': 'local', 'type': 'int', 'index': 0},
            'y': {'scope': 'local', 'type': 'int', 'index': 1},
            'z': {'scope': 'local', 'type': 'int', 'index': 2},
            'finished': {'scope': 'local', 'type': 'boolean', 'index': 3},
        }

        self.assertEqual(ce.symbol_table.subroutine_table, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('count', 'identifier'),
            (',', 'symbol'),
            ('sCount', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('boolean', 'keyword'),
            ('is', 'identifier'),
            (';', 'symbol'),
            ('method', 'keyword'),
            ('int', 'keyword'),
            ('dist', 'identifier'),
            ('(', 'symbol'),
            ('char', 'keyword'),
            ('c', 'keyword'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('a', 'keyword'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (',', 'symbol'),
            ('z', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('boolean', 'keyword'),
            ('finished', 'identifier'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected_class = {
            'x': {'scope': 'this', 'type': 'int', 'index': 0},
            'y': {'scope': 'this', 'type': 'int', 'index': 1},
            'z': {'scope': 'this', 'type': 'int', 'index': 2},
            'count': {'scope': 'static', 'type': 'int', 'index': 0},
            'sCount': {'scope': 'static', 'type': 'int', 'index': 1},
            'is': {'scope': 'static', 'type': 'boolean', 'index': 2},
        }

        expected_subroutine = {
            'this': {'scope': 'argument', 'type': 'Point', 'index': 0},
            'c': {'scope': 'argument', 'type': 'char', 'index': 1},
            'a': {'scope': 'argument', 'type': 'int', 'index': 2},
            'x': {'scope': 'local', 'type': 'int', 'index': 0},
            'y': {'scope': 'local', 'type': 'int', 'index': 1},
            'z': {'scope': 'local', 'type': 'int', 'index': 2},
            'finished': {'scope': 'local', 'type': 'boolean', 'index': 3},
        }

        self.assertEqual(ce.symbol_table.class_table, expected_class)
        self.assertEqual(ce.symbol_table.subroutine_table, expected_subroutine)

    def test_expression(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('1', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printChar', 'identifier'),
            ('(', 'symbol'),
            ('s', 'stringConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            f'push constant {ord('s')}',
            'call Output.printChar 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0'
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printString', 'identifier'),
            ('(', 'symbol'),
            ('Hello, World!', 'stringConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            f'push constant 13',
            'call String.new 1',
            f'push constant {ord('H')}',
            'call String.appendChar 2',
            f'push constant {ord('e')}',
            'call String.appendChar 2',
            f'push constant {ord('l')}',
            'call String.appendChar 2',
            f'push constant {ord('l')}',
            'call String.appendChar 2',
            f'push constant {ord('o')}',
            'call String.appendChar 2',
            f'push constant {ord(',')}',
            'call String.appendChar 2',
            f'push constant {ord(' ')}',
            'call String.appendChar 2',
            f'push constant {ord('W')}',
            'call String.appendChar 2',
            f'push constant {ord('o')}',
            'call String.appendChar 2',
            f'push constant {ord('r')}',
            'call String.appendChar 2',
            f'push constant {ord('l')}',
            'call String.appendChar 2',
            f'push constant {ord('d')}',
            'call String.appendChar 2',
            f'push constant {ord('!')}',
            'call String.appendChar 2',
            'call Output.printString 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0'
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('boolean', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('true', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'push constant 1',
            'neg',
            'return',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('boolean', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('false', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('-', 'symbol'),
            ('143', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'push constant 143',
            'neg',
            'return',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('1', 'integerConstant'),
            ('+', 'symbol'),
            ('(', 'symbol'),
            ('2', 'integerConstant'),
            ('*', 'symbol'),
            ('3', 'integerConstant'),
            (')', 'symbol'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'push constant 1',
            'push constant 2',
            'push constant 3',
            'call Math.multiply 2',
            'add',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0'
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('d', 'identifier'),
            (';', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('d', 'identifier'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 1',
            'push constant 0',
            'pop local 0',
            'push local 0',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('3', 'integerConstant'),
            (']', 'symbol'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 1',
            'push constant 0',
            'pop local 0',
            'push local 0',
            'push constant 3',
            'add',
            'pop pointer 1',
            'push that 0',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('3', 'integerConstant'),
            (']', 'symbol'),
            ('+', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('4', 'integerConstant'),
            (']', 'symbol'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 1',
            'push constant 0',
            'pop local 0',
            'push local 0',
            'push constant 3',
            'add',
            'pop pointer 1',
            'push that 0',
            'push local 0',
            'push constant 4',
            'add',
            'pop pointer 1',
            'push that 0',
            'add',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('3', 'integerConstant'),
            (']', 'symbol'),
            ('+', 'symbol'),
            ('(', 'symbol'),
            ('4', 'integerConstant'),
            ('*', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 1',
            'push constant 0',
            'pop local 0',
            'push local 0',
            'push constant 3',
            'add',
            'pop pointer 1',
            'push that 0',
            'push constant 4',
            'push constant 5',
            'call Math.multiply 2',
            'add',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('(', 'symbol'),
            ('4', 'integerConstant'),
            ('*', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'push constant 4',
            'push constant 5',
            'call Math.multiply 2',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return',
            'pop temp 0',
        ]
        self.assertEqual(ce.output, expected)

    def test_compile_let(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('5', 'integerConstant'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 5',
                    'pop local 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('5', 'integerConstant'),
            ('*', 'symbol'),
            ('10', 'integerConstant'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 5',
                    'push constant 10',
                    'call Math.multiply 2',
                    'pop local 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('boolean', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('true', 'keyword'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 1',
                    'neg',
                    'pop local 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('boolean', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('false', 'keyword'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('char', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('m', 'stringConstant'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 109',
                    'pop local 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 2',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'pop local 1',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'pop local 1',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('x', 'identifier'),
            ('+', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 2',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'pop local 1',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 1',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'add',
                    'pop local 1',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('+', 'symbol'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 2',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'pop local 1',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'push local 1',
                    'add',
                    'pop local 1',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('5', 'integerConstant'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push constant 5',
                    'pop that 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('var', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('x', 'identifier'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 2',
                    'push constant 0',
                    'pop local 0',
                    'push constant 0',
                    'pop local 1',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push local 1',
                    'pop that 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('3', 'integerConstant'),
            (']', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'add',
                    'push local 0',
                    'push constant 3',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'pop temp 0',
                    'pop pointer 1',
                    'push temp 0',
                    'pop that 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('var', 'keyword'),
            ('Array', 'keyword'),
            ('arr', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('=', 'symbol'),
            ('Array', 'identifier'),
            ('.', 'symbol'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            ('*', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('arr', 'identifier'),
            ('[', 'symbol'),
            ('1', 'integerConstant'),
            ('+', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 1',
                    'push constant 0',
                    'pop local 0',
                    'push constant 5',
                    'call Array.new 1',
                    'pop local 0',
                    'push local 0',
                    'push constant 2',
                    'push constant 2',
                    'call Math.multiply 2',
                    'add',
                    'push local 0',
                    'push constant 1',
                    'push constant 2',
                    'add',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'pop temp 0',
                    'pop pointer 1',
                    'push temp 0',
                    'pop that 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

    def test_compile_return(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('test', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('5', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.test 0',
                    'push constant 5',
                    'return']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('test', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.test 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Foo', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('bar', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('-', 'symbol'),
            ('152', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Foo.bar 0',
            'push constant 152',
            'neg',
            'return',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Foo', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('boolean', 'keyword'),
            ('bar', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('true', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Foo.bar 0',
            'push constant 1',
            'neg',
            'return',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Foo', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('char', 'keyword'),
            ('bar', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('s', 'stringConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]
        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Foo.bar 0',
            f'push constant {ord('s')}',
            'return',
        ]
        self.assertEqual(ce.output, expected)

    def test_compile_do(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('void', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'),
            ('Output', 'identifier'),
            ('.', 'symbol'),
            ('printInt', 'identifier'),
            ('(', 'symbol'),
            ('5', 'integerConstant'),
            (')', 'symbol'),
            (';', 'symbol'),
            ('return', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 0',
                    'push constant 5',
                    'call Output.printInt 1',
                    'pop temp 0',
                    'push constant 0',
                    'return',
                    'pop temp 0']

        self.assertEqual(ce.output, expected)

    def test_compile_if(self):
        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('if', 'keyword'),
            ('(', 'symbol'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('1', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('else', 'keyword'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('0', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 0',
                    'push argument 0',
                    'push argument 1',
                    'eq',
                    'not',
                    'if-goto IF_FALSE0',
                    'push constant 1',
                    'return',
                    'goto IF_TRUE1',
                    'label IF_FALSE0',
                    'push constant 0',
                    'return',
                    'label IF_TRUE1']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            ('Array', 'identifier'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('if', 'keyword'),
            ('(', 'symbol'),
            ('x', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('1', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('else', 'keyword'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('0', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 0',
                    'push argument 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'push argument 1',
                    'eq',
                    'not',
                    'if-goto IF_FALSE0',
                    'push constant 1',
                    'return',
                    'goto IF_TRUE1',
                    'label IF_FALSE0',
                    'push constant 0',
                    'return',
                    'label IF_TRUE1']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('Array', 'identifier'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('if', 'keyword'),
            ('(', 'symbol'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('y', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('1', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('else', 'keyword'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('0', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 0',
                    'push argument 0',
                    'push argument 1',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'eq',
                    'not',
                    'if-goto IF_FALSE0',
                    'push constant 1',
                    'return',
                    'goto IF_TRUE1',
                    'label IF_FALSE0',
                    'push constant 0',
                    'return',
                    'label IF_TRUE1']

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Main', 'identifier'),
            ('{', 'symbol'),
            ('function', 'keyword'),
            ('int', 'keyword'),
            ('main', 'identifier'),
            ('(', 'symbol'),
            ('Array', 'identifier'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('Array', 'identifier'),
            ('y', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('if', 'keyword'),
            ('(', 'symbol'),
            ('x', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            ('=', 'symbol'),
            ('y', 'identifier'),
            ('[', 'symbol'),
            ('2', 'integerConstant'),
            (']', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('1', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('else', 'keyword'),
            ('{', 'symbol'),
            ('return', 'keyword'),
            ('0', 'integerConstant'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = ['function Main.main 0',
                    'push argument 0',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'push argument 1',
                    'push constant 2',
                    'add',
                    'pop pointer 1',
                    'push that 0',
                    'eq',
                    'not',
                    'if-goto IF_FALSE0',
                    'push constant 1',
                    'return',
                    'goto IF_TRUE1',
                    'label IF_FALSE0',
                    'push constant 0',
                    'return',
                    'label IF_TRUE1']

        self.assertEqual(ce.output, expected)

    def test_compile_while(self):
        t = [
            ('class', 'keyword'), ('Main', 'identifier'), ('{', 'symbol'),
            ('function', 'keyword'), ('void', 'keyword'), ('main', 'identifier'),
            ('(', 'symbol'), (')', 'symbol'), ('{', 'symbol'),
            ('while', 'keyword'), ('(', 'symbol'), ('true', 'keyword'), (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'), ('Output', 'identifier'), ('.', 'symbol'),
            ('printInt', 'identifier'), ('(', 'symbol'), ('1', 'integerConstant'),
            (')', 'symbol'), (';', 'symbol'),
            ('}', 'symbol'),
            ('return', 'keyword'), (';', 'symbol'),
            ('}', 'symbol'), ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'label TRUE0',
            'push constant 1', 'neg',  # true
            'not',
            'if-goto FALSE1',
            'push constant 1',
            'call Output.printInt 1',
            'pop temp 0',
            'goto TRUE0',
            'label FALSE1',
            'push constant 0',
            'return',
            'pop temp 0'
        ]

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'), ('Main', 'identifier'), ('{', 'symbol'),
            ('function', 'keyword'), ('void', 'keyword'), ('main', 'identifier'),
            ('(', 'symbol'), (')', 'symbol'), ('{', 'symbol'),
            ('while', 'keyword'), ('(', 'symbol'), ('false', 'keyword'), (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'), ('Output', 'identifier'), ('.', 'symbol'),
            ('printInt', 'identifier'), ('(', 'symbol'), ('1', 'integerConstant'),
            (')', 'symbol'), (';', 'symbol'),
            ('}', 'symbol'),
            ('return', 'keyword'), (';', 'symbol'),
            ('}', 'symbol'), ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 0',
            'label TRUE0',
            'push constant 0',
            'not',
            'if-goto FALSE1',
            'push constant 1',
            'call Output.printInt 1',
            'pop temp 0',
            'goto TRUE0',
            'label FALSE1',
            'push constant 0',
            'return',
            'pop temp 0'
        ]

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'), ('Main', 'identifier'), ('{', 'symbol'),
            ('function', 'keyword'), ('void', 'keyword'), ('main', 'identifier'),
            ('(', 'symbol'), (')', 'symbol'), ('{', 'symbol'),
            ('var', 'keyword'), ('int', 'keyword'), ('i', 'identifier'), (';', 'symbol'),
            ('let', 'keyword'), ('i', 'identifier'), ('=', 'symbol'),
            ('0', 'integerConstant'), (';', 'symbol'),
            ('while', 'keyword'), ('(', 'symbol'),
            ('i', 'identifier'), ('<', 'symbol'), ('10', 'integerConstant'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('let', 'keyword'), ('i', 'identifier'), ('=', 'symbol'),
            ('i', 'identifier'), ('+', 'symbol'), ('1', 'integerConstant'), (';', 'symbol'),
            ('}', 'symbol'),
            ('return', 'keyword'), (';', 'symbol'),
            ('}', 'symbol'), ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 1',
            'push constant 0',
            'pop local 0',
            'push constant 0',
            'pop local 0',
            'label TRUE0',
            'push local 0',
            'push constant 10',
            'lt',
            'not',
            'if-goto FALSE1',
            'push local 0',
            'push constant 1',
            'add',
            'pop local 0',
            'goto TRUE0',
            'label FALSE1',
            'push constant 0',
            'return',
            'pop temp 0'
        ]

        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'), ('Main', 'identifier'), ('{', 'symbol'),
            ('function', 'keyword'), ('void', 'keyword'), ('main', 'identifier'),
            ('(', 'symbol'), (')', 'symbol'), ('{', 'symbol'),
            ('var', 'keyword'), ('Array', 'identifier'), ('arr', 'identifier'), (';', 'symbol'),
            ('var', 'keyword'), ('int', 'identifier'), ('i', 'identifier'), (';', 'symbol'),
            ('var', 'keyword'), ('int', 'identifier'), ('j', 'identifier'), (';', 'symbol'),
            ('while', 'keyword'), ('(', 'symbol'),
            ('arr', 'identifier'), ('[', 'symbol'), ('i', 'identifier'), (']', 'symbol'),
            ('<', 'symbol'),
            ('arr', 'identifier'), ('[', 'symbol'), ('j', 'identifier'), (']', 'symbol'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('do', 'keyword'), ('Output', 'identifier'), ('.', 'symbol'),
            ('printInt', 'identifier'), ('(', 'symbol'), ('0', 'integerConstant'),
            (')', 'symbol'), (';', 'symbol'),
            ('}', 'symbol'),
            ('return', 'keyword'), (';', 'symbol'),
            ('}', 'symbol'), ('}', 'symbol')
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'function Main.main 3',
            'push constant 0',
            'pop local 0',
            'push constant 0',
            'pop local 1',
            'push constant 0',
            'pop local 2',
            'label TRUE0',
            'push local 0',
            'push local 1',
            'add',
            'pop pointer 1',
            'push that 0',
            'push local 0',
            'push local 2',
            'add',
            'pop pointer 1',
            'push that 0',
            'lt',
            'not',
            'if-goto FALSE1',
            'push constant 0',
            'call Output.printInt 1',
            'pop temp 0',
            'goto TRUE0',
            'label FALSE1',
            'push constant 0',
            'return',
            'pop temp 0'
        ]

        self.assertEqual(ce.output, expected)

    def test_compile_constructor(self):
        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (';', 'symbol'),
            ('constructor', 'keyword'),
            ('Point', 'identifier'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('ax', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('ay', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('ax', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('y', 'identifier'),
            ('=', 'symbol'),
            ('ay', 'identifier'),
            (';', 'symbol'),
            ('return', 'keyword'),
            ('this', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'push constant 0',
            'pop this 0',
            'push constant 0',
            'pop this 1',
            'function Point.new 0',
            'push constant 2',
            'call Memory.alloc 1',
            'pop pointer 0',
            'push argument 0',
            'pop this 0',
            'push argument 1',
            'pop this 1',
            'push pointer 0',
            'return',
        ]
        self.assertEqual(ce.output, expected)

        t = [
            ('class', 'keyword'),
            ('Point', 'identifier'),
            ('{', 'symbol'),
            ('field', 'keyword'),
            ('int', 'keyword'),
            ('x', 'identifier'),
            (',', 'symbol'),
            ('y', 'identifier'),
            (';', 'symbol'),
            ('static', 'keyword'),
            ('int', 'keyword'),
            ('pointCount', 'identifier'),
            (';', 'symbol'),
            ('constructor', 'keyword'),
            ('Point', 'identifier'),
            ('new', 'keyword'),
            ('(', 'symbol'),
            ('int', 'keyword'),
            ('ax', 'identifier'),
            (',', 'symbol'),
            ('int', 'keyword'),
            ('ay', 'identifier'),
            (')', 'symbol'),
            ('{', 'symbol'),
            ('let', 'keyword'),
            ('x', 'identifier'),
            ('=', 'symbol'),
            ('ax', 'identifier'),
            (';', 'symbol'),
            ('let', 'keyword'),
            ('y', 'identifier'),
            ('=', 'symbol'),
            ('ay', 'identifier'),
            (';', 'symbol'),
            ('return', 'keyword'),
            ('this', 'keyword'),
            (';', 'symbol'),
            ('}', 'symbol'),
            ('}', 'symbol'),
        ]

        ce = CompilationEngine(t)
        ce.compile_class()

        expected = [
            'push constant 0',
            'pop this 0',
            'push constant 0',
            'pop this 1',
            'push constant 0',
            'pop static 0',
            'function Point.new 0',
            'push constant 2',
            'call Memory.alloc 1',
            'pop pointer 0',
            'push argument 0',
            'pop this 0',
            'push argument 1',
            'pop this 1',
            'push pointer 0',
            'return',
        ]
        self.assertEqual(ce.output, expected)

if __name__ == '__main__':
    unittest.main()
