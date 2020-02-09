import sqlite3
import os.path
import os
import sys


def initialDatabase():
    if os.path.exists('databases/projects') is False:
        conn = sqlite3.connect('databases/projects')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE projects
                          (id INTEGER PRIMARY KEY, name varchar(255), host varchar(255), folder varchar(255),
                          www_folder varchar(255), port varchar(255), status INTEGER)
                       """)
    else:
        return True

def getDatabase():
    if os.path.exists('databases/projects') is True:
        conn = sqlite3.connect("databases/projects")
        cursor = conn.cursor()
        data = cursor.execute("""SELECT * FROM projects""")
        return data
    else:
        initialDatabase()

def addData():
    conn = sqlite3.connect('databases/projects')
    cursor = conn.cursor()
    add = cursor.execute("""INSERT INTO projects(id,name,host_name,folder,www_folder,a2_conf,port,status) VALUES (2,'test1','rest1.local','testtses','fold','conf',80,1);""")
    print(add)