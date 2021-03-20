import hashlib 
import re
import math
import random as rnd
from math import gcd

def sbox(key):    
    s_box = list(range(256)) 
    j = 0
    for i in range(256):
        j = (j + s_box[i] + ord(key[i % len(key)])) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box

def encrypt(plain, key):
    box = sbox(key)
    res = []
    i = j =0
    for s in plain:
        i = (i + 1) %256
        j = (j + box[i]) %256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j])% 256
        k = box[t]
        res.append(chr(ord(s)^k))
    cipher = "".join(res)

    return cipher

def decrypt(plain, key):
    box = sbox(key)
    plain = plain
    res = []
    i = j =0
    for s in plain:
        i = (i + 1) %256
        j = (j + box[i]) %256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j])% 256
        k = box[t]
        res.append(chr(ord(s)^k))
    cipher = "".join(res)
    return cipher


#Jacobian symbol
def Jacobian(a, n): 
    if (a == 0): 
        return 0 
    ans = 1 
    if (a < 0):         
        a = -a
        if (n % 4 == 3): 
            ans = -ans 
    if (a == 1): 
        return ans
    while (a): 
        if (a < 0): 
            a = -a
            if (n % 4 == 3):
                ans = -ans 
        while (a % 2 == 0): 
            a = a // 2 
            if (n % 8 == 3 or n % 8 == 5): 
                ans = -ans  
        a, n = n, a
        if (a % 4 == 3 and n % 4 == 3): 
            ans = -ans
        a = a % n
        if (a > n // 2): 
            a = a - n 
    if (n == 1): 
        return ans
    return 0 

def solovayStrassen(p, iterations):    
    for i in range(iterations):         
        a = rnd.randint(2, p - 1)         
        if gcd(a, p) > 1:
            return False        
        first = pow(a, (p - 1) // 2, p)    
        j = Jacobian(a, p) % p                            
        if first != j: 
            return False 
    return True

def findFirstPrime(n, k): 
    while not solovayStrassen(n,k):
        n+=2   
    return n 

def generateServer():
    p =  rnd.getrandbits(512)  
    if p%2==0:
        p+=1  
    p = findFirstPrime(p,1000) 
    g = rnd.getrandbits(64)
    a = rnd.getrandbits(64)
    if g%2 == 0:
        g+=1  
    if a%2 == 0:
        a+=1
    while True:
        if solovayStrassen(g,100) and pow(g, p-1, p)==1:            
            break
        else:
           g+=2     
    
    return g,p,a        


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