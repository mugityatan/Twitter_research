#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import config
from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys
import pprint
import time
import re
import sys
import os
# 他のライブラリーを使用
# https://gist.github.com/yume-yu/f7e10723ea6c530e0f14a9ff7362fbd2
from get_tweets import tweet 

###詳細検索（コメントに基づく解析）
class Twitter_Standard_Search:
    def __init__(self,TwitterID,TwitterHashTag):
        self.TwitterID=TwitterID
        self.TwitterHashTag = TwitterHashTag
        self.__str__()
        self.preparation()
        self.Search()
    
    def __str__(self):
        print("TwitterID : "+self.TwitterID+" --- HashTag : "+self.TwitterHashTag)

    def preparation(self):
        #下準備----------------------------------------------------------------------------------------------------------------------
        EXCLUDE_RT = "exclude:retweets"
        AT_USER = "to:"+self.TwitterID
        # q = id+" OR "+hashTag    #検索キーワード　「OR」で追加
        self.q= " ".join([self.TwitterHashTag, EXCLUDE_RT])
        print("query : "+self.q)
        #時間を修正、表示
        self.JST = datetime.timezone(datetime.timedelta(hours=9))
        self.TWEET_DATETIME_FORMAT = "%a %b %d %H:%M:%S %z %Y"

        #保存先を設定（絶対パスではないので注意）
        self.mainWriteFile= "data/AnalysisDate/main/" + self.TwitterID + datetime.datetime.now().strftime('Day%Y-%m-%d_Time%H_%M_%S') + ".csv"
        self.textOnlyWriteFile="data/AnalysisDate/textOnly/" + self.TwitterID + datetime.datetime.now().strftime('Day%Y-%m-%d_Time%H_%M_%S') + ".txt"
    
    def Search(self):
        #API収集開始--------------------------------------------------------------------------------------------------------------------

        
        with open(self.mainWriteFile,"w",encoding="UTF-8") as mf:
            with open(self.textOnlyWriteFile,"w",encoding="UTF-8") as tof:
                msg="TweetID,Day_Time,Msg"+datetime.datetime.now().strftime(('%Y年%m月%d日 %H:%M:%S'))+"\n"
                mf.write(msg)

                # Tweet取得オブジェクトの初期化
                t = tweet.Tweet()
                # 取得オブジェクトの初期化
                max_id = None
                loop_flag = True
                is_retweet = re.compile("^RT ")
                

                while loop_flag:
                    # 指定されたクエリで検索する
                    tweets = t.search_tweet(keyword=self.q, max_id=max_id)

                    
                    if len(tweets) < 100:
                        # 取得結果が0のとき、プログラムを終了する
                        loop_flag = False
                    else:
                        # 0でなければ、最古のツイートのidを控える
                        max_id = tweets[-1].get("id")
                        print(max_id)

                    for _tweet in tweets:
                        # pprint(tweet) <- ツイート1件に含まれる情報を全部見たい時はこれを実行する
                        if re.match(is_retweet, _tweet.get("text")):
                            continue
                        elif _tweet.get("user").get("screen_name") == id:
                            continue
                        msg=",".join([str(_tweet.get("id")),datetime.datetime.strptime(_tweet.get("created_at"), self.TWEET_DATETIME_FORMAT).astimezone(self.JST).strftime("%Y-%m-%d %H:%M:%S"),_tweet.get("text").replace('\n',''),"\n"])
                        # print(msg)
                        mf.write(msg)
                        msg=_tweet.get("text").replace('\n','')+"\n"
                        tof.write(msg)
                    print(tweets[-1].get("created_at"))

# メンション＋ハッシュタグ　ハッシュタグが複数ある場合は[ OR #hoge2]の形でつなぐ
Twitter_Standard_Search("hoge","#hoge")

