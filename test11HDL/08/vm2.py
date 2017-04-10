# -*- coding:utf-8 -*-


class Vm2:
    def __init__(self, filename, static_num=16):
        self.filename = filename
        self.static_num = static_num
        self.temp = 5
        self.global_stack = 256
        self.pointer = 3
        self.temp = 5
        self.local = 300
        self.arg = 400
        self.this = 'THIS'
        self.that = 'THAT'
        self.eq_label = 0
        self.gt_label = 0
        self.lt_label = 0
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
                if c_type in ['C_PUSH', 'C_POP', 'C_LABEL', 'IF_INS', 'GOTO_INS']:
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
        if 'if' in line:
            return 'IF_INS'
        if 'goto' in line:
            return 'GOTO_INS'
        return 'UNKNOWN'

    def write_push_pop(self, line):
        ll = line.split(' ')
        if len(ll) > 2:
            pp, arg1, arg2 = ll
        else:
            pp, arg1 = ll
            arg2 = ''
        if pp == 'push':
            cmd = 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            if arg1 == 'constant':
                cmd = '@{arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(arg2=arg2)
            elif arg1 == 'local':
                cmd = '@{local}\n'.format(local=self.local + int(arg2)) + cmd
            elif arg1 == 'argument':
                cmd = '@{arg}\n'.format(arg=self.arg + int(arg2)) + cmd
            elif arg1 == 'this':
                _cmd = '@{_this}\nA=M\n'.format(_this=self.this)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd = _cmd + cmd
            elif arg1 == 'that':
                _cmd = '@{that}\nA=M\n'.format(that=self.that)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd = _cmd + cmd
            elif arg1 == 'temp':
                cmd = '@{temp}\n'.format(temp=self.temp + int(arg2)) + cmd
            elif arg1 == 'pointer':
                cmd = '@{pointer}\n'.format(pointer=self.pointer + int(arg2)) + cmd
            elif arg1 == 'static':
                cmd = '@{static}\n'.format(static=self.static_num + int(arg2)) + cmd
        elif pp == 'pop':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n'
            if arg1 == 'local':
                cmd += '@{local}\nM=D\n'.format(local=self.local + int(arg2))
            elif arg1 == 'argument':
                cmd += '@{arg}\nM=D\n'.format(arg=self.arg + int(arg2))
            elif arg1 == 'this':
                _cmd = '@{_this}\nA=M\n'.format(_this=self.this)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd += _cmd + 'M=D\n'
            elif arg1 == 'that':
                _cmd = '@{that}\nA=M\n'.format(that=self.that)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd += _cmd + 'M=D\n'
            elif arg1 == 'temp':
                cmd += '@{temp}\nM=D\n'.format(temp=self.temp + int(arg2))
            elif arg1 == 'pointer':
                cmd += '@{pointer}\nM=D\n'.format(pointer=self.pointer + int(arg2))
            elif arg1 == 'static':
                cmd += '@{static}\nM=D\n'.format(static=self.static_num + int(arg2))
        elif pp == 'label':
            cmd = '({label})\n'.format(label=arg1)
        elif pp == 'if-goto':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@{label}\nD;JNE\n'.format(label=arg1)
        elif pp == 'goto':
            cmd = '@{label}\n0;JMP\n'.format(label=arg1)
        else:
            cmd = 'None\n'
        return cmd

    def write_arithmetic(self, line):
        arg1 = line.strip()
        if arg1 == 'add':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n'
        elif arg1 == 'sub':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n'
        elif arg1 == 'neg':
            cmd = '@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n'
        elif arg1 == 'eq':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n' \
                  '@{true}\nD;JEQ\n' \
                  'D=0\n@{back}\n0;JMP\n' \
                  '({true})\nD=-1\n' \
                  '({back})\n@SP\nA=M\nM=D\n' \
                  '@SP\nM=M+1\n'.format(true=self.filename.split('.')[0] + 'eq' + str(self.eq_label),
                                        back=self.filename.split('.')[0] + 'eq' + str(self.eq_label) + str(self.eq_label))
            self.eq_label += 1
        elif arg1 == 'gt':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n' \
                  '@{true}\nD;JGT\n' \
                  'D=0\n@{back}\n0;JMP\n' \
                  '({true})\nD=-1\n' \
                  '({back})\n@SP\nA=M\nM=D\n' \
                  '@SP\nM=M+1\n'.format(true=self.filename.split('.')[0] + 'gt' + str(self.gt_label),
                                        back=self.filename.split('.')[0] + 'gt' + str(self.gt_label) + str(self.gt_label))
            self.gt_label += 1
        elif arg1 == 'lt':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n' \
                  '@{true}\nD;JLT\n' \
                  'D=0\n@{back}\n0;JMP\n' \
                  '({true})\nD=-1\n' \
                  '({back})\n@SP\nA=M\nM=D\n' \
                  '@SP\nM=M+1\n'.format(true=self.filename.split('.')[0] + 'lt' + str(self.lt_label),
                                        back=self.filename.split('.')[0] + 'lt' + str(self.lt_label) + str(self.lt_label))
            self.lt_label += 1
        elif arg1 == 'and':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n'
        elif arg1 == 'or':
            cmd = '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n'
        elif arg1 == 'not':
            cmd = '@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n'
        else:
            cmd = ''
        return cmd

if __name__ == '__main__':
    # namelist = ['PointerTest.vm', 'StaticTest.vm']
    # static_num = 16
    p = Vm2('FibonacciSeries.vm')
    p.advance()
