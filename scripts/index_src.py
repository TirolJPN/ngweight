"""
TODO:
クラスタリング結果が保存されているndarrayの結果を参照して、
各クラスタのインデックスごとにディレクトリを作成、該当srcファイルをコピーする
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
import copy
import matplotlib.pyplot as plt
import sys
from pandas.plotting import scatter_matrix
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
from scipy.cluster.hierarchy import fcluster
import shutil


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
path_vector_files = r'./../vector_files/'
path_plot_results = r'./../plot_results/'
path_indexed_src = r'./../indexed_src/'
num_clusters = 8




def exec_copy(problem_id, src_name, metric, method, tmp_index):
    path_src_file = '%s%s' % (path_src, src_name)
    if os.path.exists(path_src_file):
        path_copy_src_file = '%s/%s/%s/%s/%s/%s' % (path_indexed_src, problem_id, metric, method, tmp_index, src_name)
        shutil.copy(path_src_file, path_copy_src_file)


# 問題idを引数にして、オリジナルのソースコードをクラスタのインデックスのディレクトリごとにコピーする
def copy_src(problem_id):
    metrics = ['cosine']
    methods = ['complete', 'weighted']

    # csvを読み込んできて、ファイル名の一覧を取得する
    # それぞれの行(解答)毎にforループを回して、ndarrayのインデックス値と照合する
    path_csv = '%s%s.csv' % (path_vector_files, problem_id)
    with open(path_csv, "r", encoding="utf-8") as csv_file:
        f = csv.reader(csv_file, delimiter=",",  lineterminator='\n')
        header = next(f)
        row_count = 0
        for row in f:
            src_name = row[0]
            for metric in metrics:
                for method in methods:
                    path_ndarray =  '%s%s/%s/%s.npy' % (path_plot_results, metric, method, problem_id)
                    indexs = np.load(path_ndarray)
                    tmp_index = indexs[row_count]
                    exec_copy(problem_id, src_name, metric, method, tmp_index)
            row_count += 1



# 対象問題のidの一覧を返す
def get_problems():
    global cur
    # sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    sql = r'SELECT * FROM Problem WHERE competition_id = 727;'
    cur.execute(sql)
    return cur.fetchall()

# コピー先のディレクトリが存在しなければ作成する
def make_directory(problem_id):
    global num_clusters
    metrics = ['cosine']
    methods = ['complete', 'weighted']
    clusters = range(1, num_clusters+1)
    for cluster in clusters:
        for metric in metrics:
            for method in methods:
                path_cluster = '%s/%s/%s/%s/%s'% (path_indexed_src, problem_id, metric, method, str(cluster))
                if not os.path.exists(path_cluster):
                    os.makedirs(path_cluster)

def main():
    problems = get_problems()
    for problem in problems:
        make_directory(problem["problem_id"])
        copy_src(problem["problem_id"])

if __name__ == '__main__':
    main()
