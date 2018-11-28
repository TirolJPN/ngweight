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
    database='codeforces')
)
cur = cnx.cursor(buffered=True, dictionary=True)


"""
ngweightに入力するファイルを用意する問題のid一覧を返す
"""
def get_problem_list():



def main():
    

if __name__ == '__main__':
    main()