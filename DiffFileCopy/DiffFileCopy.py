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
 
# 指定されたディレクトリパスのファイルのリストを
# 指定されたファイルに書き込む
def create_file_list(dir_path, file_name):
    # print dir_path
    # print file_name
    target_files = IOUtil.get_all_files(dir_path)
    with open(file_name, 'w') as f:
        for f_name in target_files:
            f.writelines(f_name + '\n')


# ファイルをローテートする
# return: ローテート後のファイル名
def file_lotate(file_name):
    if (not os.path.exists(file_name)):
        return

    src = file_name
    today = datetime.today()
    dst = file_name + '_' + str(today.year) + str(today.month) + str(today.day - 1)
    shutil.copyfile(src, dst)
    
# 設定ファイルの値を取得する。
# 指定ノードの値を取得する。複数ある場合は最初に見つかったものを返す。
# return: 設定値
def get_first_node_config(node_name):
    tree = parse('./config.xml')
    return tree.getroot().find(node_name).text

def add_time(value):
    today = datetime.today()
    return value + '_' + datetime.now().strftime("%Y%m%d_%H%M%S")
    
def get_diff_list(before, now):
    result = []
    d = difflib.Differ()
    with open(before) as before_file_list:
        with open(now) as now_file_list:
            result  = list(d.compare(before_file_list.read().splitlines(1),
                                    now_file_list.read().splitlines(1)))
    
    return result
            
    
def main():

    # 前回バックアップされたファイルの一覧を取得する。
    backup_dst_path = get_first_node_config('backup_dst_path')
    dst_list_file_name = add_time('log/dst_file_list')
    # file_lotate(dst_list_file_name)
    create_file_list(backup_dst_path, dst_list_file_name)
    
    # 現在のファイル一覧を作成する。
    backup_src_path = get_first_node_config('backup_src_path')
    src_list_file_name = add_time('log/src_file_list')
    # file_lotate(src_list_file_name)
    create_file_list(backup_src_path, src_list_file_name)

    # 現在と前回のファイルリストの差分を取得する。
    result = get_diff_list(dst_list_file_name, src_list_file_name)



    # 増えたファイルをバックアップフォルダにコピーする。
    for line in result:
        if '+' in line:
            src_file = line.lstrip('+ ').rstrip()
            dst_file = src_file.replace(get_first_node_config('backup_src_path'),
                                        get_first_node_config('backup_dst_path'))
            
            # ファイルを作成する
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(os.path.dirname(dst_file))
                
            shutil.copy(src_file, dst_file)
            print line

if __name__ == '__main__':
    sys.exit(main())
