# -*- coding:utf-8 -*-


class Vm1:
    def __init__(self, filename):
        self.filename = filename
        self.global_stack = 256
        self.symbol_table = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4'}
        self.ram_table = {'0': self.global_stack}
        self.nfn = filename.split('.')[0] + '.asm'
        with open(self.nfn, 'w') as nf:
            nf.write('@{global_stack}\nD=A\n@SP\nM=D\n'.format(global_stack=self.global_stack))

    def advance(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('//'):
                    continue
                if '//' in line:
                    line = line.split('//')[0]
                line = line.lower().strip()
                c_type = self.command_type(line)
                if c_type in ['C_PUSH', 'C_POP']:
                    cmd = self.write_push_pop(line)
                elif c_type == 'C_ARITHMETIC':
                    cmd = self.write_arithmetic(line)
                else:
                    cmd = ''
                with open(self.nfn, 'a') as nf:
                    nf.write(cmd)

    def command_type(self, line):
        if line in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        if 'push' in line:
            return 'C_PUSH'
        if 'pop' in line:
            return 'C_POP'
        if 'label' in line:
            return 'C_LABEL'
        return 'UNKNOWN'

    def write_push_pop(self, line):
        arg1, arg2 = line.split(' ')[1:]
        if arg1 == 'constant':
            self.ram_table[self.symbol_table['SP']] = self.global_stack
            self.ram_table[str(self.global_stack)] = arg2
            self.global_stack += 1
            cmd = '@{arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(arg2=arg2)
        else:
            cmd = 'None\n'
        return cmd

    def write_arithmetic(self, line):
        arg1 = line.strip()
        if arg1 == 'add':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n'
        elif arg1 == 'sub':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D-M\n@SP\nM=M+1\n'
        elif arg1 == 'neg':
            cmd = ''
        else:
            cmd = ''
        return cmd

if __name__ == '__main__':
    p = Vm1('SimpleAdd.vm')
    p.advance()
    print(p.ram_table)
