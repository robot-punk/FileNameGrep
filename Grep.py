# coding: utf-8
import fnmatch

u'''execute grep '''
def grep(path, word):
    i = 1
    result = {}
    file = open(path, 'r')
    for line in file:
        w = u'*' + word + u'*'
        if fnmatch.fnmatch(line, w):
            result[i] = line[:-1]
        i = i + 1

    file.close
    return result

u'''execute grep for file object'''
def grep_for_file(file, word):
    result = {}
    i = 0
    for line in file:
        w = u'*' + word + u'*'
        if fnmatch.fnmatch(line, w):
            result[i] = line[:-1]
        i = i + 1

    return result

#def grep(file, word):
#    i = 1
#    result = []
#    for line in file:
#        if fnmatch.fnmatch(line, word):
#            result.append(i + u':' + line)
#        i = i + 1

#    return result

