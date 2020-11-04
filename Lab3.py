from tkinter import *
from tkinter import filedialog as fd
import zipfile
from itertools import product
from tkinter.ttk import Progressbar
from time import sleep
path=''
path_dictionary=''
root = Tk()

b1= Button(root, text='Выбрать файл')
b2= Button(root, text='Полный перебор')
b3= Button(root, text='Выбрать словарь')
b4= Button(root, text='Перебор словарем')
l=Label(root, text='Введите символы для пароля')
e=Entry(root, width=50)
l1=Label(root, text='Введите длину пароля')
e1=Entry(root, width=50)
l2=Label(root, text='')

def openfile(event):
    global path
    path=fd.askopenfilename()
b1.bind('<Button-1>', openfile)

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
    a = zipfile.ZipFile(path, 'r')
    count=3
    while count<=int(e1.get()):
      for i in product(e.get(), repeat=count):
        line=bytes(''.join(i),'ASCII')
        try:
            a.extractall(path='D:\\3', pwd=line)
        except:
            l2['text'] =('The {} word not matched.'.format(line))
        else:
            l2['text'] =('Wow ! found the password: {}'.format(line))
            break
      count+=1
    a.close()
b2.bind('<Button-1>', hack)



def hack_dictionary(event):
    for y in range(101):
        pb.configure(value=y)
        pb.update()
        sleep(0.02)
    b = zipfile.ZipFile(path, 'r')
    with open(path_dictionary, 'rb') as password_list:
        for line in password_list:
            line = line.replace(b'\n', b'')
            try:
                b.extractall(path='D:\\3', pwd=line)
            except:
                l2['text'] =('The {} word not matched.'.format(line))
            else:
                l2['text'] =('Wow ! found the password: {}'.format(line))
                break
    b.close()
b4.bind('<Button-1>', hack_dictionary)

b1.pack()
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












