from pathlib import Path
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

class JackCompiler(object):
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.tokens = []
        self.vm_code = []

    def set_tokens(self):
        jt = JackTokenizer(self.file_name)
        self.tokens = jt.tokenize()

    def set_vm_code(self):
        self.set_tokens()
        ce = CompilationEngine(self.tokens)
        ce.compile_class()
        self.vm_code = ce.output

    def compile_project(self):
        if self.file_name.endswith('.jack'):
            self.compile_file()
        else:
            directory = Path(self.file_name)
            all_files = [self.file_name + '/' + f.name for f in directory.iterdir() if
                         f.is_file() and f.name.endswith(".jack")]
            for file_name in all_files:
                # self.compile_file(file_name)
                jk = JackCompiler(file_name)
                jk.compile_file()

    def compile_file(self):
        self.set_vm_code()
        vm_file_name = self.file_name.split('.')[0] + '.vm'
        handler = open(vm_file_name, 'w')

        for vm_line in self.vm_code:
            handler.write(vm_line + '\n')

        handler.close()


def compile_jack_to_vm(file_name):
    jk = JackCompiler(file_name)
    jk.compile_project()