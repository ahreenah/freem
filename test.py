import sqlite3
conn=sqlite3.connect("users.db")
cursor=conn.cursor()
def userExists(login):
    cursor.execute("SELECT * FROM users WHERE login=\""+login+"\"")
    return len(cursor.fetchall())>0
def createUser(login,password):
    if(userExists(login)):
        return
    cursor.execute("INSERT INTO users VALUES (\""+login+"\",\""+password+"\")")
def checkAccount(login,password):
    if(not userExists(login)):
        return False
    cursor.execute("SELECT * FROM users WHERE login=\""+login+"\"")
    return cursor.fetchall()[0][1]==password

