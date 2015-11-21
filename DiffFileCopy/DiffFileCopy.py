# coding: utf-8


'''
Created on 2015/11/16

@author: robot_punk
'''

import sys
import os
import IOUtil
from xml.etree.ElementTree import *
import shutil
from datetime import datetime
import difflib
import filecmp
 
# 現在のファイル一覧を作成する
def write_now_file_list(backup_src_path, file_name):
    print backup_src_path
    target_files = IOUtil.get_all_files(backup_src_path)
#    write_file_list(file_name)
    with open(file_name, 'w') as f:
        for f_name in target_files:
            f.writelines(f_name + '\n')


# ファイルをローテートする
# return: ローテート後のファイル名
def file_lotate(file_name):
    src = file_name
    today = datetime.today()
    dst = file_name + '_' + str(today.year) + str(today.month) + str(today.day - 1)
    shutil.copyfile(src, dst)
    return dst
    
# 設定ファイルの値を取得する。
# 指定ノードの値を取得する。複数ある場合は最初に見つかったものを返す。
# return: 設定値
def get_first_node_config(node_name):
    tree = parse('./config.xml')
    return tree.getroot().find(node_name).text

def main():
    # ファイルリストをローテーションする。
    file_name = 'log/file_list'
    if (not os.path.exists(file_name)):
        f = open(file_name, 'w')
        f.close()

    before_file = file_lotate(file_name)

    # 現在のファイル一覧を作成する。
    backup_src_path = get_first_node_config('backup_src_path')
    write_now_file_list(backup_src_path, file_name)

    # 現在と過去のファイルの差分を取得する。
    result = []
    d = difflib.Differ()
    with open(before_file) as before_file_list:
        with open(file_name) as now_file_list:
            result  = list(d.compare(before_file_list.read().splitlines(1),
                                    now_file_list.read().splitlines(1)))



    # 増えたファイルをバックアップフォルダにコピーする。
    # TODO 行頭に+ がついた行のファイルのみをコピーする。
    for line in result:
        if '+' in line:
            src_file = line.lstrip('+ ').rstrip()
            print src_file
            dst_file = src_file.replace(get_first_node_config('backup_src_path'),
                                        get_first_node_config('backup_dst_path'))
            print dst_file
            
            # ファイルを作成する
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(os.path.dirname(dst_file))
                
            shutil.copy(src_file, dst_file)
            

if __name__ == '__main__':
    sys.exit(main())
