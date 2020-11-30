import os
from tkinter import *
from tkinter import filedialog as fd
from Cryptodome.Cipher import AES
import hashlib
from Crypto import Random

path = ''
root = Tk()
password_label = Label(root, text='Введите пароль')
password_entry = Entry(root, width=50)

iv_label = Label(root, text='Введите вектор инициализации или он сформируется автоматически')
iv_entry = Entry(root, width=50)

start_button = Button(root, width=70, text='Стартуем!')

file_button = Button(root, bg='black', fg='white', width=60, text='Выберите зашифрованный файл')
decode_button = Button(root, width=70, text='Расшифровать')

def openfile(event):
    global path
    path = fd.askopenfilename()

file_button.bind('<Button-1>', openfile)

def start(event):
    password = password_entry.get().encode('utf-8')
    key = hashlib.md5(password).hexdigest().encode('utf-8')[:16]
    if len(iv_entry.get()) > 16:
        iv = iv_entry.get().encode('utf-8')[:16]
    else:
        iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_OFB, iv)
    with open('D:\\for_me\\file_saved\\file.txt', 'rb') as f, open('D:\\for_me\\file_saved\\virus.txt', 'wb') as f1:
        #f1.write(iv)
        while True:
            data = f.read(2048)
            n = len(data)
            if n == 0:
                break
            elif n % 16 != 0:
                data += (' ' * (16 - n % 16)).encode()
            ciphertext = cipher.encrypt(data)
            f1.write(ciphertext)


start_button.bind('<Button-1>', start)

def decode(event):
    password = password_entry.get().encode('utf-8')
    key = hashlib.md5(password).hexdigest().encode('utf-8')[:16]
    if len(iv_entry.get()) > 16:
        iv = iv_entry.get().encode('utf-8')[:16]
    else:
        iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_OFB, iv)
    with open(path, 'rb') as f, open(
            'D:\\for_me\\file_saved\\virus1.txt',
            'wb') as f1:
        fsz = os.path.getsize(str(path))
        while True:
            data = f.read(2048)
            n = len(data)
            if n == 0:
                break
            decodetext = cipher.decrypt(data)
            n = len(decodetext)
            if fsz > n:
                f1.write(decodetext)
            else:
                f1.write(decodetext[:fsz])
            fsz -= n
decode_button.bind('<Button-1>', decode)

password_label.pack()
password_entry.pack()
iv_label.pack()
iv_entry.pack()
start_button.pack()
file_button.pack()
decode_button.pack()
root.mainloop()