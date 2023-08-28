import streamlit as st
import pandas as pd
import sqlite3 as sqlite

st.title("課題メモアプリ")

#データベースにアクセス
db = sqlite.connect('memo_db')
#データベースにmemo_dbがない場合は作成する
db.execute("CREATE TABLE IF NOT EXISTS memo_db ( id INTEGER PRIMARY KEY, task TEXT NOT NULL, limit_date TEXT NOT NULL)")
db.commit()

#memo_dbからデータを取得
cursor = db.cursor()
cursor.execute("SELECT * FROM memo_db")

list = cursor.fetchall()
tasks = []
limit_dates = []
for item in list:
    tasks.append(item[1])
    limit_dates.append(item[2])

df = pd.DataFrame(data={
    'Task':tasks,
    'Limit':limit_dates
})

st.write('タスク管理表', df)

task = st.text_input('課題')
limit = st.date_input('期限')

if st.button('追加する'):
    if not task:
        st.error('タスクの名前が記入されていません')
    else:
        db.execute(f"""
        INSERT INTO memo_db(task, limit_date) VALUES('{task}', '{limit}')""")
        db.commit()
