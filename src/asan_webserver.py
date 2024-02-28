import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3

def load_data(db_path: Path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM asan_logs", conn)
    print(df)
    conn.close()
    return df

def app():
    db_path = Path('database.db')
    df = load_data(db_path)
    
    st.title('Asan Logs')
    st.write(df)
    # 这里可以添加更多的Streamlit组件来实现文件上传、数据编辑等功能

if __name__ == '__main__':
    app()
