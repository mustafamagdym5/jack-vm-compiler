class VMWriter(object):
    def __init__(self):
        self.output = []

    def write_push(self, segment: str, index: str or int):
        self.output.append(f'push {segment} {index}')

    def write_pop(self, segment: str, index: str or int):
        self.output.append(f'pop {segment} {index}')

    def write_arithmetic(self, command: str):
        self.output.append(f'{command}')

    def write_label(self, label: str):
        self.output.append(f'label {label}')

    def write_goto(self, label: str):
        self.output.append(f'goto {label}')

    def write_if(self, label: str):
        self.output.append(f'if-goto {label}')

    def write_call(self, name: str, n_args: str or int):
        self.output.append(f'call {name} {n_args}')

    def write_function(self, name: str, n_vars: str or int):
        self.output.append(f'function {name} {n_vars}')

    def write_return(self):
        self.output.append('return')