#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Azure Text analyticsの感情分析を使用するときのスクリプト
# CSVが入力

#引用
#https://docs.microsoft.com/ja-jp/azure/cognitive-services/text-analytics/quickstarts/client-libraries-rest-api?pivots=programming-language-python&tabs=version-3-1#sentiment-analysis

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import csv
import pandas as pd
import time

key = "hoge"
endpoint = "hoge"

#クライアントを認証する
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def sentiment_analysis_example(client,AnalyticsTxt):

    documents = [AnalyticsTxt]
    response = client.analyze_sentiment(documents=documents)[0]
    # print("Document Sentiment: {}".format(response.sentiment))
    # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
    #     response.confidence_scores.positive,
    #     response.confidence_scores.neutral,
    #     response.confidence_scores.negative,
    # ))
    # for idx, sentence in enumerate(response.sentences):
    #     print("Sentence: {}".format(sentence.text))
    #     print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
    #     print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
    #         sentence.confidence_scores.positive,
    #         sentence.confidence_scores.neutral,
    #         sentence.confidence_scores.negative,
    #     ))
    return response.sentiment,response.confidence_scores.positive,response.confidence_scores.neutral,response.confidence_scores.negative

#クライアントを認証する
client = authenticate_client()

print(client)
time.sleep(200)
# データ格納用、配列を用意
TwitterData_ID = []
TwitterData_Day = []
TwitterData_Msg = []
TwitterData_Msg_Sentiment = []
TwitterData_Msg_Sentiment_Score_Positive = []
TwitterData_Msg_Sentiment_Score_Neutral = []
TwitterData_Msg_Sentiment_Score_Negative = []
RequestError = 0

csv_save_filename="hoge.csv"
#読み込む数
analysis_N = 300000000
#飛ばす数（割る数）
analysis_Skip = 1
#最大リクエスト数
analysis_Max = 2000

with open("Azure\Before_Data\e00003KickFlightJP_Sort.csv","r",encoding="utf-8") as f: #ファイルの読み込み
    #シート全体の読み込み
    reader = csv.reader(f)
    l = [row for row in reader]
    #行での読み込み
    for i, InputData in enumerate(l):
        if i<=analysis_N and len(TwitterData_ID) <= analysis_Max:
            if 0 != i:
                if i % analysis_Skip == 0:
                    #例外処理導入
                    try:
                        rt=sentiment_analysis_example(client,InputData[2])
                        TwitterData_ID.append(InputData[0])
                        TwitterData_Day.append(InputData[1])
                        TwitterData_Msg.append(InputData[2])
                        TwitterData_Msg_Sentiment.append(rt[0])
                        TwitterData_Msg_Sentiment_Score_Positive.append(rt[1])
                        TwitterData_Msg_Sentiment_Score_Neutral.append(rt[2])
                        TwitterData_Msg_Sentiment_Score_Negative.append(rt[3])
                        #デバック用
                        DebagCount = int(i/analysis_Skip)
                        msg = TwitterData_ID[DebagCount]+"," + TwitterData_Day[DebagCount]+"," +TwitterData_Msg_Sentiment[DebagCount]+","
                        msg2 = str(TwitterData_Msg_Sentiment_Score_Positive[DebagCount])+"," +str(TwitterData_Msg_Sentiment_Score_Neutral[DebagCount])+","+str(TwitterData_Msg_Sentiment_Score_Negative[DebagCount])+","+TwitterData_Msg[DebagCount]+ "\n"
                        msg = msg + msg2
                        print("i:",i,"\tGetAPISum:",len(TwitterData_ID),msg)
                        time.sleep(100)
                    except:
                        print("Null Data  (RequestError)",RequestError)
                        RequestError += 1
                        time.sleep(100)
                        break

            else:
                TwitterData_ID.append(InputData[0])
                TwitterData_Day.append(InputData[1])
                TwitterData_Msg.append(InputData[2])
                TwitterData_Msg_Sentiment.append("Sentiment")
                TwitterData_Msg_Sentiment_Score_Positive.append("Score_Positive")
                TwitterData_Msg_Sentiment_Score_Neutral.append("Score_Neutral")
                TwitterData_Msg_Sentiment_Score_Negative.append("Score_Negative")
        else:
            break

with open(csv_save_filename,"w",encoding="utf-8") as fs:
    for i, data in enumerate(TwitterData_ID):
        #print(i,"ID:", TwitterData_ID[i]," Day:",TwitterData_Day[i], " msg:", TwitterData_Msg[i],"\n")
        msg = TwitterData_ID[i]+"," + TwitterData_Day[i]+"," +TwitterData_Msg_Sentiment[i]+","
        msg2 = str(TwitterData_Msg_Sentiment_Score_Positive[i])+"," +str(TwitterData_Msg_Sentiment_Score_Neutral[i])+","+str(TwitterData_Msg_Sentiment_Score_Negative[i])+","+TwitterData_Msg[i]+ "\n"
        msg = msg + msg2
        print(msg)
        fs.write(msg)
    
print(pd.read_csv(csv_save_filename))            
print("RequestError",RequestError)