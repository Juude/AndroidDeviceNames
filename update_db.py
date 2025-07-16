import csv
import sqlite3

csv_file = 'supported_devices (3).csv'
db_file = 'database/android-devices.db'

conn = sqlite3.connect(db_file)
cur = conn.cursor()

# 创建表（如果不存在）
cur.execute('''
CREATE TABLE IF NOT EXISTS devices (
    _id INTEGER PRIMARY KEY,
    name TEXT,
    codename TEXT,
    model TEXT
)
''')

# 尝试多种编码打开文件
encodings = ['utf-8-sig', 'utf-16', 'gbk']
for enc in encodings:
    try:
        with open(csv_file, newline='', encoding=enc) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "Brand":
                    continue
                name = row[1]
                codename = row[2]
                model = row[3]
                cur.execute(
                    'INSERT INTO devices (name, codename, model) VALUES (?, ?, ?)',
                    (name, codename, model)
                )
        break
    except UnicodeDecodeError:
        continue

conn.commit()
conn.close()