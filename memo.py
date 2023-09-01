import streamlit as st
import pandas as pd
import sqlite3 as sqlite
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def main():
    # Streamlit API の title を使用して文字表示
    #データベースにアクセス
    db = sqlite.connect('memo_db')
    #データベースにmemo_dbがない場合は作成する
    db.execute("CREATE TABLE IF NOT EXISTS memo_db ( id INTEGER PRIMARY KEY, task TEXT NOT NULL, limit_date TEXT NOT NULL)")

    #memo_dbからデータを取得
    cursor = db.cursor()
    cursor.execute("SELECT * FROM memo_db")

    list = cursor.fetchall()
    ids = []
    tasks = []
    limit_dates = []
    for item in list:
        ids.append(item[0])
        tasks.append(item[1])
        limit_dates.append(item[2])

    df = pd.DataFrame(data={
        'ID':ids,
        'TASK':tasks,
        'LIMIT':limit_dates
    })

    st.subheader('タスク管理表')
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    gridTable = AgGrid(df, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)
    st.session_state["selected_rows"] = gridTable.selected_rows

    task = st.text_input('課題')
    limit = st.date_input('期限')

    st.session_state["task"] = task
    st.session_state["limit"] = limit

    #タスクを表に追加する関数
    def addTaskToDatabase():
        task = st.session_state["task"]
        limit = st.session_state["limit"]
        if not task:
            st.error('タスクの名前が記入されていません')
        else:
            db = sqlite.connect('memo_db')
            cursor = db.cursor()
            cursor.execute(f"""
                INSERT INTO memo_db(task, limit_date) VALUES('{task}', '{limit}')""")
            db.commit()

    st.button('追加する', on_click=addTaskToDatabase)

    #表のデータをすべて削除する関数
    def deleteTask():
        db = sqlite.connect('memo_db')
        cursor = db.cursor()
        cursor.execute("DELETE FROM memo_db")
        db.commit()

    st.button("表の削除", on_click=deleteTask)

    def deleteSelectedTask():
        db = sqlite.connect('memo_db')
        cursor = db.cursor()
        selected_rows = st.session_state["selected_rows"]
        for row in selected_rows:
            id = row["ID"]
            cursor.execute(f"DELETE FROM memo_db WHERE id == '{id}'")
            db.commit()
            
    st.button("選択したタスクの削除", on_click=deleteSelectedTask)

if __name__ == '__main__':
  st.set_page_config(page_title="テスト結果", layout="wide")
  main()
