from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import random
import pyaes, pbkdf2, binascii, os, secrets
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


def AES_RSA(subject,plaintext):

    keyPair = RSA.generate(3072)

    pubKey = keyPair.publickey()

    pubKeyPEM = pubKey.exportKey()

    privKeyPEM = keyPair.exportKey()

    print(privKeyPEM.decode('ascii'))


    enc = 'RSA_AES' + str(random.randint(0,3072))
    print(enc)
    f = open('./static/' + enc + '.pem','wb')
    f.write(keyPair.exportKey('PEM'))
    f.close()

##    final_key = 'algo2\n' + enc

    text_RSA = plaintext[int(len(plaintext)/2):len(plaintext)]

    print(text_RSA)


    ###########

    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(text_RSA.encode())
    print("Encrypted:", binascii.hexlify(encrypted))

    f = open('./static/' + 'encrypted_file.txt','wb')
    f.write(encrypted)
    f.close()
####################################################################################

    text_AES = plaintext[0:int(len(plaintext)/2)]
    # Derive a 256-bit AES encryption key from the password
    password = "BE PROJECT"
    passwordSalt = os.urandom(16)

    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)

    # Encrypt the plaintext with the given key:
    key2 = secrets.randbits(256)

    file = open('./static/' + 'key1.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()


##    enc = 'AES' + str(random.randint(0,3072))
    print(enc)
    file = open('./static/' + enc + '.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()

    file = open('./static/' + 'key2.key', 'w')  # Open the file as wb to write bytes
    file.write(str(key2))  # The key is type bytes still
    file.close()

    print(str(key) + '\n' + str(key2))

    print()

##    plaintext = "THIS IS AJAY "
    print("Plain Text for AES:  ", text_AES)

    ###########

    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(key2))

    ciphertext = aes.encrypt(text_AES)

    f = open('./static/' + "encrypted_file.txt", "a")
    f.write('***')
    f.close()

    f = open('./static/' + "encrypted_file.txt", "ab")
    f.write(ciphertext)
    f.close()

####################################################################################
    storage.child("/" + subject).put('./static/' + "encrypted_file.txt")

    print(ciphertext)
    st_enc('algo1' + '\n' + enc + '\n' + str(key) + '\n' + str(key2))

##AES_RSA('from ajay','Hello this is ajay FROM PuNe')

