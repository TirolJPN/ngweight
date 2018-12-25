"""
各ディレクトリ毎にスクリプトを実行、copyを行う
やること
各ディレクトリ：ある問題のあるmetricのあるmethodでクラスタリングされた1つのクラスター。
              分類された問題の一覧がある

それぞれのディレクトリに対して以下の処理を行う
1. ファイル名をリストにする
2. miningscripts/CodeForceCrawler/resultから、SourceMonitorのメトリクス値を読みこんでくる
3. pandaのライブラリに読み込んでくる
4. クラスタリングを実行。fclusterでクラスターのラベリング。
5. 再コピー。

4, 5はリファクタリングの時点で一緒にする(？)
各出力のディレクトリの流れを確認する。
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
import glob

# グローバル変数
cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='khkh5813',
    port='3306',
    database='codeforces'
)
cur = cnx.cursor(buffered=True, dictionary=True)

# path_src = r'./../../Database/src_original/src_original/'
# path_vector_files = r'./../vector_files/'
# path_plot_results = r'./../plot_results/'
# path_indexed_src = r'./../indexed_src/'
# path_indexed_metric_src = r'./../indexed_metric_src/'
# path_metric_values = r'./../../miningscripts/CodeForceCrawler/result/'


# 633を分類する
path_src = r'./../../Database/src_original/src_original/'
path_vector_files = r'./../../ngweight_12_19_outputs/vector_files/'
path_plot_results = r'./../../ngweight_12_19_outputs/plot_results/'
path_indexed_src = r'./../../ngweight_12_19_outputs/indexed_src/'
path_indexed_metric_src = r'./../../ngweight_12_19_outputs/indexed_metric_src/'
path_metric_values = r'./../../miningscripts/CodeForcesCrawler/result/'
num_clusters = 8
num_metric_clusters = 3




def get_fcluster_result(df, metric, method, cluster, problem_id):
    global num_metric_clusters
    length_culumns = len(df.columns)
    x = df.iloc[:,1:length_culumns]
    print(x)
    if len(df) >= 2:
        result = linkage(x,
                    metric = metric,
                    method = method)
        dendrogram(
                    result,
                    truncate_mode='lastp',  # show only the last p merged clusters
                    p=20,  # show only the last p merged clusters
                    leaf_rotation=90.,
                    leaf_font_size=12.,
                    show_contracted=True,  # to get a distribution impression in truncated branches
                )
        cluster_index = fcluster(result, num_metric_clusters, criterion='maxclust')
        print(cluster_index)
        plt.title("Dedrogram")
        plt.ylabel("Threshold")
        plot_file_name = '%s%s/%s/%s/%s/cluster.png' %(path_indexed_metric_src, problem_id, metric, method, str(cluster))
        plt.savefig(plot_file_name, dpi = 1000)
        plt.clf()
        
        return cluster_index
    else:
        return [1]




def exec_copy(src_list, label, metric, method, num_cluster, problem_id):
    index = 0
    for src_name in src_list:
        path_src_file = '%s%s' % (path_src, src_name)
        if os.path.exists(path_src_file):
            path_copy_src_file = '%s/%s/%s/%s/%s/%s/%s' % (path_indexed_metric_src, problem_id, metric, method, num_cluster ,  label[index], src_name)
            shutil.copy(path_src_file, path_copy_src_file)
            index = index + 1


def exec_all_metric_clustering(problem_id):
    """
    それぞれのディレクトリに対して以下の処理を行う
    1. ファイル名をリストにする
    2. miningscripts/CodeForceCrawler/resultから、SourceMonitorのメトリクス値を読みこんでくる
    3. pandaのライブラリに読み込んでくる
    4. クラスタリングを実行。fclusterでクラスターのラベリング。
    5. 再コピー。
    """
    global num_clusters
    global num_metric_clusters
    metrics = ['cosine']
    methods = ['complete', 'weighted']
    clusters = range(1, num_clusters+1)
    metric_clusters = range(1, num_metric_clusters+1)
    # メトリックスで未分類の問題について
    for metric in metrics:
        for method in methods:
            for num_cluster in clusters:
                # そのディレクトリに存在するファイル名の一覧を取得する
                # 現在のループでフォルダが存在すれば
                path_cluster = '%s%s/%s/%s/%s/'% (path_indexed_src, problem_id, metric, method, str(num_cluster))
                if os.path.exists(path_cluster):
                    print(path_cluster)
                    path_cluster = '%s%s/%s/%s/%s/*'% (path_indexed_src, problem_id, metric, method, str(num_cluster))
                    src_list = [os.path.basename(r) for r in glob.glob(path_cluster)]
                    print(len(src_list))
                    print(src_list)
                    # src_listに存在するcsvの行だけ、dfに入れる
                    path_metric_csv = '%s%s.csv' % (path_metric_values, problem_id)

                    # 探索対象のdfをこれに追加していく
                    data_frame = pd.DataFrame(index=[], columns=['file_name', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M9', 'M11', 'M12', 'M13', 'M14'])
                    # series = pd.Series(['hoge', 'fuga'], index=data_frame.columns)
                    
                    # for i in range(5):
                    # data_frame = data_frame.append(series, ignore_index = True)

                    with open(path_metric_csv, "r", encoding="utf-8") as csv_file:
                        f = csv.reader(csv_file, delimiter=",",  lineterminator='\n')
                        next(f)
                        for csv_row in f:
                            tmp_file_name = '%s_%s_%s.src' % (csv_row[0], csv_row[1], csv_row[2])
                            # ディレクトリに注目している行のファイルが存在すれば
                            # print(tmp_file_name)
                            if tmp_file_name in src_list:
                                # 全要素が0だと類似度が計算できないので除外する
                                print([csv_row[3], csv_row[4], csv_row[5], csv_row[6], csv_row[7], csv_row[8], csv_row[9], csv_row[12], csv_row[14], csv_row[15], csv_row[16], csv_row[17]])
                                if not all(str(int(float(elem))) == '0' for elem in [csv_row[3], csv_row[4], csv_row[5], csv_row[6], csv_row[7], csv_row[8], csv_row[9], csv_row[12], csv_row[14], csv_row[15], csv_row[16], csv_row[17]]):
                                    metric_list = [tmp_file_name, csv_row[3], csv_row[4], csv_row[5], csv_row[6], csv_row[7], csv_row[8], csv_row[9], csv_row[12], csv_row[14], csv_row[15], csv_row[16], csv_row[17]]
                                    series = pd.Series(metric_list, index=data_frame.columns)
                                    data_frame = data_frame.append(series, ignore_index = True)
                                else:
                                    src_list.remove(tmp_file_name)
                    # クラスタリングの結果のラベルが帰ってくる
                    # exec_clustering()と同様にコピーを実行する
                    # ex. label が[1,2,3,2,1,2], src_listが['aaaa.src', 'hoge.src'. 'fuga.src']みたいな形なので、順序が同じことを前提にコピー
                    # print(data_frame)
                    label = get_fcluster_result(data_frame, metric, method, num_cluster, problem_id)
                    exec_copy(src_list, label, metric, method, num_cluster, problem_id)
                    print('-----------------------------------------------------------')
                        







# コピー先のディレクトリが存在しなければ作成する
# 最終的な結果はpath_indexed_metric_src先にコピーする
def make_directory(problem_id):
    global num_clusters
    metrics = ['cosine']
    methods = ['complete', 'weighted']
    clusters = range(1, num_clusters+1)
    metric_clusters = range(1, num_metric_clusters+1)
    for cluster in clusters:
        for metric_cluster in metric_clusters:
            for metric in metrics:
                for method in methods:
                    path_cluster = '%s%s/%s/%s/%s/%s'% (path_indexed_metric_src, problem_id, metric, method, str(cluster), str(metric_cluster))
                    if not os.path.exists(path_cluster):
                        os.makedirs(path_cluster)

    
# 対象問題のidの一覧を返す
def get_problems():
    global cur
    # sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    sql = r'SELECT * FROM Problem WHERE competition_id = 633;'
    cur.execute(sql)
    return cur.fetchall()

def main():
    problems = get_problems()
    for problem in problems:
        print(problem['problem_id'])
        make_directory(problem['problem_id'])
        exec_all_metric_clustering(problem['problem_id'])

if __name__ == '__main__':
    main() 