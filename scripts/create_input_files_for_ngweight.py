"""
TODO:
ngweightに入力するためのファイルを用意する
「733」「633」の２つで試験する
保存先のフォルダはfeature_word_vectorsとかにする
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq

# グローバル変数
cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='khkh5813',
    port='3306',
    database='codeforces'
)
cur = cnx.cursor(buffered=True, dictionary=True)

path_feature_word_vectors = r'./'
path_src = r'./'


"""
problem_idを引数として、それに該当するソースコードの一覧をFileテーブルから取ってくる
コンテスト中、コンテスト外の全てのソースコードにおいて、
verdictがOKとなっているソースコードのみ対象
"""
def get_right_answers(problem_id):
        global cur
        sql = "SELECT * FROM File WHERE problem_id = %s AND verdict = OK" % problem_id
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
                with open(path_file, mode='w', encording = 'utf-8') as f_ngweight:
                        for answer in answer:
                                # 各解答のソースコードをngweight用のテキストファイルに追記していく
                                path_answer = path_src + answer['submission_id'] + '.src'
                                with open(path_answer, mode='r', encording='utf-8') as f_src:
                                        code_content = f_src.read()
                                f_ngweight.write(ord(2))
                                f_ngweight.write(code_content)
                                f_ngweight.write(ord(3))



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