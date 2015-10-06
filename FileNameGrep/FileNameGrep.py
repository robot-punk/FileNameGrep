# coding: utf-8

import sys
import IOUtil
import os
import fnmatch
import csv
import Grep
import datetime


u'''main'''
def main(log_file):

    # argument check
    valid = validate_argument_program_parser(sys.argv)
    if not valid:
        print u'Canceled. invalid arguments.'
        exit()

    param     = sys.argv
    path      = param[1]
    file_name = param[2]
    extension = param[3]
    out_of_target = []
    if len(param) > 4:
        out_of_target = str(param[4]).split(u',')
        #for item in list:
        #    out_of_target[item] = item

    # get target files
    target_files = IOUtil.get_files_without_svn(path, extension)

    # execute grep
    file_dic = {}

    # write file open
    f = open(file_name, 'w')
    writer = csv.writer(f, delimiter=',',lineterminator="\n")
    write_header(writer)


    u'''grep for target file''' 
    for target_file in target_files:

        if len(file_dic) > 180: 
            break

        if not is_target(target_file, out_of_target):
            continue

        # ---- log start-----------------------------
        start_time = datetime.datetime.now()
        print target_file + ' start:' + str(start_time)
        log_file.writelines(target_file + ' start:' + str(start_time) + '\n')
        # ---- log end-----------------------------

        u'''grep with file name'''
        file = open(target_file, 'r')
        word_dic = {}
        for f in IOUtil.get_all_files_without_svn(path):
            if not is_target(f, out_of_target):
                continue

            f_name = os.path.basename(f)
            f_name_without_ext, ext = os.path.splitext(f_name)

            #line_dic = Grep.grep(target_file, f_name_without_ext)
            #line_dic = Grep.grep_for_file(file, f_name_without_ext)
            line_dic = Grep.grep_for_file_count_0(file, f_name_without_ext, True)
            file.seek(0,os.SEEK_SET)

            if f not in word_dic:
                word_dic[f] = line_dic

        for word in sorted(word_dic):
            line_dic = word_dic.get(word, {})
            for line in sorted(line_dic):
                value = line_dic.get(line, u'')
                search_word, ext = os.path.splitext(os.path.basename(word))
                writer.writerow([f_name,
                                f,
                                search_word,
                                word,
                                line,
                                value])

        #file_dic[target_file] = word_dic
        #file.close

        end_time = datetime.datetime.now()
        print target_file + ' end:' + str(end_time)
        log_file.writelines(target_file + ' end:' + str(end_time) + '\n')
        log_file.flush()

        
    # output result
    
    #for file_path in sorted(file_dic):
    #    word_dic = file_dic.get(file_path, {})

    #    for word in sorted(word_dic):
    #        line_dic = word_dic.get(word, {})
    #        for line in sorted(line_dic):
    #            value = line_dic.get(line, u'')
    #            search_word, ext = os.path.splitext(os.path.basename(word))
    #            writer.writerow([os.path.basename(file_path),
    #                            file_path,
    #                            search_word,
    #                            word,
    #                            line,
    #                            value])

    #f.close
    
u'''validate arguments(default)'''
def validate_argument(args):

    u'number of arguments'
    if len(args) != 5:
        print u'引数は4つ指定してください。'
        print u'1.フォルダパス'
        print u'2.出力するファイル名'
        print u'3.検索対象（ワイルドカード有効）'
        print u'4.検索する文字列'

        return False

    u'is exist target folder'
    if not os.path.exists(args[1]):
        print u'指定したフォルダが見つかりませんでした。'
        print u'パス' + args[1]

        return False

    return True

u'''validate arguments_for_program_parser'''
def validate_argument_program_parser(args):
    u'number of arguments'
    if not (len(args) == 4 or len(args) == 5) :
        print u'引数は3つ、または4つ指定してください。'
        print u'1.フォルダパス'
        print u'2.出力するファイル名'
        print u'3.検索対象（ワイルドカード有効）'
        print u'4.検索対象外（ワイルドカード有効）[オプション]'


        return False

    u'is exist target folder'
    if not os.path.exists(args[1]):
        print u'指定したフォルダが見つかりませんでした。'
        print u'パス' + args[1]

        return False

    return True

def is_target(path, out_of_target):
    basename, ext = os.path.splitext(os.path.basename(path))

    if ext == '':
        return False

    for i in range(0, len(out_of_target)):
        if fnmatch.fnmatch(path, out_of_target[i]):
            return False

    return True

def write_header(csv_writer):
    csv_writer.writerow([u'検索対象ファイル名'.encode('cp932'),
                         u'検索対象ファイル名 (フルパス)'.encode('cp932'),
                         u'検索文字列'.encode('cp932'),
                         u'検索文字列 フルパス'.encode('cp932'),
                         u'該当行番号'.encode('cp932'),
                         u'該当行'.encode('cp932')])



if __name__ == '__main__':
    
    log_file = open('log.txt', 'wb')
    try:
        start_time = datetime.datetime.now()
        print start_time
        log_file.writelines(str(start_time) + '\n')

        main(log_file)

        end_time = datetime.datetime.now()
        print end_time
        log_file.writelines(str(end_time) + '\n')
    except Exception as e:
        print 'type:' + str(type(e))
        print 'args:' + str(e.args)
        print 'message:' + e.message
        print 'e:' + str(e)
        log_file.writelines('type:' + str(type(e)))
        log_file.writelines('args:' + str(e.args))
        log_file.writelines('message:' + e.message)
        log_file.writelines('e:' + str(e))
    finally:
        log_file.close




