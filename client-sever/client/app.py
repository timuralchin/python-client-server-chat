from tkinter import * 
import socket
from bitarray import bitarray
import sys
import json
import asyncio
import hashlib 

    

class ClientApp:

    def __init__(self, server_url, port):
        self.port = port
        self.server_url = server_url
        self.window = Tk()
        
    def start(self):       
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((self.server_url, self.port))
        try:
            self.startScreen()
            self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
            self.window.mainloop()
        finally:
            self.client_sock.close()
    def encodeText(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def startScreen(self):
        #add if user is already loged in checking
        self.loginScreen()
    
    def checkPassword(self, password, confirmPassword, errorLabel):
        if password!=confirmPassword:
            #errorLabel.config(text="Passwords are not the same")            
            return False
        else:
            return True
    
    def loginScreen(self):
        #self.window.withdraw()
        loginWindow =self.window #Toplevel(self.window)
        loginWindow.title('Login')
        loginWindow.geometry('600x400')

        usernameLabel = Label(loginWindow, text="Username")  
        usernameLabel.place(anchor='center', relx =.5, rely=.1)  

        usernameField = Entry(loginWindow,width=10)  
        usernameField.place(anchor='center', relx =.5, rely=.15) 

        passwordLabel = Label(loginWindow, text="Password")  
        passwordLabel.place(anchor='center', relx =.5, rely=.3)

        passwordField = Entry(loginWindow,width=10,show="*")  
        passwordField.place(anchor='center', relx =.5, rely=.35)

        responseLabel = Label(loginWindow, text="")  
        responseLabel.place(anchor='center', relx =.5, rely=.5)

        submitButton = Button(loginWindow, text="Login", command=lambda: self.submitLogin(usernameField.get(), passwordField.get(), responseLabel))  
        submitButton.place(anchor='center', relx =.5, rely=.6)       
       

        registrationButton = Button(loginWindow, text="Don't have an account yet? ", command=lambda: self.registrationScreen(loginWindow))  
        registrationButton.place(anchor='center', relx =.5, rely=.7)
        
    def registrationScreen(self, parentWindow):
        parentWindow.withdraw()
        registrationWindow = Toplevel(parentWindow)
        registrationWindow.title('Registration')
        registrationWindow.geometry('600x400')

        usernameLabel = Label(registrationWindow, text="Username")  
        usernameLabel.place(anchor='center', relx =.5, rely=.1)


        usernameField = Entry(registrationWindow,width=10)  
        usernameField.place(anchor='center', relx =.5, rely=.15) 

        passwordLabel = Label(registrationWindow, text="Password")  
        passwordLabel.place(anchor='center', relx =.5, rely=.3)

        passwordField = Entry(registrationWindow,width=10,show="*")  
        passwordField.place(anchor='center', relx =.5, rely=.35)
        

        confirmPasswordLabel = Label(registrationWindow, text="Confirm password" )  
        confirmPasswordLabel.place(anchor='center', relx =.5, rely=.5)
        
        confirmPasswordField = Entry(registrationWindow,width=10,show="*")  
        confirmPasswordField.place(anchor='center', relx =.5, rely=.55)   
            
        errorLabel = Label(registrationWindow, text="")
        errorLabel.place(anchor='center', relx =.5, rely=.7)   
        submitButton = Button(registrationWindow, text="Register", command=lambda: self.submitRegistration(usernameField.get(), passwordField.get(),confirmPasswordField.get(),errorLabel))  
        submitButton.place(anchor='center', relx =.5, rely=.8)  
        
        goBackButton = Button(registrationWindow, text="Go back", command=lambda: self.goBack(parentWindow, registrationWindow))  
        goBackButton.place(anchor='center', relx =.5, rely=.9)  

    def goBack(self, previousWindow, currentWindow):
        previousWindow.deiconify()
        currentWindow.withdraw()

    def submitLogin(self, username, password, responseLabel):
        encodedPassword = self.encodeText(password)        
        user = {"username":username, "password":encodedPassword}
        body = {"route":"login", "user":user}
        userData = json.dumps(body)
        self.client_sock.sendall(bytes(userData, encoding="utf-8"))
        data = self.client_sock.recv(1024)
        message = data.decode('utf-8')
        responseLabel.config(text=message)       
        
    
            

    def submitRegistration(self, username, password,confirmPassword, errorLabel):
        if not self.checkPassword(password,confirmPassword,errorLabel):
            return
        encodedPassword = self.encodeText(password)        
        user = {"username":username, "password":encodedPassword}
        body = {"route":"registration", "user":user}
        userData = json.dumps(body)
        self.client_sock.sendall(bytes(userData, encoding="utf-8"))
        data = self.client_sock.recv(1024)
        message = data.decode('utf-8')
        errorLabel.config(text=message)
        
        

    def onClosing(self):
        self.client_sock.close()
        self.window.destroy()


    

if __name__=="__main__":
    app = ClientApp('127.0.0.1',4001)
    app.start()