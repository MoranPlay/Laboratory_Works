from tkinter import *
from tkinter import filedialog as fd
import hashlib
import glob

file=glob.glob("D:/*.txt")
my_file = open("D:/save.txt", "w")
for f in file:
    with open(f, 'rb') as f3:
        data48=f3.read()
        gethash = hashlib.md5(data48).hexdigest()
        my_file.write("f: "+gethash)

        print("f: " + gethash)
my_file.close()
path_file1=''
path_file2=''

root = Tk()

b1= Button(root, text='Выбрать файл')
b2= Button(root, text='Хешировать')
l_file1= Label(root, bg='black', fg='white')
l_file2= Label(root, bg='black', fg='white')

def openfile(event):
    global path_file1
    global path_file2
    path_file1=fd.askopenfilename()
    path_file2=fd.askopenfilename()
    print(path_file1)
    print(path_file2)
b1.bind('<Button-1>', openfile)

def hash(event):
    h_file1 = hashlib.md5()
    h_file2 = hashlib.md5()
    BUF_SIZE=1
    if path_file1!='' or path_file2!='':
        with open(path_file1, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                h_file1.update(data)
        with open(path_file2, 'rb') as f2:
            while True:
                data2 = f2.read(BUF_SIZE)
                if not data2:
                    break
                h_file2.update(data2)
                #hashlib.md5(data2)

        print("Файлы идентичны? "+str(h_file1.hexdigest()==h_file2.hexdigest()))
        l_file1['text']='Хэширование файла ' + path_file1 + ' '+h_file1.hexdigest()
        l_file2['text']='Хэширование файла ' + path_file2 + ' '+h_file2.hexdigest()

b2.bind('<Button-1>', hash)


b1.pack()
b2.pack()
l_file1.pack()
l_file2.pack()

root.mainloop()
