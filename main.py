import streamlit as st
import pandas as pd
import get_video_id
import get_viewer_title
import job_schedule
import MySQLdb
import traceback



def main():
    st.title('Youtubeデータ収集')
    text = st.text_input(label='CHANNELIDを入力して下さい', value='id')
    st.write('vide0_id: ', text)
    if(text!='id'):
        get_video_id.get_video_id(text)
        #DB接続
        conn = MySQLdb.connect(
        unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
        user='x19030',
        passwd='hibio511',
        host='localhost',
        db='YT_2021',
        charset='utf8mb4'
        )
        cursor = conn.cursor()

        #videoid抽出
        sql="""SELECT video_id FROM video_id ORDER BY datatime desc LIMIT 1"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            video = row[0]
        videoId = video
        url ='https://www.youtube.com/watch?v=' + videoId
        st.write(url)
        try:
            job_schedule.schedule_job()
        except:
            st.write('# traceback.format_exc()')
            t = traceback.format_exc()
            st.write(t)


if __name__ == '__main__':
    main()
