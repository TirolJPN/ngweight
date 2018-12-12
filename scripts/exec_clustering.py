"""
TODO:
階層クラスタリングまで実行して、保存する
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
sys.setrecursionlimit(100000)
# from pandas.tools import plotting
from pandas.plotting import scatter_matrix
from scipy.cluster.hierarchy import linkage, dendrogram

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
path_plot_results = r'./../plot_results/'



# problem_idを引数にして、クラスタリングを実行する
# 改善の余地あり
def exec_cluster(problem_id):
    path_csv_file = path_vector_files + problem_id + '.csv'
    df = pd.read_csv(path_csv_file, delimiter=",", )
    length_culumns = len(df.columns)
    # print('num of % nodes : %' % (problem_id ,str(length_culumns)) )
    # scatter_matrix(df[df.columns[1:length_culumns]], figsize=(6,6), alpha=0.8, diagonal='kde')
    # クラスタリング結果にかなり偏りがある
    # 全パターンで試す



    metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
    normal_methods = ['single', 'average', 'complete', 'weighted']
    euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']
    
    for metric in metrics:
        if metric != 'euclidean':
            methods = normal_methods
        else:
            methods = euclidean_methods
        for method in methods:
            # 階層クラスタリングを行い、プロット
            result = linkage(df.iloc[:,1:length_culumns],
                            metric = metric,
                            method = method)
            dendrogram(result)
            plt.title("Dedrogram")
            plt.ylabel("Threshold")

            # plot_file_name = path_plot_results + problem_id + '.png'
            plot_file_name = '%s%s/%s/%s.png' % (path_plot_results, metric, method, problem_id)
            plt.savefig(plot_file_name, dpi = 300)
            plt.clf()



def make_directories():
    metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
    normal_methods = ['single', 'average', 'complete', 'weighted']
    euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']
    for metric in metrics:
        if metric != 'euclidean':
            methods = normal_methods
        else:
            methods = euclidean_methods
        for method in methods:
            plot_file_name = '%s%s/%s/' % (path_plot_results, metric, method)
            if not os.path.exists(plot_file_name):
                os.makedirs(plot_file_name)


def get_problem_list():
    global cur
    sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    # sql = r'SELECT * FROM Problem WHERE  competition_id = 633;';
    cur.execute(sql)
    return cur.fetchall()
    

def main():
    make_directories()
    problems = get_problem_list()
    for problem in problems:
        exec_cluster(problem['problem_id'])



if __name__ == "__main__":
    main()