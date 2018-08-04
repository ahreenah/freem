from flask import Flask, request, render_template, session
from database import DBWorker
import os
import sqlite3
#db=DBWorker()
app = Flask(__name__)
app.config["SECRET_KEY"]='dygydtyug67fghkagsewGHF'

def chatExists(cid):
    if(not os.path.exists("lastnums/"+cid+".txt")):
        return False
    return True
def createChat(cid):
    if(not chatExists(cid)):
         n=open(os.path.relpath("lasts/"+cid+".txt"),"w")
         n.write(" ")
         n.close()
         n=open(os.path.relpath("lastnums/"+cid+".txt"),"w")
         n.write("1")
         n.close()
createChat("testchreat")
pass
@app.route('/')
def hello():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    print(linf)
    return render_template("main.html",linf=linf)
    return "Welcome to freem, the free mssenger"

@app.route("/register/")
def register():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    return render_template("register.html",linf=linf)

@app.route('/test')
def testdbcnt():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    db=DBWorker()
    return str(db.checkAccount("medvosa","jdkdfg"))
    return 'test'
@app.route("/registered", methods=["GET","POST"])
def registered():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    db=DBWorker()
    if(db.userExists(request.form["login"])):
        return "User already exists"
    if(request.form["login"]=='')or(request.form["password"]==""):
        return "Login or password is empty"
    if(not (request.form["password"]==request.form["password_repeat"])):
        return "Pasword and repeat of the password do not match!!!"
    db.createUser(request.form["login"],request.form["password"])
    return "You have succcessfully registered"
    #("login")
    #return "You are successfully registered"
@app.route("/login")
def login():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    return render_template("login.html",linf=linf)

@app.route('/chat')
def chatlist():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    db=DBWorker()
    if("login" in session):
        str= "chat list ("+session["login"]+"):<br>"
        for i in db.getUserChats(session["login"]):
            str=str+i+"<br>"
        return render_template("chatlist.html",str=db.getUserChats(session["login"]),linf=linf)
    else:
        return "You chould login to use chats"

@app.route("/chat/<cid>")
def viewChat(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    db=DBWorker()
    if(not "login" in session):
        return "You should login to use chats"
    if(not chatExists(cid)):
        return 'Chat does not Exist, but you can <a Href="/createchat/'+cid+'">create</a> it.'
    if(not db.userInChat(session["login"], cid)):
       return "You are not allowed to use this chat"
    return render_template("chat.html", login=session['login'],cid=cid,linf=linf)

@app.route("/createchat/<cid>")
def createChatPage(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    if (not "login" in session):
        return "You should login to create chats"
    if(chatExists(cid)):
        return "Chat already exists"
    createChat(cid)
    db=DBWorker()
    db.addChatUser(session["login"],cid)
    return "Chat was created"

@app.route("/invite/<cid>")
def invite_page(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    return render_template("invite.html",cid=cid,linf=linf)

@app.route("/invited/<cid>", methods=["GET","POST"])
def invitedPage(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    #return "oo"
    #print (request.form["login"])
    #return ""
    db=DBWorker()
    if(not db.userInChat(session["login"],cid)):
        return "you are not allowed to use this chat"
    db.addChatUser(request.form["login"],cid)
    return "inviting "+str(request.form["login"])+" to chat "+str(cid)

@app.route("/lastnum/<cid>")
def lastnum(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    #os.chdir("lastnums")
    n=open(os.path.relpath("lastnums/"+cid+".txt"),"r")
    return n.read()

@app.route("/last/<cid>")
def last(cid):
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    n=open(os.path.relpath("lasts/"+cid+".txt"),"r")
    return n.read()

@app.route("/logout")
def logout():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    if "login" in session:
        session.pop("login")
    return "You have successfully logged out."

@app.route("/loggedin", methods=["GET","POST"])
def loggein():
    if('login' in session):
        linf=session['login']
    else:
        linf='login!'
    db=DBWorker()
    if(not(db.checkAccount(request.form['login'],request.form['password']))):
        return "Wrong login or password"
    else:
        session['login']=request.form['login']
        return "Welcome"

@app.route("/send/<cid>/<text>")
def send(cid,text):
    if('login' in session):
        linf=session['login']
    else:
        linf="login!"
    db=DBWorker()
    if (not "login" in session):
        return "You should login to use chats"
    if (not db.userInChat(session["login"],cid)):
        return "You are not allowed to use this chat"
    n=open(os.path.relpath("lasts/"+cid+".txt"),"w")
    n.write("<b>"+session['login']+"</b>:"+text)
    n.close()
    n=open(os.path.relpath("lastnums/"+cid+".txt"),"r")
    now=int(n.read())
    n.close()
    n=open(os.path.relpath("lastnums/"+cid+".txt"),"w")
    n.write(str((now+1)%10))
    n.close()
    return ""
@app.route('/about')
def about_page():
    if('login' in session):
        linf=session['login']
    else:
        linf="login!"
    return render_template('about.html', linf=linf)
@app.route('/license')
def license_page():
    if('login' in session):
        linf=session['login']
    else:
        linf="login!"
    return render_template('license.html', linf=linf)

if __name__ == '__main__':
    app.run()
