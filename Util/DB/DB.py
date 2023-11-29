import sqlite3

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
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER
                battlefield_name TEXT
                )''')
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
    c.execute(cmd)
    conn.commit()
    result = c.fetchall()
    return result