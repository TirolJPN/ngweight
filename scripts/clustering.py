"""
TODO:
結局これはscipy1の実行テスト用のスクリプトということで
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
from enum import  Enum
import re
import subprocess
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
# from pandas.tools import plotting
from pandas.plotting import scatter_matrix

# グローバル変数
cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='khkh5813',
    port='3306',
    database='codeforces'
)
cur = cnx.cursor(buffered=True, dictionary=True)

path_src = r'./../../Database/src_original/src_original/'
path_input_files = r'./../input_files/'
path_output_files = r'./../output_files/'
path_vector_files = r'./../vector_files/'



# problem_idを引数にして、クラスタリングを実行する
# 改善の余地あり
def exec_cluster(problem_id):
    path_csv_file = path_vector_files + problem_id + '.csv'
    df = pd.read_csv(path_csv_file, delimiter=",", )
    # print(df.iloc[:, 1:(len(df.columns) - 1)].head())
    scatter_matrix(df[df.columns[1:(len(df.columns) - 1)]], figsize=(6,6), alpha=0.8, diagonal='kde')
    plt.show()





def get_problem_list():
    global cur
    # sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    sql = r'SELECT * FROM Problem WHERE  competition_id = 633;';
    cur.execute(sql)
    return cur.fetchall()
    

def main():
    problems = get_problem_list()
    # for problem in problems:
    #     exec_cluster(problem['problem_id'])
    exec_cluster("633E")



if __name__ == "__main__":
    main()