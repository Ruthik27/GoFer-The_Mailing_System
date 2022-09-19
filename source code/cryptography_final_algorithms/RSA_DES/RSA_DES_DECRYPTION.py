
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


def DES_RSA(subject, key_image):

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

    print("message : ",message)

    algo_type=message.split('\n')[-4]
    key=message.split('\n')[-3]

    print('=========')
    print(algo_type)
    print(key)
    ####
    f = open(key + '.pem','rb')
    keyPair = RSA.import_key(f.read())
    f.close()


    storage.child("/"+subject).download("received_encrypted_file.txt")

    f = open('received_encrypted_file.txt','rb')
    encrypted = f.read()
    f.close()

    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted = decryptor.decrypt(encrypted)
    decrypted = decrypted.decode()

    decrypted_DES = ''

    for i in range (len(decrypted)):
        if(i%4 != 0):
            decrypted_DES = decrypted_DES + decrypted[i]

    print('Decrypted:', decrypted_DES)



##########################################


subject = 'from ajay'
key_image = "./encrypted_image.png"
##key_image = "./a.jpg"
DES_RSA(subject, key_image)


