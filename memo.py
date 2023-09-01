import streamlit as st
import pandas as pd
import sqlite3 as sqlite







def main():
    # Streamlit API の title を使用して文字表示
    st.title("課題メモアプリ")

    #データベースにアクセス
    db = sqlite.connect('memo_db')
    #データベースにmemo_dbがない場合は作成する
    db.execute("CREATE TABLE IF NOT EXISTS memo_db ( id INTEGER PRIMARY KEY, task TEXT NOT NULL, limit_date TEXT NOT NULL)")

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

    st.session_state["task"] = task
    st.session_state["limit"] = limit

    #タスクを表に追加する関数
    def addTaskToDatabase():
        print("addTaskToDatabase:Call")
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
        print("deleteTask:Call")
        db = sqlite.connect('memo_db')
        cursor = db.cursor()
        cursor.execute("DELETE FROM memo_db")
        db.commit()

    st.button("表の削除", on_click=deleteTask)


if __name__ == '__main__':
  main()
    

# def main():
#     # セッション変数が存在しないときは初期化する
#     # ここでは 'counter' というセッション変数を作っている
#     if 'counter' not in st.session_state:
#         st.session_state['counter'] = 0

#     # セッション変数の状態を表示する
#     msg = f"Counter value: {st.session_state['counter']}"
#     st.write(msg)

#     # ボタンが押されたときに発火するコールバック
#     def plus_one_clicks():
#         print("call")
#         # ボタンが押されたらセッション変数の値を増やす
#         st.session_state['counter'] += 1
#     # ボタンを作成するときにコールバックを登録しておく
#     st.button(label='+1',
#               on_click=plus_one_clicks)

#     # ボタンが押されたらセッション変数の値を減らすバージョン
#     def minus_one_clicks():
#         print("call")
#         st.session_state['counter'] -= 1
#     st.button(label='-1',
        
#               on_click=minus_one_clicks)

#     # セッション変数の値をリセットするボタン
#     def reset_clicks():
#         st.session_state['counter'] = 0
#     st.button(label='Reset',
#               on_click=reset_clicks)


# if __name__ == '__main__':
#     main()