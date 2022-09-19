from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .forms import IMAGE_upload_form
from .models import Todo
from .models import secure_data,IMAGE_upload
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import tkinter as tk
from tkinter import filedialog
import sqlite3
from cryptography_final_algorithms.ALL_ALGO import AES_DES_ENCRYPTION, AES_RSA_ENCRYPTION, RSA_DES_ENCRYPTION,ALL_DECRYPTION
from . import EMAIL

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
                user.save()
                login(request, user)
                f = open("current_user.txt", "w")
                f.write(request.POST['username'])
                f.close()
                f = open("current_email.txt", "w")
                f.write(request.POST['email'])
                f.close()
                return redirect('mailing_inbox')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            f = open("current_user.txt", "w")
            f.write(request.POST['username'])
            f.close()
            f = open("current_email.txt", "w")
            f.write(request.user.email)
            f.close()
            return redirect('mailing_inbox')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


class convert_to_class:
    def __init__(self,a,b,c,d,e):
        """ Create a new point at the origin """
        self.sender = a
        self.receiver = b
        self.data_file = c
        self.algo_type = d
        self.created_date = e.split(' ')[-2]
        self.created_time = e.split(' ')[-1].split('.')[-2]

@login_required
def mailing(request):
    return render(request, 'todo/mailing.html')


@login_required
def mailing_result(request):
    if request.method == 'GET':
        algo = request.GET['algo']
        subject =request.GET['subject']
        subject = subject.replace('+',' ')
        receiver =request.GET['receiver']
        if(len(algo)==0 or len(subject)==0  or len(receiver)==0 ):
            return render(request, 'todo/mailing.html', { 'error':'Please Consider all the fields'})
        else:

            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            QP = []
            for data in cur.execute('SELECT * FROM auth_user;'):
                    QP.append(data[4])
            con.close()
            print(QP)
            authenticated_receiver = 0
            for name in QP:
                if receiver == name:
                    authenticated_receiver = 1
                    break
            if(authenticated_receiver == 0):
                return render(request, 'todo/mailing.html', { 'error':'Please write authenticated receiver name'})
            else:

                con = sqlite3.connect("db.sqlite3")
                cur = con.cursor()
                QP = []
                for data in cur.execute('SELECT * FROM auth_user;'):
                        QP.append(data)
                con.close()

                for receiver_name in QP:
                        if receiver_name[4] == receiver:
                                receiver_email = receiver_name[6]

                print(receiver_email)

                f = open("current_user.txt", "r")
                user_name = f.read()
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                print(file_path)
                f = open(file_path, "r")
                data_to_send = f.read()
                f.close()
    
                # f = open("current_user.txt", "r")
                # user_name = f.read()
                # f.close()
                
                print(algo)

                if(algo == 'algo1'):
                    print('AES_RSA_ENCRYPTION')
                    AES_RSA_ENCRYPTION.AES_RSA(subject,data_to_send)

                if(algo == 'algo2'):
                    print('RSA_DES_ENCRYPTION')
                    RSA_DES_ENCRYPTION.DES_RSA(subject,data_to_send)

                if(algo == 'algo3'):
                    print('AES_DES_ENCRYPTION')
                    AES_DES_ENCRYPTION.AES_DES(subject,data_to_send)

                EMAIL.send(subject,receiver_email)

                Secure_Data = secure_data.objects.create(sender=user_name,receiver=receiver, data_file=subject,algo_type =algo,created_time = timezone.now())
                return render(request, 'todo/home.html')
                


@login_required
def mailing_inbox(request):

    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    # chats = secure_data.objects
    f = open("current_user.txt", "r")
    user_name = f.read()
    f.close()
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    QP = []
    for data in cur.execute('SELECT * FROM todo_secure_data;'):
        if(data[2]==user_name):
            QP.append(data)
    con.close()

    users_mails=[]
    for all_mails in QP:
        users_mails.append(convert_to_class(all_mails[1],all_mails[2],all_mails[3],all_mails[4],all_mails[5]))
    print("=-=-=-=-=-=-==-=-=-=-==-")

    for p in users_mails:
        print(p.sender,p.receiver,p.data_file,p.algo_type,p.created_date,p.created_time)
    
    return render(request, 'todo/mailing_inbox.html', {'todos':todos,'users_mails':users_mails})

@login_required
def completedtodos(request):
    if request.method == 'POST': 
        print('posting')
        form = IMAGE_upload_form(request.POST, request.FILES)   
        if form.is_valid(): 
            form.save() 
            return redirect('download_mail') 
    else: 
        print(' not posting')
        form = IMAGE_upload_form() 
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos,'form' : form})


@login_required
def download_mail(request):

    IMAGES = IMAGE_upload.objects.all()
    print(IMAGES[len(IMAGES)-1].steganography_image )
    print('./' + str(IMAGES[len(IMAGES)-1].steganography_image ))
    print(str(IMAGES[len(IMAGES)-1].Enter_Subject_of_received_data_to_encrypt_file ))
    image_path = './' + str(IMAGES[len(IMAGES)-1].steganography_image )
    subject_name = str(IMAGES[len(IMAGES)-1].Enter_Subject_of_received_data_to_encrypt_file )
    f = open("current_user.txt", "r")
    user_name = f.read()
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    QP = []
    for data in cur.execute('SELECT * FROM todo_secure_data;'):
        if(data[2]==user_name):
            QP.append(data)
    con.close()

    users_mails=[]
    for all_mails in QP:
        users_mails.append(convert_to_class(all_mails[1],all_mails[2],all_mails[3],all_mails[4],all_mails[5]))

    for p in users_mails:
        print(p.sender,p.receiver,p.data_file,p.algo_type,p.created_date,p.created_time)
    
    valid_subject_name = 0
    for subjects in QP:
        if(subjects[3] == subject_name):
            print(subjects[3])
            valid_subject_name = 1
            break
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    form = IMAGE_upload_form(request.POST, request.FILES)   
    if valid_subject_name == 0:
        return render(request, 'todo/downloaded_file.html', {'status':'Please enter valid subject name'})

    else:
        docode_success = ALL_DECRYPTION.ALL_DESCRIPTION(subject_name,image_path)
        if(docode_success == 1):
            return render(request, 'todo/downloaded_file.html', {'status':'Encrypted file is Downloaded Successfully'})
        else:
            return render(request, 'todo/downloaded_file.html', {'status':'Please give proper Steganography image'})


