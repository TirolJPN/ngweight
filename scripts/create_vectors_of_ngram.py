"""
TODO:
ngweightでで作成した特徴語のリストから、そのN-gramの種類の数だけの次元の特徴ベクトルを
決まったフォーマットで作成する。
クラスタリング・可視化は別のスクリプトで行う。
pythonにおける階層クラスタリングは次を参照 https://qiita.com/suecharo/items/20bad5f0bb2079257568
問題の種類によっては次元数がアホみたいなことになるが、気にしないでとりあえず実行する
クラスタリング手法には最長距離法、メトリクスにはコサイン類似度(コサイン距離？)を用いる

ある一つの問題ごとに以下を実行する
1. 入力ファイル(input_files/hoge.txt)を参照する。1解答ごとに
    0x02[file_name]0x03 {単語群} 0x02[file_name]0x03 {単語群} 0x02[file_name]0x03 {単語群}...
    の形式になっているので、0x02[file_name]0x03を区切りに、1解答づつの文章を取得
2. output_filesの特徴語のリストと照らし合わせて、特徴語の種類(outputfileの行数と同じ)の次元を持つ特徴ベクトルを作成
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


"""
problem_idを引数として、前解答の特徴ベクトルを作成する
"""
def create_key_word_vectors(problem_id):



"""
ngweightに入力するファイルを用意する問題のid一覧を返す
"""
def get_problem_list():
    global cur
    sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    cur.execute(sql)
    return cur.fetchall()

def main():
    for problems in get_problem_list():
        create_key_word_vectors(problems['problem_id'])
        



if __name__ == '__main__':
    main()