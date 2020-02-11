import sqlite3
import os.path
import os
import sys


def initialDatabase():
    if os.path.exists('databases/projects.db') is False:
        conn = sqlite3.connect('databases/projects')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE projects
                          (id INTEGER PRIMARY KEY, name TEXT, host TEXT, folder TEXT,
                          www_folder TEXT, port TEXT, status INTEGER)
                       """)
        conn.close()
        return
    else:
        return True


def getDatabase():
    if os.path.exists('databases/projects.db') is True:
        conn = sqlite3.connect('databases/projects.db')
        cursor = conn.cursor()
        data = cursor.execute("""SELECT * FROM projects""")
        rows = data.fetchall()
        conn.close()
        return rows
    else:
        initialDatabase()


def addData(name, host_name, folder, www_folder, a2_conf, port, status):
    conn = sqlite3.connect('databases/projects.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO projects (name,host_name,folder,www_folder,a2_conf,port,status) VALUES (?,?,?,?,?,
    ?,?);""", [name, host_name, folder, www_folder, a2_conf, port, status])
    conn.commit()
    conn.close()
    return

def getProject(name):
    conn = sqlite3.connect('databases/projects.db')
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM projects WHERE name = ?""", [name])
    rows = data.fetchall()
    conn.close()
    return rows