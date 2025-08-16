from symbol_table import SymbolTable
from vm_writer import VMWriter

class CompilationEngine(object):
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens: list[tuple[str, str]] = tokens
        self.class_name = self.tokens[1][0]
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter()
        self.current_subroutine_name = ''
        self.output: list[str] = self.vm_writer.output
        self.current = 0
        self.counter = 0

    def get_counter(self):
        self.counter += 1
        return self.counter - 1

    def has_more_token(self):
        return self.current < len(self.tokens)

    def peek(self, n=0):
        if self.current + n >= len(self.tokens):
            return None
        return self.tokens[self.current + n]

    def advance(self)->None:
        self.current += 1

    def get_current_token(self):
        if self.has_more_token():
            return self.peek()[0]
        return None

    def get_current_token_and_advance(self):
        if self.has_more_token():
            token = self.peek()[0]
            self.advance()
            return token
        return None

    def expect(self, expected_token=None, expected_type=None):
        token, token_type = self.peek()

        if expected_token and token != expected_token:
            # print(self.peek(1))
            raise ValueError(f"Expected token '{expected_token}', got '{token}'")
        if expected_type and token_type != expected_type:
            raise ValueError(f"Expected type '{expected_type}', got '{token_type}'")

        self.advance()

    def compile_class(self):
        """ Compile a complete class """
        self.expect(expected_token='class', expected_type='keyword')
        self.expect(expected_type='identifier')
        self.expect(expected_token='{', expected_type='symbol')

        self.symbol_table = SymbolTable()
        while self.get_current_token() in {'static', 'field'}:
            self.compile_class_variable_declarations()

        while self.get_current_token() in {'constructor', 'method', 'function'}:
            self.compile_class_subroutine()

    def compile_class_variable_declarations(self):
        """
        compile the variable defined in the class level to hack assembly code
        and append the code to self.output
        """
        v_scope = self.get_current_token_and_advance()
        v_type = self.get_current_token_and_advance()
        v_name = self.get_current_token_and_advance()
        self.symbol_table.add(v_name, v_type, v_scope)
        self.pop_null_to_var_dec_with_name(v_name)
        while self.get_current_token() == ',':
            self.advance()
            v_name = self.get_current_token_and_advance()
            self.symbol_table.add(v_name, v_type, v_scope)
            self.pop_null_to_var_dec_with_name(v_name)
        self.advance()

    def pop_null_to_var_dec_with_name(self, v_name):
        self.vm_writer.write_push('constant', 0)
        self.vm_writer.write_pop(self.symbol_table.kind_of(v_name),
                                 self.symbol_table.index_of(v_name))

    def compile_class_subroutine(self):
        subroutine_kind = self.peek(0)[0]
        subroutine_type = self.peek(1)[0]
        subroutine_name = self.peek(2)[0]
        self.compile_parameter_list()

        self.compile_subroutine_variable_declarations()

        local_var_count = self.symbol_table.var_count('local')
        self.vm_writer.write_function(f'{self.class_name}.{subroutine_name}', local_var_count)

        for var_index in range(self.symbol_table.count['local']):
            self.pop_null_to_var_dec_with_kind_and_index('local', var_index)

        if subroutine_kind == 'constructor':
            num_of_field_variables = self.symbol_table.var_count('this')
            self.vm_writer.write_push('constant', num_of_field_variables)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)
        elif subroutine_kind == 'method':
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)

        self.compile_subroutine_statements()

        self.expect(expected_token='}', expected_type='symbol')

        if subroutine_type == 'void':
            self.vm_writer.write_pop('temp', 0)

    def pop_null_to_var_dec_with_kind_and_index(self, kind, index):
        self.vm_writer.write_push('constant', 0)
        self.vm_writer.write_pop(kind, index)

    def compile_parameter_list(self):
        finished = False
        self.symbol_table.start_subroutine()

        subroutine_kind = self.get_current_token()

        self.expect(expected_token=subroutine_kind) # method, function, constructor
        self.advance() # void, int, ...
        if subroutine_kind == 'constructor':
            self.current_subroutine_name = 'new'
            self.expect(expected_token='new', expected_type='keyword') # new
        else:
            self.current_subroutine_name = self.get_current_token()
            self.expect(expected_type='identifier')  # draw, print, main ...
        self.expect(expected_token='(')

        v_scope = 'argument'
        if subroutine_kind == 'method':
            self.symbol_table.add('this', self.class_name, v_scope)

        if self.get_current_token() != ')':
            v_type = self.get_current_token_and_advance()
            v_name = self.get_current_token_and_advance()
            self.symbol_table.add(v_name, v_type, v_scope)

            while self.get_current_token() == ',':
                self.advance()
                v_type = self.get_current_token_and_advance()
                v_name = self.get_current_token_and_advance()
                self.symbol_table.add(v_name, v_type, v_scope)

            if self.get_current_token() == ')':
                finished = True
                self.expect(')')
            else:
                self.expect(';')

        if not finished:
            self.expect(')')

    def compile_subroutine_variable_declarations(self):
        self.expect(expected_token='{', expected_type='symbol')

        while self.get_current_token() == 'var':
            self.expect(expected_token='var', expected_type='keyword')
            v_scope = 'local'
            v_type = self.get_current_token_and_advance()
            v_name = self.get_current_token_and_advance()
            self.symbol_table.add(v_name, v_type, v_scope)

            while self.get_current_token() == ',':
                self.advance()
                v_name = self.get_current_token_and_advance()
                self.symbol_table.add(v_name, v_type, v_scope)

            self.expect(expected_token=';')


    def compile_subroutine_statements(self):
        while self.get_current_token() in {'let', 'if', 'while', 'do', 'return'}:
            if self.get_current_token() == 'let':
                self.compile_let()
            elif self.get_current_token() == 'do':
                self.compile_do()
            elif self.get_current_token() == 'return':
                self.compile_return()
            elif self.get_current_token() == 'if':
                self.compile_if()
            elif self.get_current_token() == 'while':
                self.compile_while()

    def compile_let(self):
        self.expect('let', 'keyword')
        lhs_var_kind = self.symbol_table.kind_of(self.get_current_token())
        lhs_var_index = self.symbol_table.index_of(self.get_current_token())
        if self.peek(1)[0] != '[':
            self.expect(expected_type='identifier')
            self.expect('=', 'symbol')
            self.compile_expression()
            self.vm_writer.write_pop(lhs_var_kind, lhs_var_index)
        else:
            self.advance()
            self.vm_writer.write_push(lhs_var_kind, lhs_var_index)
            self.expect('[')
            self.compile_expression()
            self.expect(']')
            self.vm_writer.write_arithmetic('add')
            self.expect('=', 'symbol')
            is_rhs_array = self.peek(1)[0] == '['
            if not is_rhs_array:
                self.vm_writer.write_pop('pointer', 1)
                self.compile_expression()
                self.vm_writer.write_pop('that', 0)
            else:
                rhs_var_kind = self.symbol_table.kind_of(self.get_current_token())
                rhs_var_index = self.symbol_table.index_of(self.get_current_token())
                self.vm_writer.write_push(rhs_var_kind, rhs_var_index)
                self.expect(expected_type='identifier')
                self.expect('[', 'symbol')
                self.compile_expression()
                self.expect(']', 'symbol')
                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)
                self.vm_writer.write_pop('temp', 0)
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('temp', 0)
                self.vm_writer.write_pop('that', 0)

        self.expect(';')

    def compile_return(self):
        self.expect('return', 'keyword')
        if self.get_current_token() == ';':
            self.vm_writer.write_push('constant', 0)
        else:
            self.compile_expression()
        self.expect(';')
        self.vm_writer.write_return()

    def compile_do(self):
        self.expect('do', 'keyword')
        self.compile_subroutine_call()
        self.vm_writer.write_pop('temp', 0)
        self.expect(';')

    def compile_if(self):
        l0 = f'IF_FALSE{self.get_counter()}'
        l1 = f'IF_TRUE{self.get_counter()}'

        self.expect('if', 'keyword')
        self.expect('(', 'symbol')
        self.compile_expression()
        self.expect(')', 'symbol')
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(l0)
        self.expect('{', 'symbol')
        self.compile_subroutine_statements()
        self.expect('}', 'symbol')
        self.vm_writer.write_goto(l1)
        self.vm_writer.write_label(l0)
        if self.get_current_token() == 'else':
            self.expect('else', 'keyword')
            self.expect('{', 'symbol')
            self.compile_subroutine_statements()
            self.expect('}', 'symbol')
        self.vm_writer.write_label(l1)

    def compile_while(self):
        l0 = f'TRUE{self.get_counter()}'
        l1 = f'FALSE{self.get_counter()}'

        self.vm_writer.write_label(l0)

        self.expect('while', 'keyword')
        self.expect('(', 'symbol')
        self.compile_expression()
        self.expect(')', 'symbol')

        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(l1)

        self.expect('{', 'symbol')
        self.compile_subroutine_statements()
        self.expect('}', 'symbol')

        self.vm_writer.write_goto(l0)

        self.vm_writer.write_label(l1)

    def compile_subroutine_call(self):
        """
        subroutineCall:
            subroutineName '(' expressionList ')'
          | (className | varName) '.' subroutineName '(' expressionList ')'

        square.draw();
        name = square
        sub_name = draw

        Output.printInt(1 + (2 * 3));
        name = Output
        sub_name = printInt
        """
        name, token_type = self.peek()
        # name is either subroutineName, className, varName
        self.advance()
        n_args = 0

        if self.get_current_token() == '.':
            self.expect('.')
            sub_name = self.get_current_token_and_advance()

            if self.symbol_table.kind_of(name) is not None:
                # method call on an object
                type_name = self.symbol_table.type_of(name)
                self.vm_writer.write_push(self.symbol_table.kind_of(name),
                                          self.symbol_table.index_of(name))

                n_args += 1
                full_name = f'{type_name}.{sub_name}'

            else:
                full_name = f'{name}.{sub_name}'

        else:
            self.vm_writer.write_push('pointer', 0)
            n_args += 1
            full_name = f'{self.class_name}.{name}'

        self.expect('(')
        n_args += self.compile_expression_list()
        self.expect(')')

        self.vm_writer.write_call(full_name, n_args)

    def compile_expression(self):
        previous_op = self.peek()[0]
        self.compile_term()

        while self.get_current_token() and self.get_current_token() in {'+', '-', '~', '*', '/', '&', '|', '<', '>', '='}:
            if self.get_current_token() == '+':
                op = 'add'
            elif self.get_current_token() == '-':
                if previous_op in {'+', '-', '~', '*', '/', '&', '|', '<', '>', '='}:
                    op = 'neg'
                else:
                    op = 'sub'
            elif self.get_current_token() == '~':
                op = 'not'
            elif self.get_current_token() == '*':
                op = f'call Math.multiply 2'
            elif self.get_current_token() == '/':
                op = f'call Math.divide 2'
            elif self.get_current_token() == '&':
                op = 'and'
            elif self.get_current_token() == '|':
                op = 'or'
            elif self.get_current_token() == '<':
                op = 'lt'
            elif self.get_current_token() == '>':
                op = 'gt'
            elif self.get_current_token() == '=':
                op = 'eq'
            else:
                op = '0'

            previous_op = self.get_current_token()
            self.advance()
            self.compile_term()
            if op != '0':
                self.vm_writer.write_arithmetic(op)

    def compile_term(self):
        token, token_type = self.peek()

        if token_type == 'integerConstant':
            self.handle_integer_term()
        elif token_type == 'stringConstant':
            if len(token) == 1:
                self.handle_char_term()
            else:
                self.handle_string_term()
        elif token in {'true', 'false', 'null', 'this'}:
            self.handle_keyword_term()
        elif token in {'-', '~'}:
            if token == '-':
                op = 'neg'
            else:
                op = 'not'
            self.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op)
        elif token == '(':
            self.expect('(')
            self.compile_expression()
            self.expect(')')
        elif token_type == 'identifier':
            self.handle_identifier_term()

    def compile_expression_list(self)->int:
        n_args = 0
        if self.peek()[0] != ')':
            self.compile_expression()
            n_args += 1
            while self.peek()[0] == ',':
                self.advance()
                self.compile_expression()
                n_args += 1
        return n_args

    def handle_integer_term(self):
        self.vm_writer.write_push('constant', self.get_current_token())
        self.advance()
        
    def handle_char_term(self):
        self.vm_writer.write_push('constant', ord(self.get_current_token()))
        self.advance()

    def handle_string_term(self):
        self.vm_writer.write_push('constant', len(self.get_current_token()))
        self.vm_writer.write_call('String.new', 1)
        for c in self.get_current_token():
            self.vm_writer.write_push('constant', ord(c))
            self.vm_writer.write_call('String.appendChar', 2)
        self.advance()

    def handle_keyword_term(self):
        if self.get_current_token() == 'true':
            self.vm_writer.write_push('constant', 1)
            self.vm_writer.write_arithmetic('neg')
        elif self.get_current_token() in {'false', 'null'}:
            self.vm_writer.write_push('constant', 0)
        else:  # this
            self.vm_writer.write_push('pointer', 0)
        self.advance()

    def handle_identifier_term(self):
        token = self.get_current_token()
        next_token,_ = self.peek(1)

        if next_token == '[':
            self.push_array_address()
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_push('that', 0)
        elif next_token in {'.', '('}:
            self.compile_subroutine_call()
        else:  # simple variable name
            kind = self.symbol_table.kind_of(token)
            index = self.symbol_table.index_of(token)
            self.vm_writer.write_push(kind, index)
            self.advance()

    def handle_array_identifier(self):
        token = self.get_current_token()
        kind = self.symbol_table.kind_of(token)
        index = self.symbol_table.index_of(token)
        self.vm_writer.write_push(kind, index)

        self.advance()

        self.expect('[')
        self.compile_expression()
        self.expect(']')

        self.vm_writer.write_arithmetic('add')

        self.vm_writer.write_pop('pointer', 1)
        self.vm_writer.write_push('that', 0)

    def push_array_address(self):
        kind = self.symbol_table.kind_of(self.get_current_token())
        index = self.symbol_table.index_of(self.get_current_token())
        self.vm_writer.write_push(kind, index)  # base address
        self.advance()
        self.expect('[')
        self.compile_expression()
        self.expect(']')
        self.vm_writer.write_arithmetic('add')


