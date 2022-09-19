import pyaes, pbkdf2, binascii, os, secrets
from encry import st_enc
import random

import pyrebase

config = {
    "apiKey": "AIzaSyCKr9hxtY08fIDQbaRU9Q2WCegeb68KoYE",
    "authDomain": "fbstorage-98a2d.firebaseapp.com",
    "databaseURL": "https://fbstorage-98a2d.firebaseio.com",
    "projectId": "fbstorage-98a2d",
    "storageBucket": "fbstorage-98a2d.appspot.com",
    "messagingSenderId": "120054639692",   
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

def AES_DES(subject,plaintext):
    # Derive a 256-bit AES encryption key from the password
    password = "BE PROJECT"
    passwordSalt = os.urandom(16)

    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)

    # Encrypt the plaintext with the given key:
    key2 = secrets.randbits(256)

##    file = open('key1.key', 'wb')  # Open the file as wb to write bytes
##    file.write(key)  # The key is type bytes still
##    file.close()


    enc = 'AES' + str(random.randint(0,3072))
    print(enc)
    file = open(enc + '.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()

    file = open('key2.key', 'w')  # Open the file as wb to write bytes
    file.write(str(key2))  # The key is type bytes still
    file.close()

    print(str(key) + '\n' + str(key2))

    print()

##    plaintext = "THIS IS AJAY "
    print("Plain Text :  ", plaintext)

    ###########

    encrypted_DES = ''

    AES_key = ['*','#','@','!','%',
           '^','&','a','b','c',
           'd','e','f','g','h',
           'i','j','k','l','m',
           'n','o','p','q','r',
           's','t','u','v','w',
           'x','y','z','Q','E',
           'R','T','Y','U','O',
           'A','D','F','G','H',
           'L','X','B','N','M',
           '4','2','1','3','6',
           '5','7','8','9','0','=','+']

    for i in range (len(plaintext)):
        if(i%3 == 0):
            encrypted_DES = encrypted_DES + AES_key[random.randint(0, 60)]
        encrypted_DES = encrypted_DES + plaintext[i]

    print(encrypted_DES)


    ###########


    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(key2))

    ciphertext = aes.encrypt(encrypted_DES)

    f = open("encrypted_file.txt", "wb")
    f.write(ciphertext)
    f.close()


    storage.child("/" + subject).put("encrypted_file.txt")

    print(ciphertext)
    st_enc('algo3' + '\n' + enc + '\n' + str(key) + '\n' + str(key2))


subject = 'to ajay' 
plaintext = 'Take data from ajay to you'
AES_DES(subject,plaintext)


