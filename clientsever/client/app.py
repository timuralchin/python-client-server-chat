from tkinter import * 
import socket
from bitarray import bitarray
import sys
import json
import asyncio
import hashlib 
from time import sleep
import re
from lib.support import *

    

class ClientApp:

    def __init__(self, server_url, port):
        self.port = port
        self.server_url = server_url
        self.window = Tk()
        self.appSize = '600x400'
        self.window.geometry(self.appSize)
        self.window.resizable(width=False, height=False)
        self.hideImage = PhotoImage(file='src/img/eye-icon.png').subsample(6,6)
        
    def start(self):       
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((self.server_url, self.port))
        try:
            self.startScreen()
            self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
            self.window.mainloop()
        finally:
            self.client_sock.close()
            self.window.destroy()

    

    

   

    def startScreen(self):
        #add if user is already loged in checking
        self.loginScreen()
    
    def checkPassword(self, password, confirmPassword, validationLabel):
        if password!=confirmPassword:
            validationLabel.config(text="Passwords are not the same")            
            return False
        else:
            validationLabel.config(text="")   
            return True
    
    def changePasswordVisibility(self, passwordField):        
        state = passwordField[0].cget("show")
        for etry in passwordField:
            if state == '':
                etry.config(show="*")
            else:
                etry.config(show="")

    def userScreen(self, parentWindow):
        parentWindow.withdraw()
        userWindow = Toplevel(parentWindow)
        userWindow.title('Chat') 
        userWindow.geometry(self.appSize)
        goBackButton = Button(userWindow, text="Go back", command=lambda: self.goBack(parentWindow, userWindow))  
        goBackButton.place(anchor='center', relx =.5, rely=.5)  


    def loginScreen(self):        
        loginWindow =self.window 
        loginWindow.title('Login')
        

        usernameLabel = Label(loginWindow, text="Username")  
        usernameLabel.place(anchor='center',relx =.5, rely=.1)  

        usernameField = Entry(loginWindow)  
        usernameField.place(anchor='center',width=100, height=25, relx =.5, rely=.15) 
        

        responseLabel = Label(loginWindow, text="")  
        responseLabel.place(anchor='center', relx =.5, rely=.5)

        submitButton = Button(loginWindow, text="Login", command=lambda: self.submitLogin(usernameField.get(), responseLabel, loginWindow))  
        submitButton.place(anchor='center', relx =.5, rely=.6)        

    def passwordScreen(self,parentWindow, login, response):        
        loginWindow =Toplevel(parentWindow)
        loginWindow.geometry(self.appSize)
        loginWindow.title('Login')
        

        usernameLabel = Label(loginWindow, text="Username")  
        usernameLabel.place(anchor='center',relx =.5, rely=.1)  

        usernameField = Entry(loginWindow)  
        usernameField.place(anchor='center',width=100, height=25, relx =.5, rely=.15) 
        usernameField.insert(END, login)
        usernameField.config(state=DISABLED)

        passwordLabel = Label(loginWindow, text="Password")  
        passwordLabel.place(anchor='center', relx =.5, rely=.3)

        passwordField = Entry(loginWindow,show="*")  
        passwordField.place(anchor='center', width=100, height=25,  relx =.5, rely=.35)
        
        entries = [passwordField]

        hideFieldsButton = Button(loginWindow, image=self.hideImage, command=lambda: self.changePasswordVisibility(entries))  
        hideFieldsButton.place(anchor='center', width=25, height=25,relx =.605, rely=.35)  
        

        responseLabel = Label(loginWindow, text="")  
        responseLabel.place(anchor='center', relx =.5, rely=.5)

        submitButton = Button(loginWindow, text="Login", command=lambda: self.submitPassword(usernameField.get(), passwordField.get(),response, responseLabel, loginWindow))  
        submitButton.place(anchor='center', relx =.5, rely=.6)     

        

        goBack = Button(loginWindow, text="Back", command=lambda: self.goBack(parentWindow, loginWindow))  
        goBack.place(anchor='center', relx =.5, rely=.7)             
      

       
        
    

    def goBack(self, previousWindow, currentWindow):
        previousWindow.deiconify()
        currentWindow.withdraw()

    def submitLogin(self, username, responseLabel, currentWindow):
             
        user = {"username":username}
        body = {"route":"login", "user":user}
        userData = json.dumps(body)
        self.client_sock.sendall(bytes(userData, encoding="utf-8"))
        data = self.client_sock.recv(1024)
        message = data.decode('utf-8')             
        if message == 'User does not exist!':
            responseLabel.config(text=message) 
        else:
            self.passwordScreen(currentWindow, username, message)
            currentWindow.withdraw()
        
    def submitPassword(self, username, password, message, responseLabel, currentWindow):
        password = encodeText(password)
        request = encodeText(password+message)
        user = {"username":username, 'sault':request}
        body = {"route":"auth", "user":user}
        userData = json.dumps(body)
        self.client_sock.sendall(bytes(userData, encoding="utf-8"))
        data = self.client_sock.recv(1024)
        message = data.decode('utf-8')          
        responseLabel.config(text=message) 
            
        
            

    
        

    def onClosing(self):
        self.client_sock.close()
        self.window.destroy()


    

if __name__=="__main__":
    app = ClientApp('127.0.0.1',4000)
    app.start()