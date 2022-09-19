
import pyaes, pbkdf2, binascii, os, secrets
import cv2
from tkinter import filedialog, Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

image_display_size = 500, 350
import pyrebase
import os
config = {
    "apiKey": "AIzaSyCKr9hxtY08fIDQbaRU9Q2WCegeb68KoYE",
    "authDomain": "fbstorage-98a2d.firebaseapp.com",
    "databaseURL": "https://fbstorage-98a2d.firebaseio.com",
    "projectId": "fbstorage-98a2d",
    "storageBucket": "fbstorage-98a2d.appspot.com",
    "messagingSenderId": "120054639692",
    
}

def ALL_DESCRIPTION(subject, key_image):
    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()


    print('--------------------------')
    print(subject)

    img = cv2.imread(key_image)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data)+1)/8)):
        message.append(data[i*8:(i*8+8)])
    # join all the letters to form the message.
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)
    ##    print(message)

    try:
        algo_type=message.split('\n')[-4]
        print(algo_type)

        if(algo_type == 'algo1'):

            key=message.split('\n')[-3]

            ##        print(key)

            f = open('./static/' + key + '.pem','rb')
            keyPair = RSA.import_key(f.read())
            f.close()


            storage.child("/"+subject).download('./static/' + "received_encrypted_file.txt")

            f = open('./static/' + 'received_encrypted_file.txt','rb')
            encrypted = f.read()
            f.close()


            encrypted_data=encrypted.split(bytes('***','utf-8'))[-2]

            decryptor = PKCS1_OAEP.new(keyPair)
            decrypted = decryptor.decrypt(encrypted_data)
            decrypted_RSA = decrypted.decode()
            print('Decrypted:', decrypted_RSA)

            ########################

            kk=message.split('\n')[-2]
            key = kk[2:len(kk)-1]

            file = open('./static/' + message.split('\n')[-3] + '.key', 'rb')  # Open the file as wb to read bytes
            key = file.read()  # The key will be type bytes
            file.close()
            print()

            print(key)

            key2 = int(message.split('\n')[-1])

            ciphertext=encrypted.split(bytes('***','utf-8'))[-1]

            # Decrypt the ciphertext with the given key:
            aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(key2))
            decrypted_AES = aes.decrypt(ciphertext).decode()

            print('Decrypted:', decrypted_AES)
            print('---------------------------------')
            print('Decrypted:', decrypted_AES + decrypted_RSA )

            f = open("decrypted_file.txt", "w")
            f.write(decrypted_AES + decrypted_RSA)
            f.close()
            os.system("start notepad.exe  decrypted_file.txt")

            return 1
    

        if(algo_type == 'algo2'):
            key=message.split('\n')[-3]
            f = open('./static/' + key + '.pem','rb')
            keyPair = RSA.import_key(f.read())
            f.close()

            storage.child("/"+subject).download('./static/' + "received_encrypted_file.txt")

            f = open('./static/' + 'received_encrypted_file.txt','rb')
            encrypted = f.read()
            f.close()

            decryptor = PKCS1_OAEP.new(keyPair)
            decrypted = decryptor.decrypt(encrypted)
            decrypted = decrypted.decode()

            decrypted_DES = ''

            for i in range (len(decrypted)):
                if(i%51 != 0):
                    decrypted_DES = decrypted_DES + decrypted[i]

            print('Decrypted:', decrypted_DES)
            f = open("decrypted_file.txt", "w")
            f.write(decrypted_DES)
            f.close()
            os.system("start notepad.exe  decrypted_file.txt")
            return 1


        if(algo_type == 'algo3'):
            print('-------------***************-------------')
            print(subject)
            kk=message.split('\n')[-2]
            key = kk[2:len(kk)-1]
            print('-------------***************-------------')

            file = open('./static/' + message.split('\n')[-3] + '.key', 'rb')  # Open the file as wb to read bytes
            key = file.read()  # The key will be type bytes
            file.close()
            key2 = int(message.split('\n')[-1])

            print('-------------***************-------------')
            print(subject)


            storage.child("/"+subject).download( './static/' + "received_encrypted_file.txt")

            f = open('./static/' + 'received_encrypted_file.txt','rb')
            ciphertext = f.read()
            f.close()

            # Decrypt the ciphertext with the given key:
            aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(key2))
            decrypted = aes.decrypt(ciphertext)
            ##        print('Decrypted:', decrypted)

            decrypted = decrypted.decode()

            decrypted_AES = ''

            for i in range (len(decrypted)):
                if(i%4 != 0):
                    decrypted_AES = decrypted_AES + str(decrypted[i])

            print('Decrypted:', decrypted_AES)

            f = open("decrypted_file.txt", "w")
            f.write(decrypted_AES)
            f.close()
            os.system("start notepad.exe  decrypted_file.txt")

            return 1
    except:
        print('invalid inputs')
        return 0

##subject = 'from ajay'
##key_image = "./encrypted_image.png"
####key_image = "./a.jpg"
##ALL_DESCRIPTION(subject, key_image)





