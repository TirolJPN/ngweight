"""
TODO:
問題ごとに階層クラスタリングをlinkage()で実行。
fcluster()でクたスター番号の索引付けを行う。
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
num_clusters = 8



def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


# problem_idを引数にして、クラスタリングを実行する
# 改善の余地あり
def exec_cluster(problem_id):
    global num_clusters

    metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
    normal_methods = ['single', 'average', 'complete', 'weighted']
    euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

    path_csv_file = path_vector_files + problem_id + '.csv'
    df = pd.read_csv(path_csv_file, delimiter=",", )
    length_culumns = len(df.columns)
    x = df.iloc[:,1:length_culumns]

    # print('num of % nodes : %' % (problem_id ,str(length_culumns)) )
    # scatter_matrix(df[df.columns[1:length_culumns]], figsize=(6,6), alpha=0.8, diagonal='kde')
    # クラスタリング結果にかなり偏りがある
    # 全パターンで試す
    
    for metric in metrics:
        if metric != 'euclidean':
            methods = normal_methods
        else:
            methods = euclidean_methods
        for method in methods:
            
            '''
            階層クラスタリングを行い、プロット
            reference: https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
            '''
            result = linkage(x,
                            metric = metric,
                            method = method)
            # dendrogram(result)
            fancy_dendrogram(
                result,
                truncate_mode='lastp',  # show only the last p merged clusters
                p=20,  # show only the last p merged clusters
                leaf_rotation=90.,
                leaf_font_size=12.,
                show_contracted=True,  # to get a distribution impression in truncated branches
                annotate_above=10,  # useful in small plots so annotations don't overlap
            )
            # fcluster()で、クラスタ数指定でクラスタ分類する
            cluster_index = fcluster(result, num_clusters, criterion='maxclust')
            print(cluster_index)
            plt.title("Dedrogram")
            plt.ylabel("Threshold")
            plot_file_name = '%s%s/%s/%s.png' % (path_plot_results, metric, method, problem_id)
            plt.savefig(plot_file_name, dpi = 1000)
            plt.clf()
            
            path_cluster_index = '%s%s/%s/%s.npy' % (path_plot_results, metric, method, problem_id)
            np.save(path_cluster_index, cluster_index)

def make_directories():
    # デンドログラムの結果を保存するディレクトリの作成
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
    # sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    sql = r'SELECT * FROM Problem WHERE  competition_id = 727;'
    cur.execute(sql)
    return cur.fetchall()
    

def main():
    make_directories()
    problems = get_problem_list()
    for problem in problems:
        exec_cluster(problem['problem_id'])



if __name__ == "__main__":
    main()