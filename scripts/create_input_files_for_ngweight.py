"""
TODO:
ngweightに入力するためのファイルを用意する
「733」「633」の２つで試験する
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq

cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='khkh5813',
    port='3306',
    database='codeforces'
)
cur = cnx.cursor(buffered=True, dictionary=True)


"""
problem_idを引数として、ngweight用の1つの入力ファイルを作成する
"""
def create_an_file_for_ngweight(problem_id):
    


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