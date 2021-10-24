import schedule
import time
from get_viewer_title import job
import streamlit as st
import MySQLdb
import pandas as pd
import sqlalchemy as sa

def schedule_job():
    schedule.every(1).minutes.do(job)
    b1=st.button('cancel')
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
            if b1:
                st.write('finish')
                break
        except:
            st.write('finish!!!')
            break
    
    url = 'mysql+pymysql://x19030:hibio511@localhost:3306/YT_2021?charset=utf8'
    engine = sa.create_engine(url, echo=False)
    query1 = "select viewer, datatime from YT_2021.live_data where datatime > date_sub(now(), interval 1 hour)"
    df = pd.read_sql(query1,con = engine)
    st.dataframe(df)
            
