import hashlib 
import re

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def primitive_root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g


def genParam():
    pass

def checkPassword( password, confirmPassword, validationLabel):
    if password!=confirmPassword:
        validationLabel.config(text="Passwords are not the same")            
        return False
    else:
        validationLabel.config(text="")   
        return True


def validateUsername(username, validationLabel):
    reg = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    pat = re.compile(reg) 
    mat = re.search(pat, username)
    if mat:  
        validationLabel.config(text="")          
        return True
    else:
        validationLabel.config(text="Invalid username(email)") 
        return False

def validatePassword(password,validationLabel):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg) 
    mat = re.search(pat, password)
    if mat:  
        validationLabel.config(text="")          
        return True
    else:
        validationLabel.config(text="Password, should contain at least\none number, one uppercase, one lowercase character,\none special symbol, 6 characters" ) 
        return False

def encodeText(text):
    return hashlib.md5(str(text).encode()).hexdigest()