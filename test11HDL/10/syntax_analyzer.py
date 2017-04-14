# -*- coding:utf-8 -*-


import string


class JackTokenizer:
    def __init__(self, fname=None):
        self.fname = fname
        self.STable = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~')
        self.KWtable = ('class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                        'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')

    def advance(self):
        with open('ppp'+self.fname.split('.')[0]+'.xml', 'w') as nn:  # 等后面实现完逻辑之后要删除掉的
            nn.write('<tokens>'+'\n')
        with open(self.fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('\n') or line.startswith('/'):
                    continue
                if '//' in line:
                    line = line.split('//')[0]
                # if not line.endswith('/n'):
                #     line += '\n'
                line = line.strip()
                if line:
                    # pass
                    tokenlist = self.constructor_token(line)
                    for token in tokenlist:
                        token, t_type = self.token_type(token)
                        with open('ppp'+self.fname.split('.')[0]+'.xml', 'a') as nf:
                            nf.write('<{type}> {token} </{type}>'.format(token=token, type=t_type)+'\n')
        with open('ppp'+self.fname.split('.')[0]+'.xml', 'a') as nff:
            nff.write('</tokens>'+'\n')

    def constructor_token(self, line):  # 分割出子元
        token_list = []
        temp_list = line.split()
        temp = ''
        for i in temp_list:
            if i.startswith('"') and i.endswith('"'):  # 提前处理字符串
                token_list.append(i)
                continue
            if i.startswith('"'):
                temp = i
                continue
            if '"' in i:
                head, tail = i.split('"')
                temp_list.append(temp + ' ' + head + '"')
                temp_list.append(tail)
                continue
            token = ''
            for c in i:
                if c in self.STable:  # 主体思路是，把符号提取出来
                    if token:
                        token_list.append(token)
                    token_list.append(c)
                    token = ''
                else:
                    token += c
            if token:
                token_list.append(token)
        return token_list

    def token_type(self, token):
        if token in self.STable:
            return [token, 'symbol']
        if token in self.KWtable:
            return [token, 'keyword']
        if token.startswith('"') or token.startswith("'"):
            token = token[1:-1]
            return [token, 'stringConstant']
        for i in token:
            if i not in string.digits:
                break
        else:
            return [token, 'integerConstant']
        return [token, 'identifier']


if __name__ == '__main__':
    j = JackTokenizer('Main.jack')
    j.advance()
    # statement = 'let s = "string constant";'
    # print(j.constructor_token(statement))
