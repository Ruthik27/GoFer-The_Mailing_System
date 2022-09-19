import sqlite3


##con = sqlite3.connect("db.sqlite3")
##cur = con.cursor()
##cur.execute('UPDATE todo_todo SET memo = 2 WHERE id = 0 ')# correct answers
##con.commit()


##receiver = 'sjay'
##
##con = sqlite3.connect("db.sqlite3")
##cur = con.cursor()
##QP = []
##for data in cur.execute('SELECT * FROM auth_user;'):
##        QP.append(data[4])
##con.close()
##print(QP)
##authenticated_receiver = 0
##for name in QP:
##    if receiver == name:
##        authenticated_receiver = 1
##        break
##
##if(authenticated_receiver == 1):
##    print('find')
##else:
##    print('no')
##


receiver = 'a'

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
##authenticated_receiver = 0
##for name in QP:
##    if receiver == name:
##        authenticated_receiver = 1
##        break
##
##if(authenticated_receiver == 1):
##    print('find')
##else:
##    print('no')





##class convert_to_class:
##    def __init__(self,a,b,c,d,e):
##        """ Create a new point at the origin """
##        self.sender = a
##        self.receiver = b
##        self.data_file = c
##        self.algo_type = d
##        self.created_date = e.split(' ')[-2]
##        self.created_time = e.split(' ')[-1].split('.')[-2]
##
##
##users_mails=[]
##for all_mails in QP:
##    users_mails.append(convert_to_class(all_mails[1],all_mails[3],all_mails[3],all_mails[4],all_mails[5]))
##
##for p in users_mails:
##    print(p.sender,p.receiver,p.data_file,p.algo_type,p.created_date,p.created_time)
    










