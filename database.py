import sqlite3

def con_table(table):
    con = sqlite3.connect('Reddit.db')
    cur = con.cursor()
    if len(cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}'").fetchall()):
        return
    cur.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY AUTOINCREMENT, post_url varchar(50) NOT NULL, post_id varchar(10) NOT NULL, data_url varchar(50) NOT NULL)")
    con.commit()
    con.close()

def insert(table, url, post_id, data_url):
    con = sqlite3.connect('Reddit.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table}(post_url, post_id, data_url) VALUES(?, ?, ?)", (url, post_id, data_url))
    con.commit()
    con.close()

def get_messages(table):
    con = sqlite3.connect('Reddit.db')
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table}")
    messages = cur.fetchall()
    con.close()
    return messages

def show_messages(table):
    messages = get_messages(table)
    for message in messages:
        print(message)

def save_message(table):
    messages = get_messages(table)
    print(messages)

if __name__ == "__main__":
    show_messages("memes")