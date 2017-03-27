# -*- coding:utf-8 -*-


from string import digits


class Assembler:
    def __init__(self, filename):
        self.filename = filename
        self.symbol_table = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4',
                             'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3',
                             'R4': '4', 'R5': '5', 'R6': '6', 'R7': '7',
                             'R8': '8', 'R9': '9', 'R10': '10', 'R11': '11',
                             'R12': '12', 'R13': '13', 'R14': '14', 'R15': '15',
                             'SCREEN': '16384', 'KBD': '24576'}
        self.line = ''
        self.address = '16'
        self.rom_address = 0
        self.rom_table = {}
        self.d_dict = {'Null': '000', 'M': '001', 'D': '010',
                       'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
        self.c_dict = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
                       'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
                       '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
                       'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
                       'D&A': '0000000', 'D|A': '0010101',  'M': '1110000', '!M': '1110001',
                       '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
                       'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000', 'D|M': '1010101'}
        self.j_dict = {'null': '000', 'JGT': '001', 'JEQ': '010',
                       'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

    def before_do_main(self):
        """
        第一遍读取，构造ROM的对应表：（行数， 命令）
        构造RAM的对应表：（标签， 仅跟便签之后的行数）
        :return: 构造标签的对应表
        """
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('\n') or line.startswith('//'):
                    continue
                self.line = line.split('/')[0].strip()
                c_type = self.command_type()
                if c_type.startswith('L'):
                    str_part = self.line[1:-1]
                    self.symbol_table[str_part] = str(self.rom_address)  # 存到表里，按道理是应该存到rom里面，但是现在简单实现，所以就统一存放了
                    continue
                self.rom_table[str(self.rom_address)] = self.line
                self.rom_address += 1

    def do_main(self):
        """
        第二次读取
        逐行翻译A指令和C指令
        """
        self.before_do_main()
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('\n') or line.startswith('//'):
                    continue
                self.line = line.split('/')[0].strip()
                c_type = self.command_type()
                if c_type.startswith('C'):
                    d = self.dest()
                    c = self.comp()
                    j = self.jump()
                    str13 = self.turn_to_byte(d, c, j)
                    instruction = '111' + str13
                elif c_type.startswith('A'):
                    str_part = self.symbol()
                    str15 = bin(int(str_part)).split('b')[-1].rjust(15, '0')
                    instruction = '0' + str15
                else:
                    continue
                with open(self.filename.split('.')[0] + '1' + '.hack', 'a') as nf:
                    nf.write(instruction + '\n')

    def command_type(self):
        """
        判断指令类型
        """
        if self.line.startswith('@'):
            return 'A_COMMAND'
        if '(' in self.line and ')' in self.line:
            return 'L_COMMAND'
        return 'C_COMMAND'

    def symbol(self):
        """
        读取A指令的内容
        """
        ram_address = self.line[1:]
        for i in ram_address:
            if i not in digits:
                break
        else:
            return ram_address
        if self.symbol_table.get(ram_address):
            return self.symbol_table[ram_address]
        else:
            self.symbol_table[ram_address] = self.address
            self.address = str(int(self.address) + 1)
            return self.symbol_table[ram_address]

    def dest(self):
        """
        读取dest部分
        """
        if '=' in self.line:
            d = self.line.split('=')[0]
            return d

    def comp(self):
        """
        读取comp部分
        """
        if '=' in self.line:
            c = self.line.split('=')[-1]
            if ';' in c:
                c = c.split(';')[0]
                return c
            else:
                return c
        if ';' in self.line:
            c = self.line.split(';')[0]
            return c

    def jump(self):
        """
        读取jump部分
        """
        if ';' in self.line:
            return self.line.split(';')[-1]

    def turn_to_byte(self, d, c, j):
        """
        对传入的参数进行转换为二进制表示
        """
        _d = d if d is not None else 'Null'
        _c = c if c is not None else '0'
        _j = j if j is not None else 'null'
        if self.d_dict.get(_d):
            d_part = self.d_dict[_d]
            if self.c_dict.get(_c):
                c_part = self.c_dict[_c]
                if self.j_dict.get(_j):
                    j_part = self.j_dict[_j]
                    s = c_part + d_part + j_part
                    if len(s) == 13:
                        return s
        print('something happen in {}={};{}'.format(_d, _c, _j))
        raise Exception


if __name__ == '__main__':
    p = Assembler('Rect.asm')
    p.do_main()
