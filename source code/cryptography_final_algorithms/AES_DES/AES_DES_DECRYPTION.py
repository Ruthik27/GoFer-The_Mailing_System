
import pyaes, pbkdf2, binascii, os, secrets
import cv2
from tkinter import filedialog, Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np

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


def AES_DES(subject, key_image):

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


    print(message)

    kk=message.split('\n')[-2]
    key = kk[2:len(kk)-1]

    file = open(message.split('\n')[-3] + '.key', 'rb')  # Open the file as wb to read bytes
    key = file.read()  # The key will be type bytes
    file.close()
    print()

    print(key)

    key2 = int(message.split('\n')[-1])

    storage.child("/"+subject).download("received_encrypted_file.txt")

    f = open('received_encrypted_file.txt','rb')
    ciphertext = f.read()
    f.close()

    # Decrypt the ciphertext with the given key:
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(key2))
    decrypted = aes.decrypt(ciphertext)
    print('Decrypted:', decrypted)

    decrypted = decrypted.decode()

    decrypted_AES = ''

    for i in range (len(decrypted)):
        if(i%4 != 0):
            decrypted_AES = decrypted_AES + str(decrypted[i])

    print('Decrypted:', decrypted_AES)


subject = 'to ajay'
key_image = "./encrypted_image.png"
##key_image = "./a.jpg"
AES_DES(subject, key_image)





