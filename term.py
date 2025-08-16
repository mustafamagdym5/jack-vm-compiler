class Term(object):
    def __init__(self, term: str):
        self.term = term
        self.output = []

    def compile(self):
        if self.term.isdigit():
            return "integerConstant"
        elif self.term.startswith('"'):
            return "stringConstant"
        elif self.term in ["true", "false", "null", "this"]:
            return "keyword"
        return ""