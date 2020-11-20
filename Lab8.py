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
    key = hashlib.md5(password).hexdigest().encode('utf-8')[:24]
    if len(iv_entry.get()) > 16:
        iv = iv_entry.get().encode('utf-8')[:16]
    else:
        iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    with open('D:\\Магистратура, чёрт побери\\КІБЕРБЕЗПЕКА ТА УПРАВЛІННЯ ЗАХИСТОМ ІНФОРМАЦІЙНИХ СИСТЕМ\\Лаб 8 Кириловский\\file.txt', 'rb') as f, open('D:\\Магистратура, чёрт побери\\КІБЕРБЕЗПЕКА ТА УПРАВЛІННЯ ЗАХИСТОМ ІНФОРМАЦІЙНИХ СИСТЕМ\\Лаб 8 Кириловский\\virus.txt', 'wb') as f1:
        f1.write(iv)
        while True:
            data = f.read()
            if not data:
                break
            ciphertext = cipher.encrypt(data)
            f1.write(ciphertext)

start_button.bind('<Button-1>', start)

def decode(event):
    password = password_entry.get().encode('utf-8')
    key = hashlib.md5(password).hexdigest().encode('utf-8')[:24]
    if len(iv_entry.get()) > 16:
        iv = iv_entry.get().encode('utf-8')[:16]
    else:
        iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    with open(path, 'rb') as f, open(
            'D:\\Магистратура, чёрт побери\\КІБЕРБЕЗПЕКА ТА УПРАВЛІННЯ ЗАХИСТОМ ІНФОРМАЦІЙНИХ СИСТЕМ\\Лаб 8 Кириловский\\virus1.txt',
            'wb') as f1:
        while True:
            ciphertext = f.read()
            if not ciphertext:
                break
            data = cipher.decrypt(ciphertext)
            f1.write(data[16:])
decode_button.bind('<Button-1>', decode)

password_label.pack()
password_entry.pack()
iv_label.pack()
iv_entry.pack()
start_button.pack()
file_button.pack()
decode_button.pack()
root.mainloop()