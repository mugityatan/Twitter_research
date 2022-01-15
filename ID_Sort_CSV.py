#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#CSVを整形して昇順に治すプログラム


import pandas as pd
import csv
import re
import numpy as np #numpyをインポート

TwitterData_ID = []
TwitterData_Day = []
TwitterData_Msg = []

csv_save_WordOrthopaedy = "cash.csv"

with open("hoge.csv","r",encoding="utf-8") as f: #ファイルの読み込み
    #シート全体の読み込み
    reader = csv.reader(f)
    l = [row for row in reader]
    #行での読み込み
    for i, InputData in enumerate(l):
        if 0 != i:
            sentence = re.sub(r'@[0-9a-zA-Z_:]*', "", InputData[2])
            #sentence = re.sub(r'#(\w+)', "", sentence)
            sentence = re.sub(r'(https?)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', "", sentence)
            sentence = re.sub(r',',"",sentence)
            TwitterData_ID.append(InputData[0])
            TwitterData_Day.append(InputData[1])
            TwitterData_Msg.append(sentence)
            #print(i)
        else:
            TwitterData_ID.append(InputData[0])
            TwitterData_Day.append(InputData[1])
            TwitterData_Msg.append(InputData[2])
        #print("i: ",i," name: ", InputData, "name[1]", InputData[0])

with open(csv_save_WordOrthopaedy,"w",encoding="utf-8") as fs:
    for i, data in enumerate(TwitterData_ID):
        #print(i,"ID:", TwitterData_ID[i]," Day:",TwitterData_Day[i], " msg:", TwitterData_Msg[i],"\n")
        msg = TwitterData_ID[i]+"," + TwitterData_Day[i]+"," + TwitterData_Msg[i]+"\n"
        fs.write(msg)


# sample.csvの取り込み
df = pd.read_csv(csv_save_WordOrthopaedy)
# 総合得点を昇順でソートして出力
df = df.sort_values("TweetID")
print(df)
df.to_csv('hoge_output.csv', index=False)