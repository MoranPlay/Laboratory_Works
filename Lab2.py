from tkinter import *
import hashlib
from Crypto.Random import get_random_bytes
import pickle
S=[get_random_bytes(16) for i in range(0,3)]
D={'user1':(S[0], hashlib.sha3_384(b'pass1' + S[0]).digest()),
'user2':(S[1], hashlib.sha3_384(b'pass2' + S[1]).digest()),
'user3':(S[2], hashlib.sha3_384(b'pass3' + S[2]).digest())}
with open("D:/password.pkl", 'wb') as f:
    pickle.dump(D,f)
with open("D:/password.pkl", 'rb') as f:
    pickle.load(f)
root=Tk()
l1=Label(root, text='Login')
e1=Entry(root, width=50)
l2=Label(root, text='Password')
e2=Entry(root, width=50)
b1=Button(text='Log in')
b2=Button(text='Register')
l3=Label(root)
l4=Label(root, text='New password')
e4=Entry(root, width=50)
b4=Button(text='Change password')


def login(event):
    with open("D:/password.pkl", 'rb') as f:
        D=pickle.load(f)
    if D[e1.get()][1]==hashlib.sha3_384(bytes(e2.get(),'ASCII')+D[e1.get()][0]).digest():
        l3['text']='You are logged in'
          # b3.pack()
        SOLD=get_random_bytes(16)
        NEW_PASS=(SOLD, hashlib.sha3_384(bytes(e2.get(),'ASCII') + SOLD).digest())
        D[e1.get()]=NEW_PASS
        with open("D:/password.pkl", 'wb') as f:
            pickle.dump(D,f)
    else:
        l3['text']='Вы неверно ввели логин или пароль'
b1.bind('<Button-1>',login)

def register(event):
    SOLD=get_random_bytes(16)
    D[e1.get()]=(SOLD, hashlib.sha3_384(bytes(e2.get(),'ASCII') + SOLD).digest())
    with open("D:/password.pkl", 'wb') as f:
        pickle.dump(D,f)
b2.bind('<Button-1>',register)

def change_password(event):
    with open("D:/password.pkl", 'rb') as f:
        D=pickle.load(f)
    if D[e1.get()][1]==hashlib.sha3_384(bytes(e2.get(),'ASCII')+D[e1.get()][0]).digest():
        SOLD = get_random_bytes(16)
        D[e1.get()] = (SOLD, hashlib.sha3_384(bytes(e4.get(), 'ASCII') + SOLD).digest())
        with open("D:/password.pkl", 'wb') as f:
            pickle.dump(D, f)
            l4['text'] = 'Вы успешно сменили пароль'
    else:
        l4['text']='Вы не вошли в систему'
b4.bind('<Button-1>',change_password)

l1.pack()
e1.pack()
l2.pack()
e2.pack()
b1.pack()
b2.pack()
l3.pack()
l4.pack()
e4.pack()
b4.pack()

root.mainloop()
