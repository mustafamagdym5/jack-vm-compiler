import re

class JackTokenizer:

    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'new', 'field', 'static', 'var',
        'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
        'let', 'do', 'if', 'else', 'while', 'return'
    }

    SYMBOLS = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~'
    }

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.string_code = ""
        self.tokens = []

    def get_code_from_file(self)->str:
        code = ""
        has_seen_class = False
        try:
            file_handler = open(self.file_name)
            for line in file_handler:
                line = line.strip()
                if re.search(r'^\s*class\s+([A-Za-z_]\w*)', line):
                    has_seen_class = True
                if has_seen_class and line and line[0] != '/' and line[0] != '*':
                    self.string_code += line.split('//')[0].split('/*')[0].strip()
            code = self.string_code
            file_handler.close()
        except IOError:
            print("File is not exist")
        return code

    def tokenize(self)->list[tuple[str, str]]:
        self.tokenize_helper()
        list_of_tokens = []
        for token in self.tokenize_helper():
            if token[1] != '0':
                if token[1] == 'keyword' and token[0] not in self.KEYWORDS:
                    token = token[0], 'identifier'
                list_of_tokens.append(token)
        self.tokens = list_of_tokens
        return self.tokens

    def tokenize_helper(self)->list[tuple[str, str]]:
        token = ""
        self.get_code_from_file()
        self.tokens = []
        i = 0
        while i < len(self.string_code):
            letter = self.string_code[i]
            token_type = self.get_type_of_token(token)

            if letter == ' ':
                if token:
                    self.tokens.append((token, token_type))
                    token = ""
                i += 1
                continue
            token += letter
            # Handle symbols
            if letter in self.SYMBOLS:
                if token:
                    self.tokens.append((token[:-1], token_type))
                self.tokens.append((letter, "symbol"))
                token = ""
            # Handle keyword
            elif token_type == "keyword" and self.string_code[i+1] == ' ':
                self.tokens.append((token, token_type))
                token = ""
            # Handle integerConstant
            elif letter.isdigit():
                integer_constant = ""
                while i < len(self.string_code) and self.string_code[i].isdigit():
                    integer_constant += self.string_code[i]
                    i += 1
                i -= 1
                self.tokens.append((integer_constant, "integerConstant"))
                token = ""
            # Handle stringConstant
            elif letter == '"':
                i += 1
                string_constant = ""
                while i < len(self.string_code) and self.string_code[i] != '"':
                    string_constant += self.string_code[i]
                    i += 1
                self.tokens.append((string_constant, "stringConstant"))
                token = ""

            i += 1
        return self.tokens

    def get_type_of_token(self, token: str)->str:
        if token in self.KEYWORDS:
            return "keyword"
        elif token in self.SYMBOLS:
            return "symbol"
        elif token.isdigit() and 0 <= int(token) <= 32767:
            return "integerConstant"
        elif token.startswith('"') and token.endswith('"'):
            return "stringConstant"
        elif re.fullmatch(r"[A-Za-z_]\w*", token):
            return "identifier"
        return '0'


if __name__ == '__main__':
    # jk1 = JackTokenizer("Square/Main.jack")
    # for k, v in jk1.tokenize():
    #     print(k, v)

    # jk2 = JackTokenizer("Square/Square.jack")
    # for k, v in jk2.tokenize():
    #     print(k, v)

    # jk3 = JackTokenizer("Square/SquareGame.jack")
    # for k, v in jk3.tokenize():
    #     print(k, v)
    #
    # jk4 = JackTokenizer("ArrayTest/Main.jack")
    # for k, v in jk4.tokenize():
    #     print(k, v)

    # jk5 = JackTokenizer("Seven/Main.jack")
    # for k, v in jk5.tokenize():
    #     print(k, v)

    # jk6 = JackTokenizer("Pong/Ball.jack")
    # for k, v in jk6.tokenize():
    #     print(k, v)

    # jk7 = JackTokenizer('Pong/Main.jack')
    # for k, v in jk7.tokenize():
    #     print(k, v)

    print()


