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
import logging
import traceback

 
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

# 指定された文字列に時間を付与する。
# return: 与えられた文字列 + '_%Y%m%d_%H%M%S'
def add_time(value):
    today = datetime.today()
    return value + '_' + datetime.now().strftime("%Y%m%d_%H%M%S")
    
# ファイルの差分を取得する
# return: 差分のリスト
def get_diff_list(before, now):
    result = []
    d = difflib.Differ()
    with open(before, 'r') as before_file_list:
        with open(now, 'r') as now_file_list:

            backup_dst_path = get_first_node_config('backup_dst_path')
            backup_src_path = get_first_node_config('backup_src_path')

            b = before_file_list.read().replace(backup_dst_path, backup_src_path).splitlines(1)
            print len(b)
            n = now_file_list.read().splitlines(1)
            print len(n)
            result =  list(d.compare(b, n))
            
    return result
    
# ファイルの差分を取得する
# return: 差分だけのリスト
# def get_diff_only_list(before, now):
#     result = []
# 
#     with open(before, 'r') as before_file_list:
#         with open(now, 'r') as now_file_list:
# 
#             backup_dst_path = get_first_node_config('backup_dst_path')
#             backup_src_path = get_first_node_config('backup_src_path')
# 
#             b_list = before_file_list.read().replace(backup_dst_path, backup_src_path).splitlines(1)
#             print len(b_list)
#             n_list = now_file_list.read().splitlines(1)           
#             print len(n_list)
#             
#             for n_line in n_list:
#                 if n_line in before_file_list:
#                      print n_line
#                      result.append(n_line)
#             
#     return result

            
# 差分のファイルをコピーする。
# 引数：differ list
# return: なし
def copy_files(deff_list):
    for line in deff_list:
        if '+' in line:
            src_file = line.lstrip('+ ').rstrip()
            dst_file = src_file.replace(get_first_node_config('backup_src_path'),
                                        get_first_node_config('backup_dst_path'))
            
            # ファイルを作成する
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(os.path.dirname(dst_file))
                
            print src_file
            print dst_file
            shutil.copy(src_file, dst_file)
            logging.info(dst_file)



def main():


    logging.basicConfig(filename='log/log.txt',level=logging.DEBUG, datefmt='%Y/%m/%d %h:%M:%S %p',
                        format='%(levelname)s\t%(asctime)s:%(message)s')
    logging.info('******バックアップ開始******')

    try:
        # 前回バックアップされたファイルの一覧を取得する。
        backup_dst_path = get_first_node_config('backup_dst_path')
        dst_list_file_name = add_time('log/dst_file_list')
        # file_lotate(dst_list_file_name)
        create_file_list(backup_dst_path, dst_list_file_name)
        logging.info('前回バックアップしたファイルの一覧取得完了')
        logging.info(dst_list_file_name)
        
        # 現在のファイル一覧を作成する。
        backup_src_path = get_first_node_config('backup_src_path')
        src_list_file_name = add_time('log/src_file_list')
        # file_lotate(src_list_file_name)
        create_file_list(backup_src_path, src_list_file_name)
        logging.info('バックアップ対象ディレクトリのファイルの一覧取得完了')
        logging.info(src_list_file_name)
    
        # 現在と前回のファイルリストの差分を取得する。
        # result = get_diff_only_list(dst_list_file_name, src_list_file_name)    
        result = get_diff_list(dst_list_file_name, src_list_file_name)
        logging.info('差分判定完了')
    
        # 増えたファイルをバックアップフォルダにコピーする。
        logging.info('コピー開始')
        copy_files(result)
    
        a = 1/0
        logging.info('コピー完了')    
    except Exception as inst:
        logging.info('異常終了')    
        logging.error(type(inst))
        logging.error(inst.message)
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    sys.exit(main())
