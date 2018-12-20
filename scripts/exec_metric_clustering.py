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
path_indexed_metric_src = r'./../indexed_metric_src/'
num_clusters = 8
num_metric_clusters = 3


def exec_all_metric_clustering(problem_id):
    """
    それぞれのディレクトリに対して以下の処理を行う
    1. ファイル名をリストにする
    2. miningscripts/CodeForceCrawler/resultから、SourceMonitorのメトリクス値を読みこんでくる
    3. pandaのライブラリに読み込んでくる
    4. クラスタリングを実行。fclusterでクラスターのラベリング。
    5. 再コピー。
    """



# コピー先のディレクトリが存在しなければ作成する
def make_directory(problem_id):
    global num_clusters
    metrics = ['cosine']
    methods = ['complete', 'weighted']
    clusters = range(1, num_clusters+1)
    metric_clusters = range(1, num_metric_clusters+1)
    for cluster in clusters:
        for metric_cluster in metric_clusters
            for metric in metrics:
                for method in methods:
                    path_cluster = '%s/%s/%s/%s/%s/%s'% (path_indexed_metric_src, problem_id, metric, method, str(cluster), str(metric_cluster))
                    if not os.path.exists(path_cluster):
                        os.makedirs(path_cluster)

# 対象問題のidの一覧を返す
def get_problems():
    global cur
    # sql = r'SELECT * FROM Problem WHERE competition_id = 733 OR competition_id = 633;';
    sql = r'SELECT * FROM Problem WHERE competition_id = 727;'
    cur.execute(sql)
    return cur.fetchall()

def main():
    problems = get_problems()
    for problem in problems:
        make_directory(problem['problem_id'])
        exec_all_metric_clustering(problem['problem_id'])

if __name__ == '__main__':
    main() 