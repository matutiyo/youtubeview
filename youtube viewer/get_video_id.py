import time
import datetime
import requests
import json
#import schedule
import traceback
import MySQLdb
from apiclient.discovery import build
import streamlit as st

def get_video_id(c_id):
    API_KEY ='AIzaSyBuMihCrrP2p611M1an1FNjNqdSLnTywms'
    CHANNEL_ID = c_id
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    conn = MySQLdb.connect(
    unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
    user='x19030',
    passwd='hibio511',
    host='localhost',
    db='YT_2021',
    charset='utf8'
    )
    cursor = conn.cursor()

    youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=API_KEY
        )

    dtNow = datetime.datetime.now()
    try:
        response = youtube.search().list(
            part = 'id',
            channelId = CHANNEL_ID,
            type = 'video',
            eventType = 'live'
            ).execute()
        for item in response.get("items", []):
            video_id=item['id']['videoId']
            cursor.execute("""
            INSERT INTO video_id 
                (video_id, datatime)
            VALUES 
                ('%s','%s')
            """% (video_id,dtNow))
            # 保存を実行
            conn.commit()
    except:
        st.error('Error message')

    cursor.close
    conn.close

    return video_id
