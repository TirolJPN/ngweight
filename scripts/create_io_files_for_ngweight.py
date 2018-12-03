"""
TODO:
ngweightに入力するためのファイルを用意する
「733」「633」の２つで試験する
保存先のフォルダはfeature_word_vectorsとかにする
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
from enum import  Enum
import re
import subprocess
import sys

# グローバル変数
cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='khkh5813',
    port='3306',
    database='codeforces'
)
cur = cnx.cursor(buffered=True, dictionary=True)

path_feature_word_vectors = r'../input_files/'
path_src = r'./../../Database/src_original/src_original/'
path_input_files = r'./../input_files/'
path_output_files = r'./../output_files/'


"""
code from http://maku77.github.io/python/io/remove-java-comments.html
"""
class State(Enum):
    CODE = 1
    C_COMMENT = 2
    CPP_COMMENT = 3
    STRING_LITERAL = 4

def filter_cpp_comment(text):
    """ Removes Java (C/C++) style comments from text. """
    result = []  # filtered text (char array)
    prev = ''  # previous char
    prevprev = ''  # previous previous char
    state = State.CODE

    for ch in text:
        # Skip to the end of C-style comment
        if state == State.C_COMMENT:
            if prevprev != '\\' and prev == '*' and ch == '/':  # End comment
                state = State.CODE
                prevprev = prev = ''
            elif ch == '\n':
                result.append('\n')
                prevprev = prev = ''
            else:
                prevprev, prev = prev, ch
            continue

        # Skip to the end of the line (C++ style comment)
        if state == State.CPP_COMMENT:
            if ch == '\n':  # End comment
                state = State.CODE
                result.append('\n')
                prevprev = prev = ''
            continue

        # Skip to the end of the string literal
        if state == State.STRING_LITERAL:
            if prev != '\\' and ch == '"':  # End literal
                state = State.CODE
            result.append(prev)
            prevprev, prev = prev, ch
            continue

        # Starts C-style comment?
        if prevprev != '\\' and prev == '/' and ch == '*':
            state = State.C_COMMENT
            prevprev = prev = ''
            continue

        # Starts C++ style comment?
        if prevprev != '\\' and prev == '/' and ch == '/':
            state = State.CPP_COMMENT
            prevprev = prev = ''
            continue

        # Comment has not started yet
        if prev: result.append(prev)

        # Starts string literal?
        if ch == '"':
            state = State.STRING_LITERAL
        prevprev, prev = prev, ch

    # Returns filtered text
    if prev: result.append(prev)
    return ''.join(result)


"""
problem_idを引数として、それに該当するソースコードの一覧をFileテーブルから取ってくる
コンテスト中、コンテスト外の全てのソースコードにおいて、
verdictがOKとなっているソースコードのみ対象
"""
def get_right_answers(problem_id):
    global cur
    lang_list = ['GNU C++14', 'GNU C++11', 'GNU C++']
    lang_select = '(%s)' % ' or '.join(["lang='%s'" % lang for lang in lang_list])
    sql = "SELECT * FROM File WHERE problem_id LIKE \"%s\" AND verdict = \"OK\" AND %s" % (problem_id, lang_select)
    cur.execute(sql)
    return cur.fetchall()

"""
problem_idを引数として、ngweight用の1つの入力ファイルを作成する
"""
def create_an_file_for_ngweight(problem_id):
    path_file = path_feature_word_vectors + problem_id + '.txt'

    # 入力ファイルがまだ作成されていなければ実行する
    if not os.path.isfile(path_file):
        answers = get_right_answers(problem_id)
        with open(path_file, mode='w', encoding='utf-8') as f_ngweight:
            for answer in answers:
                # 各解答のソースコードをngweight用のテキストファイルに追記していく
                path_answer = path_src +  answer['file_name']
                with open(path_answer, mode='r', encoding='utf-8') as f_src:
                        code_content = f_src.read()
                # ヘッダーにファイル名を入れておく
                f_ngweight.write(chr(2))
                f_ngweight.write(answer['file_name'])
                f_ngweight.write(chr(3))
                s = filter_cpp_comment(code_content)
                # 特殊記号をとりあえず空白に変換する
                processed_s = re.sub("\!|\?|\"|\'|#|\$|%|&|\||\(|\)|\{|\}|\[|\]|=|<|>|\+|-|\*|\/|\\|\~|\^|@|:|;|,|\.|\s+", " ", s)
                # 上記置換だと、改行・スペースのスペース変換による連続スペースが残るので、それらも一つのスペースにする
                processed_s = re.sub(r" +", " ", processed_s)
                f_ngweight.write(processed_s)
        # pythonスクリプトからngweightを直接実行し、出力ファイルを得る
        cmd = "../bin/default/ngweight -w -s 0 < ../input_files/%s.txt > ../output_files/%s_output" % (problem_id, problem_id)
        res = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
        sys.stdout.buffer.write(res.stdout)



"""
ngweightに入力するファイルを用意する問題のid一覧を返す
"""
def get_problem_list():
    global cur
    sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    cur.execute(sql)
    return cur.fetchall()


def main():
    for problem in get_problem_list():     
        create_an_file_for_ngweight(problem['problem_id'])

if __name__ == '__main__':
    main()