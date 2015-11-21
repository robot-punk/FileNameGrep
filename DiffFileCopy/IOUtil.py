# coding: utf-8
import io
import os
import re
import glob
import fnmatch
import csv


def get_all_files(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)

def get_files(path, extension):
    for root, dirs, files in os.walk(path):
        for f in files:
            if fnmatch.fnmatch(f, extension):
                yield os.path.join(root, f)

def get_all_files_without_svn(path):
    for p in get_all_files(path):
        if fnmatch.fnmatch(p, u'*.svn*'):
            continue
        else:
            yield p
            

def get_files_without_svn(path, extension):
    for p in get_files(path, extension):
        if fnmatch.fnmatch(p, u'*.svn*'):
            continue
        else:
            yield p

    








        
        
