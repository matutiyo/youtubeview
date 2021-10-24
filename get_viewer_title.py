import datetime
import requests
import json
import MySQLdb
import streamlit as st
import pandas as pd
import traceback


def get_currentViewers(yt_url,videoId):
    #API_KEY
    API_KEY ='AIzaSyBuMihCrrP2p611M1an1FNjNqdSLnTywms'

    #DB接続
    conn = MySQLdb.connect(
    unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
    user='x19030',
    passwd='hibio511',
    host='localhost',
    db='YT_2021',
    charset='utf8'
    )
    cursor = conn.cursor()

    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': API_KEY, 'id': videoId, 'part': 'liveStreamingDetails,snippet'}
    data   = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    countViewers = liveStreamingDetails['concurrentViewers']
    item = data['items'][0]['snippet']
    video_title=item['title']

    dtNow = datetime.datetime.now()
    #print(dumpYMD,",",dumpTimes,",",countViewers,",",video_title)

    try:
        # テーブルの作成
        cursor.execute("""
        INSERT INTO live_data 
            (video_id, title, viewer, datatime)
        VALUES 
            ('%s','%s','%s','%s')
        """% (videoId,video_title,countViewers,dtNow))
        # 保存を実行
        conn.commit()
    except:
        st.write('# traceback.format_exc()')
        t = traceback.format_exc()
        st.write(t)

    cursor.close
    conn.close

def job():
    #DB接続
    conn = MySQLdb.connect(
    unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
    user='x19030',
    passwd='hibio511',
    host='localhost',
    db='YT_2021',
    charset='utf8'
    )
    cursor = conn.cursor()

    #videoid抽出
    sql="""SELECT video_id FROM video_id ORDER BY datatime desc LIMIT 1"""
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        video = row[0]
    videoId = video
    
    yt_live_url='https://www.youtube.com/watch?v=' + videoId
    get_currentViewers(yt_live_url,videoId)
        

    cursor.close
    conn.close