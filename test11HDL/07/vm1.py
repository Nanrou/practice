# -*- coding:utf-8 -*-
import linecache


class Parse:
    def __init__(self, filename):
        self.filename = filename

    def advance(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('//'):
                    continue

    def command_type(self, line):
        if '//' in line:
            line = line.split('//')[0]
        line = line.lower()
        if line in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        if 'push' in line:
            return 'C_PUSH'
        if 'pop' in line:
            return 'C_POP'
        if 'label' in line:
            return 'C_LABEL'
        return 'UNKNOWN'


if __name__ == '__main__':
    print('???')
    print(linecache.getline('SimpleAdd.vm', 1))

