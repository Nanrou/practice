# -*- coding:utf-8 -*-

import re
from string import ascii_letters, digits


def del_extra(need_to_trans):
    """
    去掉文本中，跟在 \ 符号后面的非中文字符
    :param need_to_trans:
    :return:
    """
    char_and_num = ascii_letters + digits + '\\' + '<br />' + ' '
    finish_trans = list(need_to_trans)
    for match in re.finditer(r'\\', need_to_trans):
        s = int(match.start()) - 1
        br_skip_flag = False
        while True:
            s += 1
            letter = need_to_trans[s]
            # if letter == '<':
            #     br_skip_flag = True
            # if letter == '>':
            #     br_skip_flag = False
            #     continue
            # if br_skip_flag:
            #     continue

            if letter in char_and_num:
                finish_trans[s] = ''
                continue
            if letter == ' ':
                continue
            break
    return ''.join(finish_trans)

