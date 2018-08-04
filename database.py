#!/usr/bin/python
import sqlite3
conn=sqlite3.connect("users.db")
cursor=conn.cursor()

#cursor.execute("CREATE TABLE users_in_chat (login text, chat text)")

class DBWorker:
    def __init__(self, *args, **kwargs):
        self.conn=sqlite3.connect("users.db")
        self.cursor=self.conn.cursor()
    def userExists(self,login):
        self.cursor.execute("SELECT * FROM users WHERE login=\""+login+"\"")
        return len(self.cursor.fetchall())>0
    def createUser(self,login,password):
        if(self.userExists(login)):
            return
        self.cursor.execute("INSERT INTO users VALUES (\""+login+"\",\""+password+"\")")
        self.conn.commit()
    def checkAccount(self,login,password):
        #return True
        self.cursor.execute("SELECT * FROM users WHERE login=\""+login+"\"")
        if(not len(self.cursor.fetchall())>0):
            return False
        self.cursor.execute("SELECT * FROM users WHERE login=\""+login+"\"")
        return self.cursor.fetchall()[0][1]==password
    def getChatUsers(self,chat):
        self.cursor.execute("SELECT * FROM users_in_chat WHERE chat=\""+chat+"\"")
        resArr=[]
        for i in self.cursor.fetchall():
            resArr.append(i[0])
        return resArr
    def getUserChats(self,user):
        self.cursor.execute("SELECT * FROM users_in_chat WHERE login=\""+user+"\"")
        resArr=[]
        for i in self.cursor.fetchall():
            resArr.append(i[1])
        return resArr
    def userInChat(self,user,chat):
        self.cursor.execute("SELECT * FROM users_in_chat WHERE (login=\""+user+"\" and chat=\""+chat+"\")")
        return (len(self.cursor.fetchall())>0)
    def addChatUser(self,user,chat):
        if(not self.userInChat(user, chat)):
            self.cursor.execute("INSERT INTO users_in_chat VALUES (\""+user+"\",\""+chat+"\")")
            self.conn.commit()
#'''
#dbw=DBWorker()
#dbw.addChatUser("mdn","c16")
#print(dbw.getChatUsers("c1"))
#print(dbw.getUserChats("mn"))
#print(dbw.userInChat("mn","c3"))
