import socket
import json
import hashlib 
from tkinter import * 
from lib.support import *
from datetime import datetime
from threading import Thread
import time

class ServerApp:
    def __init__(self, port=4000, listen_count=10):
        self.port = port
        self.listen_count = listen_count
        self.window = Tk()
        self.appSize = '600x400'
        self.window.geometry(self.appSize)
        self.window.resizable(width=False, height=False)
        self.hideImage = PhotoImage(file='src/img/eye-icon.png').subsample(6,6)
        self.title = 'Server'
       
    def writeJson(self, data, filename): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 

    def isUserExist(self, inputUser, users):
        usernames = []        
        for user in users: 
            usernames.append(user['username'])        
        if inputUser in usernames:
            return True
        else:
            return False

    def compareUsernamePassword(self, username, password, users):        
        usernames = []
        passwords = []        
        for user in users: 
            usernames.append(user['username']) 
            passwords.append(user['password'])

        index = usernames.index(username)

        if passwords[index] == password:
            return True
        else:
            return False

    def getUserPassword(self,username, users):
        usernames = []
        passwords = []        
        for user in users: 
            usernames.append(user['username']) 
            passwords.append(user['password'])

        index = usernames.index(username)
        return passwords[index]


    def login(self,data, client_sock):        
        user = data['user']
        username = user['username']        
        fileName = 'db/users.json' 

        with open(fileName, 'r') as json_file: 
            users = json.load(json_file) 

        if self.isUserExist(username,users['users']):
            self.tempT = datetime.timestamp(datetime.now())  
            self.tempStartTime = time.time()               
            print(self.tempT)      
            sault = encodeText(self.tempT)            
            client_sock.sendall(bytes(sault , encoding="utf-8"))
            
        else:
            client_sock.sendall(bytes('User does not exist!', encoding="utf-8"))        
            
    def auth(self,data, client_sock):
        self.tempEndTime = time.time()
        if (self.tempEndTime - self.tempStartTime) > 60:
            client_sock.sendall(bytes('Time is over!' , encoding="utf-8"))
            return            
        user = data['user']
        username = user['username']   
        userSault = user['sault']     
        fileName = 'db/users.json' 
        with open(fileName, 'r') as json_file: 
            users = json.load(json_file) 
        password = self.getUserPassword(username, users['users'])
        server_sault = encodeText(self.tempT)
        result = encodeText(password+server_sault)

        if result == userSault:                      
            client_sock.sendall(bytes('Success' , encoding="utf-8"))            
        else:
            client_sock.sendall(bytes('Incorrect password' , encoding="utf-8"))    


    def changePasswordVisibility(self, passwordField):        
        state = passwordField[0].cget("show")
        for etry in passwordField:
            if state == '':
                etry.config(show="*")
            else:
                etry.config(show="")

    def registration(self,data):
        user = data['user'] 
        username = user['username']   
        fileName = 'db/users.json'

        with open(fileName, 'r') as json_file: 
            users = json.load(json_file) 

        if self.isUserExist(username,users['users']):
            return 'User is already exist!'
        else:
            with open(fileName) as json_file: 
                d = json.load(json_file)
                temp = d['users']
                temp.append(user)
            self.writeJson(d,fileName) 
            return "User is added!"    
            
        
    def chooseRoute(self,client_sock):    
        request = client_sock.recv(1024)
        if not request:            
            return    
        decodedJson  = json.loads(request.decode('utf-8')) 
        # print(f'Request:\n{decodedJson}\n--------------------------------------------------------')       
        route = decodedJson['route']   
        method = f'self.{route}'           
        eval(method)(decodedJson,client_sock)  
        # print(f'Response:\n{result}\n--------------------------------------------------------')          
        # return result        

    def submitRegistration(self, username, password,confirmPassword, responseLabel,validationLabel, currentWindow):
        if not checkPassword(password,confirmPassword, validationLabel)  or not validateUsername(username,validationLabel) or not validatePassword(password,validationLabel) :
            return
        encodedPassword = encodeText(password)        
        user = {"username":username, "password":encodedPassword}
        body = {"route":"registration", "user":user}
        responce = self.registration(body)        
        responseLabel.config(text=responce)
        
    def homescreen(self):
        homeScreen = self.window
        homeScreen.title(self.title)        
        homeScreen.geometry(self.appSize)
        homeScreen.resizable(width=False, height=False)

        usernameLabel = Label(homeScreen, text="Username")  
        usernameLabel.place(anchor='w', relx =.05, rely=.1)


        usernameField = Entry(homeScreen,width=10)  
        usernameField.place(anchor='w', width=100, height=25,relx =.05, rely=.15) 

        passwordLabel = Label(homeScreen, text="Password")  
        passwordLabel.place(anchor='w', relx =.05, rely=.3)

        passwordField = Entry(homeScreen,width=10,show="*")  
        passwordField.place(anchor='w',width=100, height=25, relx =.05, rely=.35)        


        confirmPasswordLabel = Label(homeScreen, text="Confirm password" )  
        confirmPasswordLabel.place(anchor='w', relx =.05, rely=.5)
        
        confirmPasswordField = Entry(homeScreen,width=10,show="*")  
        confirmPasswordField.place(anchor='w',width=100, height=25, relx =.05, rely=.55)  

        entries = [passwordField, confirmPasswordField]

        hideFieldsButton = Button(homeScreen, text="*", command=lambda: self.changePasswordVisibility(entries))  
        hideFieldsButton.place(anchor='w', width=25, height=25,relx =.215, rely=.35)  

        

        validationLabel = Label(homeScreen, text="")
        validationLabel.place(anchor='w', relx =.05, rely=.63) 
            
        responseLabel = Label(homeScreen, text="")
        responseLabel.place(anchor='w', relx =.05, rely=.7) 
          
        submitButton = Button(homeScreen, text="Register", command=lambda: self.submitRegistration(usernameField.get(), passwordField.get(),confirmPasswordField.get(),responseLabel, validationLabel, homeScreen))  
        submitButton.place(anchor='w', relx =.05, rely=.8)  

        clearButton = Button(homeScreen, text="Clear log", command=lambda: self.logPanel.delete('1.0', END))  
        clearButton.place(anchor='w', relx =.05, rely=.9)  

        self.logPanel = Text(width=50, height=30)
        self.logPanel.place(anchor='e', relx =0.95, rely=.5)
        
        scroll = Scrollbar(command=self.logPanel.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.logPanel.config(yscrollcommand=scroll.set)
    
    def onClosing(self):  
        self.serv_sock.close()      
        self.window.destroy()
 
    def serverLoop(self):
        try:
            while True:
                    client_sock, client_addr = self.serv_sock.accept()
                    print('Connected by', client_addr)
                    while True:  
                        self.chooseRoute(client_sock)  
                                
                    print('Disconnected by', client_addr)        
                    client_sock.close()
        finally:
            self.serv_sock.close()


    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        self.serv_sock.bind(('', self.port))
        self.serv_sock.listen(self.listen_count) 
        
   
        try:
            self.homescreen()
            self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
            serverThread = Thread(target=self.serverLoop)
            serverThread.start()
            self.window.mainloop()
            # tkThread = Thread(target=self.window.mainloop)
            # tkThread.start()
            
        finally:
            
            self.onClosing()
    


if __name__=="__main__":
    app = ServerApp()
    app.start()