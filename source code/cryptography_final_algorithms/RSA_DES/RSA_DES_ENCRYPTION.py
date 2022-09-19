from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import random

from encry import st_enc



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

##storage.child("/document").download("d.txt")


def DES_RSA(subject,plain_text):

    keyPair = RSA.generate(3072)

    pubKey = keyPair.publickey()

    pubKeyPEM = pubKey.exportKey()

    privKeyPEM = keyPair.exportKey()

    print(privKeyPEM.decode('ascii'))


    enc = 'RSA' + str(random.randint(0,3072))
    print(enc)
    f = open(enc + '.pem','wb')
    f.write(keyPair.exportKey('PEM'))
    f.close()


    final_key = 'algo2\n' + enc + '\nencryption\nRSA'

##    plain_text = "A message for encryption"


    ###########

    encrypted_DES = ''

    key = ['*','#','@','!','%',
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

    for i in range (len(plain_text)):
        if(i%3 == 0):
            encrypted_DES = encrypted_DES + key[random.randint(0, 60)]
        encrypted_DES = encrypted_DES + plain_text[i]
    st_enc(final_key)

    print(encrypted_DES)


    ###########

    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(encrypted_DES.encode())
    print("Encrypted:", binascii.hexlify(encrypted))

    f = open('encrypted_file.txt','wb')
    f.write(encrypted)
    f.close()

    storage.child("/" + subject).put("encrypted_file.txt")


DES_RSA('from ajay','Hello this is ajay FROM PuNe')

