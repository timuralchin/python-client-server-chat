import socket
import json
import hashlib 
class Response:

    def __init__(self, data):
        self.__dict__ = json.loads(data)


class ServerApp:
    def __init__(self, port=4001, listen_count=10):
        self.port = port
        self.listen_count = listen_count
       
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



    def login(self,data):        
        user = data['user']
        username = user['username']
        password = user['password'] 
        fileName = 'db/users.json' 

        with open(fileName, 'r') as json_file: 
            users = json.load(json_file) 

        if self.isUserExist(username,users['users']):
            if self.compareUsernamePassword(username,password,users['users']):
                return 'Success'
            else:
                return 'Invalid password'
        else:
            return 'User does not exist!'        
            
        


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
            
        
    def chooseRoute(self,data):        
        decodedJson  = json.loads(data.decode('utf-8')) 
        print(f'Request:\n{decodedJson}\n--------------------------------------------------------')       
        route = decodedJson['route']   
        method = f'self.{route}'           
        result = eval(method)(decodedJson)  
        print(f'Response:\n{result}\n--------------------------------------------------------')          
        return result        
       

    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        self.serv_sock.bind(('', self.port))
        self.serv_sock.listen(self.listen_count) 
        
   
        try:
            while True:
                client_sock, client_addr = self.serv_sock.accept()
                print('Connected by', client_addr)
                while True:                        
                    request = client_sock.recv(1024)
                    if not request:            
                        break
                    response = self.chooseRoute(request)                   
                    client_sock.sendall(bytes(response, encoding="utf-8"))
                            
                print('Disconnected by', client_addr)        
                client_sock.close()
        finally:
            self.serv_sock.close()   
    


if __name__=="__main__":
    app = ServerApp()
    app.start()