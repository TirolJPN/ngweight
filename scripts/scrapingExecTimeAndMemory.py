"""
実行時に引数がproblem_idを表す引数が必要

該当するFileのレコードごとに、URLにアクセスして、memoryとtimeの値をスクレイピングする(それぞれ単位はKB, ms、多分)
スクレイピングしてきたら、verdict, memory timeとして、新テーブルに保存していく
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
import sys
import requests 

class Connector:
    cnx = cn.connect(
    host='127.0.0.1',
    user='kosuke',
    password='localhost',
    port='3306',
    database='codeforces'
    )
    cur = cnx.cursor(buffered=True, dictionary=True)

    key = '56880864c4341b310822d42c5906a7bc2de2b4ef'
    secret = '8450cfaa0bafeafa8659e08f25a91470f86d4dc7'

    
    def execSqlStatement(self, sql):
        Connector.cur.execute(sql)
        return Connector.cur.fetchall()

"""
各problem_id毎にインスタンスを生成する
データ取得までにやること
1. problem_idが妥当か判断
2. submission_idの一覧を取得
3. 各submissionごとにAPIリクエストを送る
4. 新テーブルに取得したデータを格納する
"""
class Problem(Connector):
    # 引数がinvalid(Fileテーブルに解答が存在しなければ何もしない)
    def __init__(self, competition_id):
        self.competition_id = int(competition_id)
        sql = "SELECT count(*) as cnt FROM File WHERE competition_id = %d" %  self.competition_id
        sqlResult = super().execSqlStatement(sql)
        if int(sqlResult[0]['cnt']) != 0:
            self.execAllProcess()

    def execAllProcess(self):
        self.submissionList = self.getSubmissionList()
        self.resultsAPI = self.submitAPIRequest()['result']
        for submission in self.submissionList:
            id = submission['submission_id']
            self.resultsAPI.get('id', id)

    def getValue(key, items):
        values = [x['id'] for x in items if 'Key' in x and 'Value' in x and x['Key'] == key]
        return values[0] if values else None


    def submitAPIRequest(self):
        base_url = 'http://codeforces.com/'
        url = base_url + 'api/'
        api = "contest.status?contestId=%d&from=1" % self.competition_id
        request = requests.get(url+api)
        return request.json()
    
    def getSubmissionList(self):
        sql = "select * from File WHERE competition_id = %d" % self.competition_id
        return super().execSqlStatement(sql)

def main():
    args = sys.argv
    # 引数がなければそのまま終了
    if len(args) != 1:
        # 各引数の文字列ごとにProblemクラスを作成、データ取得とDB保存を実行
        for problem_id in args[1:]:
            problem = Problem(problem_id)


if __name__ == "__main__":
    main()