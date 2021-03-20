import socket
import json
import hashlib 
from tkinter import * 
from lib.support import *
from datetime import datetime
from threading import Thread
import time

class ServerApp:
    def __init__(self, port=4010, listen_count=10):
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
        print(user)
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
            g,p,a= generateServer()
            A = pow(g,a,p)
            params = (g, p, A)
            print(f'a={a}')
            print(f'p={p}')
            print(f'g={g}')
            

            print(print(f'Params={params}'))
            responce = json.dumps({"message": 'Success', "body": params})
            client_sock.sendall(bytes(responce, encoding="utf-8"))
            request = client_sock.recv(1024)
            if not request:            
                return    
            request  = request.decode('utf-8') 
            B = int(request)
            self.K = self.setKey(B,a,p)
            print(f'K={self.K}')                     
        else:
            responce =  json.dumps({"message": "Incorrect password"})
            client_sock.sendall(bytes(responce , encoding="utf-8"))    

    def setKey(self, B, a, p):
        K = pow(B, a, p)
        return K

    
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
        print(f'Request:\n{decodedJson}\n--------------------------------------------------------')       
        route = decodedJson['route'] 
        
        if route == "chat":
            message = decrypt(decodedJson['body'], str(self.K))
            self.logPanel.insert(1.0, f"Decoded:{message}\nRaw:{decodedJson['body']}\n")
            return  
        method = f'self.{route}' 
        print(method)          
        eval(method)(decodedJson,client_sock)  

    def sendMessage(self, message, entry):
        enc_message = encrypt(message, str(self.K))
        responce = json.dumps({"route": 'chat', "body": enc_message})
        self.client_sock.sendall(bytes(responce, encoding="utf-8"))
        self.logPanel.insert(1.0, f"{message}\n")
        entry.delete(0, END)


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
        passwordLabel.place(anchor='w', relx =.05, rely=.2)

        passwordField = Entry(homeScreen,width=10,show="*")  
        passwordField.place(anchor='w',width=100, height=25, relx =.05, rely=.25)        


        confirmPasswordLabel = Label(homeScreen, text="Confirm password" )  
        confirmPasswordLabel.place(anchor='w', relx =.05, rely=.4)
        
        confirmPasswordField = Entry(homeScreen,width=10,show="*")  
        confirmPasswordField.place(anchor='w',width=100, height=25, relx =.05, rely=.45)  

        entries = [passwordField, confirmPasswordField]

        hideFieldsButton = Button(homeScreen, text="*", command=lambda: self.changePasswordVisibility(entries))  
        hideFieldsButton.place(anchor='w', width=25, height=25,relx =.215, rely=.25)  

        

        validationLabel = Label(homeScreen, text="")
        validationLabel.place(anchor='w', relx =.05, rely=.53) 
            
        responseLabel = Label(homeScreen, text="")
        responseLabel.place(anchor='w', relx =.05, rely=.6) 
          
        submitButton = Button(homeScreen, text="Register", command=lambda: self.submitRegistration(usernameField.get(), passwordField.get(),confirmPasswordField.get(),responseLabel, validationLabel, homeScreen))  
        submitButton.place(anchor='w', relx =.05, rely=.7)  


        clearButton = Button(homeScreen, text="Clear log", command=lambda: self.logPanel.delete('1.0', END))  
        clearButton.place(anchor='w', relx =.05, rely=.9)  

        self.logPanel = Text(width=50, height=20)
        self.logPanel.place(anchor='e', relx =0.95, rely=.3)
        
        scroll = Scrollbar(command=self.logPanel.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.logPanel.config(yscrollcommand=scroll.set)

        messageField = Entry(homeScreen)  
        messageField.place(anchor='e',width=350, height=50, relx =.95, rely=.7)  

        sendMessage = Button(homeScreen, text="Send", command= lambda: self.sendMessage(messageField.get(),messageField))  
        sendMessage.place(anchor='w', relx =.7, rely=.9)  
    
    def onClosing(self):                 
        self.window.destroy()       
        
 
    def serverLoop(self):
        try:
            while True:
                    self.client_sock, client_addr = self.serv_sock.accept()
                    print('Connected by', client_addr)
                    while True:  
                        self.chooseRoute(self.client_sock)  
                                
                    print('Disconnected by', client_addr)        
                    self.client_sock.close()
        finally:  
            sys.exit()
            self.serv_sock.close()                                
            self.serv_sock.close()  
            

    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        self.serv_sock.bind(('', self.port))
        self.serv_sock.listen(self.listen_count) 
        
   
        try:
            self.homescreen()
            self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
            self.serverThread = Thread(target=self.serverLoop)
            self.serverThread.start()
            self.window.mainloop()
            
            
        finally:    
            self.serv_sock.close()    
            self.serverThread.join()              
            
    


if __name__=="__main__":
    app = ServerApp()
    app.start()
    app.onClosing()