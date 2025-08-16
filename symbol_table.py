class SymbolTable(object):
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.count = {'field': 0, 'static': 0, 'argument': 0, 'local': 0}

    def start_subroutine(self)->None:
        """
        start a new subroutine scope
        and resets the subroutine's symbol table
        """
        self.subroutine_table.clear()
        self.count['argument'] = 0
        self.count['local'] = 0


    def add(self, v_name: str, v_type: str, v_scope: str)->None:
        """
        add a new variable to the table
        """
        index = self.var_count(v_scope)
        self.count[v_scope] = index + 1
        if v_scope in {'field', 'static'}:
            if v_scope == 'field':
                v_scope = 'this'
            self.class_table[v_name] = {'type': v_type, 'scope': v_scope, 'index' : index}
        else:
            self.subroutine_table[v_name] = {'type': v_type, 'scope': v_scope, 'index' : index}

    def var_count(self, kind: str)->int:
        """
        returns the number of variables of given kind
        already defined in the current scope
        """
        if kind == 'this':
            kind = 'field'
        return self.count[kind]

    def kind_of(self, name: str)->str or None:
        """
        returns the kind of the named variable in the current scope
        """
        if name in self.class_table:
            return self.class_table[name]['scope']
        elif name in self.subroutine_table:
            return self.subroutine_table[name]['scope']
        return None

    def type_of(self, name: str)->str or None:
        """
        returns the type of the named variable in the current scope
        """
        if name in self.class_table:
            return self.class_table[name]['type']
        elif name in self.subroutine_table:
            return self.subroutine_table[name]['type']
        return None

    def index_of(self, name: str)->int or None:
        """
        returns the index of the named variable in the current scope
        """
        if name in self.class_table:
            return self.class_table[name]['index']
        elif name in self.subroutine_table:
            return self.subroutine_table[name]['index']
        return None