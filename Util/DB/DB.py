import sqlite3
import traceback

conn = None
c = None

def init():
        global conn, c
        conn = sqlite3.connect('Config/user_info.db',check_same_thread = False)
        c = conn.cursor()
        create_user_table()
        create_BF2042_table()
        
def create_user_table():
    global conn, c
    c.execute('''CREATE TABLE IF NOT EXISTS user
                (uid TEXT PRIMARY KEY,
                bf_name TEXT
                )''')
    conn.commit()

def delete_user_table():
    global conn, c
    c.execute('''DROP TABLE user''')
    conn.commit()

def create_BF2042_table():
    global conn, c
    c.execute('''CREATE TABLE IF NOT EXISTS BF
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                updateTime TEXT,
                name TEXT,
                kill INTEGER,
                deaths INTEGER,
                damage INTEGER)''')
    conn.commit()

def execute(cmd):
    try:
        c.execute(cmd)
        conn.commit()
        result = c.fetchall()
        return result
    except Exception as e:
        s = traceback.format_exc()
        print(e)
        print(s)
        return None