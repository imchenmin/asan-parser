import tarfile
from pathlib import Path
import schedule
import time
import sqlite3

def check_and_extract_tar_files(upload_folder: Path, extracted_folder: Path):
    for tar_file in upload_folder.glob('*.tar.gz'):
        with tarfile.open(tar_file, 'r:gz') as tar:
            tar.extractall(path=extracted_folder)
        # 处理完成后，可以选择移动或删除tar文件
        tar_file.unlink()  # 小心使用，这会删除文件

# 设定定时任务
def job():
    upload_folder = Path('.')
    extracted_folder = Path('extracted')
    insert_log_entry('database.db',parse_asan_log(extracted_folder / 'asan.0'))
    # check_and_extract_tar_files(upload_folder, extracted_folder)

def parse_asan_log(log_file: Path):
    with open(log_file, 'r') as file:
        lines = file.readlines()
        # 根据实际日志格式解析日志
        # 这里假设每个日志项包含datetime, code_location, memory_leak_type等
        parsed_data = {
            'datetime': '2024-02-28',
            'code_location': 'main.c:42',
            'memory_leak_type': 'use-after-free',
            # 其他所需字段
        }
    return parsed_data


def create_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 创建表
    c.execute('''CREATE TABLE IF NOT EXISTS asan_logs
                 (datetime TEXT, code_location TEXT, memory_leak_type TEXT, ip TEXT)''')
    conn.commit()
    conn.close()

def insert_log_entry(db_path: Path, log_entry):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO asan_logs VALUES (?,?,?,?)", 
              (log_entry['datetime'], log_entry['code_location'], log_entry['memory_leak_type'], 'IP_PLACEHOLDER'))
    conn.commit()
    conn.close()

create_db('database.db')
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


