# -*- coding:utf-8 -*-


class Vm2:
    def __init__(self, filename, static_num=16):
        self.filename = filename
        self.static_num = static_num
        self.temp = 5
        # self.global_stack = 256
        self.pointer = 3
        self.temp = 5
        self.local = 'LCL'
        self.arg = 'ARG'
        self.this = 'THIS'
        self.that = 'THAT'
        self.FRAME = 13
        self.RET = 14
        self.re_address = 0
        self.eq_label = 0
        self.gt_label = 0
        self.lt_label = 0
        self.symbol_table = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4'}
        # self.ram_table = {'0': self.global_stack}
        self.nfn = filename.split('.')[0] + '.asm'
        with open(self.nfn, 'w') as nf:
            nf.write('')
            # nf.write('@{global_stack}\nD=A\n@SP\nM=D\n'.format(global_stack=261))
        # dont need init @sp
        # init_ins = 'call Sys.init'
        # self.trans_to_ins(init_ins)

    def advance(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line:
                    self.trans_to_ins(line)

    def trans_to_ins(self, line):
        if line.startswith('//'):
            return
        if '//' in line:
            line = line.split('//')[0]
        line = line.lower().strip()
        c_type = self.command_type(line)
        if c_type in ['C_PUSH', 'C_POP', 'C_LABEL', 'IF_INS', 'GOTO_INS', 'FUN_INS', 'RE_INS', 'CALL_INS']:
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
        if 'function' in line:
            return 'FUN_INS'
        if 'return' in line:
            return 'RE_INS'
        if 'call' in line:
            return 'CALL_INS'
        return 'UNKNOWN'

    def write_push_pop(self, line):
        ll = line.split(' ')
        if len(ll) > 2:
            pp, arg1, arg2 = ll
        elif len(ll) > 1:
            pp, arg1 = ll
            arg2 = ''
        else:
            pp = ll[0]
            arg1, arg2 = ['', '']
        if pp == 'push':
            cmd = 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            if arg1 == 'constant':
                cmd = '@{arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(arg2=arg2)
            elif arg1 == 'local':
                _cmd = '@{local}\nA=M\n'.format(local=self.local)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd = _cmd + cmd
            elif arg1 == 'argument':
                _cmd = '@{arg}\nA=M\n'.format(arg=self.arg)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd = _cmd + cmd
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
                _cmd = '@{local}\nA=M\n'.format(local=self.local)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd += _cmd + 'M=D\n'
            elif arg1 == 'argument':
                _cmd = '@{arg}\nA=M\n'.format(arg=self.arg)
                for _ in range(int(arg2)):
                    _cmd += 'A=A+1\n'
                cmd += _cmd + 'M=D\n'
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
        elif pp == 'function':
            cmd = '({f})\n'.format(f=arg1)
            for _ in range(int(arg2)):
                cmd += '@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        elif pp == 'return':
            cmd = '@LCL\nD=M\n@13\nM=D\n'  # FRAME = LCL
            cmd += '@5\nD=D-A\nA=D\nD=M\n@14\nM=D\n'  # RET = *(FRAME-5)
            cmd += '@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n'  # pop arg 0
            cmd += '@ARG\nD=M+1\n@SP\nM=D\n'  # SP = ARG+1
            cmd += '@13\nD=M\n@1\nD=D-A\nA=D\nD=M\n@THAT\nM=D\n'  # THAT = *(FRAME-1)
            cmd += '@13\nD=M\n@2\nD=D-A\nA=D\nD=M\n@THIS\nM=D\n'  # THIS = *(FRAME-2)
            cmd += '@13\nD=M\n@3\nD=D-A\nA=D\nD=M\n@ARG\nM=D\n'  # ARG = *(FRAME-3)
            cmd += '@13\nD=M\n@4\nD=D-A\nA=D\nD=M\n@LCL\nM=D\n'  # LCL = *(FRAME-4)
            cmd += '@14\nA=M\n0;JMP\n'  # go to RET
        elif pp == 'call':
            cmd = '@return_address' + str(self.re_address) + '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'  # push return address
            cmd += '@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'  # push LCL
            cmd += '@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'  # push ARG
            cmd += '@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'  # push THIS
            cmd += '@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'  # push THAT
            cmd += '@{n}\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n'.format(n=arg2)  # ARG = SP-n-5
            cmd += '@SP\nD=M\n@LCL\nM=D\n'  # LCL = SP
            cmd += '@{f}\n0;JMP\n'.format(f=arg1)  # go to f
            cmd += '(return_address' + str(self.re_address) + ')\n'  # (return address)
            self.re_address += 1
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


import os


def combine(filename_list, newname):
    nfn = 'nf.asm'
    for n in filename_list:
        with open(n, 'r') as f:
            doc = f.read()
            with open(nfn, 'a') as nfile:
                nfile.write(doc)
    for i in filename_list:
        os.remove(i)
    os.rename(nfn, newname)


if __name__ == '__main__':

    namelist = ['Sys.vm',]
    # nfnlist = ['Sys.asm', 'Main.asm']
    # static_num = 16
    for n in namelist:
        p = Vm2(n)
        p.advance()
    # combine(nfnlist, newname='FibonacciElement.asm')
