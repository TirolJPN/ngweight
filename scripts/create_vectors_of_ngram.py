"""
TODO:
ngweightでで作成した特徴語のリストから、そのN-gramの種類の数だけの次元の特徴ベクトルを
決まったフォーマットで作成する。
クラスタリング・可視化は別のスクリプトで行う。
pythonにおける階層クラスタリングは次を参照 https://qiita.com/suecharo/items/20bad5f0bb2079257568
問題の種類によっては次元数がアホみたいなことになるが、気にしないでとりあえず実行する
クラスタリング手法には最長距離法、メトリクスにはコサイン類似度(コサイン距離？)を用いる
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

