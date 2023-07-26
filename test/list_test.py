# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

test_list = ['a', 'b', 'c']


if test_list[0] == 'a':
    print('test1')
elif test_list[1] != 'a':
    print('test2')
elif test_list[5] == 'a':
    print('test3')
elif test_list[6] != 'a':
    print('test4')

print(test_list[6])

"""
test1
IndexError: list index out of range
"""