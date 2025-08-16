import unittest
from symbol_table import SymbolTable

class SymbolTableTest(unittest.TestCase):
    def setUp(self):
        self.symbol_table = SymbolTable()

    def test_add(self):
        self.assertEqual(self.symbol_table.class_table, {})
        self.assertEqual(self.symbol_table.subroutine_table, {})

        self.symbol_table.add(v_name='x', v_type='int', v_scope='field')
        expected1 = {'x': {'type': 'int', 'scope': 'field', 'index': 0}}
        self.assertEqual(self.symbol_table.class_table, expected1)

        self.symbol_table.add(v_name='y', v_type='int', v_scope='field')
        expected2 = {
            'x': {'type': 'int', 'scope': 'field', 'index': 0},
            'y': {'type': 'int', 'scope': 'field', 'index': 1},
        }
        self.assertEqual(self.symbol_table.class_table, expected2)

        self.symbol_table.add(v_name='pointCount', v_type='int', v_scope='static')
        expected3 = {
            'x': {'type': 'int', 'scope': 'field', 'index': 0},
            'y': {'type': 'int', 'scope': 'field', 'index': 1},
            'pointCount': {'type': 'int', 'scope': 'static', 'index': 0},
        }
        self.assertEqual(self.symbol_table.class_table, expected3)

        self.symbol_table.add(v_name='this', v_type='Point', v_scope='argument')
        expected4 = {
            'this': {'type': 'Point', 'scope': 'argument', 'index': 0}
        }
        self.assertEqual(self.symbol_table.subroutine_table, expected4)

        self.symbol_table.add(v_name='other', v_type='Point', v_scope='argument')
        expected5 = {
            'this': {'type': 'Point', 'scope': 'argument', 'index': 0},
            'other': {'type': 'Point', 'scope': 'argument', 'index': 1}
        }
        self.assertEqual(self.symbol_table.subroutine_table, expected5)

        self.symbol_table.add(v_name='dx', v_type='int', v_scope='local')
        expected6 = {
            'this': {'type': 'Point', 'scope': 'argument', 'index': 0},
            'other': {'type': 'Point', 'scope': 'argument', 'index': 1},
            'dx': {'type': 'int', 'scope': 'local', 'index': 0},
        }
        self.assertEqual(self.symbol_table.subroutine_table, expected6)

        self.symbol_table.add(v_name='dy', v_type='int', v_scope='local')
        expected7 = {
            'this': {'type': 'Point', 'scope': 'argument', 'index': 0},
            'other': {'type': 'Point', 'scope': 'argument', 'index': 1},
            'dx': {'type': 'int', 'scope': 'local', 'index': 0},
            'dy': {'type': 'int', 'scope': 'local', 'index': 1},
        }
        self.assertEqual(self.symbol_table.subroutine_table, expected7)

    def test_start_subroutine(self):
        self.symbol_table.add(v_name='x', v_type='int', v_scope='field')
        self.symbol_table.add(v_name='y', v_type='int', v_scope='field')
        self.symbol_table.add(v_name='pointCount', v_type='int', v_scope='static')
        self.symbol_table.add(v_name='this', v_type='Point', v_scope='argument')
        self.symbol_table.add(v_name='other', v_type='Point', v_scope='argument')
        self.symbol_table.add(v_name='dx', v_type='int', v_scope='local')
        self.symbol_table.add(v_name='dy', v_type='int', v_scope='local')

        expected1 = {
            'x': {'type': 'int', 'scope': 'field', 'index': 0},
            'y': {'type': 'int', 'scope': 'field', 'index': 1},
            'pointCount': {'type': 'int', 'scope': 'static', 'index': 0},
        }

        expected2 = {
            'this': {'type': 'Point', 'scope': 'argument', 'index': 0},
            'other': {'type': 'Point', 'scope': 'argument', 'index': 1},
            'dx': {'type': 'int', 'scope': 'local', 'index': 0},
            'dy': {'type': 'int', 'scope': 'local', 'index': 1},
        }

        self.assertEqual(self.symbol_table.class_table, expected1)
        self.assertEqual(self.symbol_table.subroutine_table, expected2)

        self.symbol_table.start_subroutine()
        self.assertEqual(self.symbol_table.class_table, expected1)
        self.assertEqual(self.symbol_table.subroutine_table, {})
        self.assertEqual(self.symbol_table.count['argument'], 0)
        self.assertEqual(self.symbol_table.count['local'], 0)


if __name__ == '__main__':
    unittest.main()
