##https://www.youtube.com/watch?v=CBuu17j_WnA
##myaccount.google.com\lesssecureapps

import smtplib
from email.message import EmailMessage
import os
import imghdr

sender_mail_id = 'iotproject2005@gmail.com'
password = 'sanjay9890704605'

def send(subject,send_to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_mail_id
    msg['To'] = send_to
    msg.set_content("Stegnography Image. Use this image to decrypt received data")

    with open('./static/' + 'encrypted_image.png','rb') as m:

        file_data = m.read()
        file_type = imghdr.what(m.name)
        file_name = m.name

    msg.add_attachment(file_data, maintype = 'image', subtype = file_type, filename=subject + '.png')

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        smtp.login(sender_mail_id,password)
        smtp.send_message(msg)
