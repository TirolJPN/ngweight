"""
TODO:

"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
from enum import  Enum
import re
import subprocess
import sys
import csv

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