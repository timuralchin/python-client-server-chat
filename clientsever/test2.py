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










if __name__ == '__main__':
    message = "TESTMESSAGEfwegfewfsrgt     erger eg      вамвиваива  пук  14214235   wefwef"
    Key = "213456789765432"    
    a= encrypt(message, Key)
    b = decrypt(a, Key)
    print(f'Encrypted:{a}\nDecrypted:{b}')


