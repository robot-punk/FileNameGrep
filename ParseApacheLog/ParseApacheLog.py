# coding: utf-8

'''
Created on 2015/10/14

@author: okumurat
'''

import sys
import os
import datetime

SEPARATOR_BEFORE= ' '
SEPARATOR_AFTER = '\t'
CONTEXT_PATH = 'shugyo_app/'

SRC_FILE_PATH = 'access_log'
DST_FILE_PATH = 'access_' + datetime.datetime.now().strftime("%Y%m%d")+'.tsv'
HEADER = ['remote host', '', '', 'date', 'timezone',
          'request-url', 'status','response byte', 'request-from-url', 'User-Agent',
          '','', '', 'response time' ]

RESOURCE_LIST = ['gs','kh', 'kk', 'sh', 'sj', 'sk', 'za']

def main():
    with open(DST_FILE_PATH, 'w') as dst:
        for column in HEADER:
            dst.write(column + SEPARATOR_AFTER)
        dst.write('\n')
        
        with open(SRC_FILE_PATH, 'r') as src:
            for line in src.readlines():
                if (is_user_action(line)):
                    l = line.replace(SEPARATOR_BEFORE, SEPARATOR_AFTER)
                    dst.write(l)

    
def is_user_action(value):
    if (not 'POST' in value):
        return False

    resource_list = RESOURCE_LIST
    for id in resource_list:
        if (CONTEXT_PATH + id in value):
            return True
    
    return False

if __name__ == '__main__':
    sys.exit(main())
