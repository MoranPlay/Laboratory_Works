import math
from tkinter import *
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Cryptodome.Cipher import AES
import hashlib
from Crypto import Random
import os

root = Tk()
path = ''
pathDec = ''

selectFileButton = Button(root, bg='black', fg='white', text='Select file', width=30)
selectFileButton.pack()

entropy_label = Label(root, text='Entropy')
entropy_label.pack()

iv_label = Label(root, text='Введите вектор инициализации или он сформируется автоматически')
iv_entry = Entry(root, width=50)

start_button = Button(root, width=70, text='Стартуем!')

file_button = Button(root, bg='black', fg='white', width=60, text='Выберите зашифрованный файл')
decode_button = Button(root, width=70, text='Расшифровать')

iv_label.pack()
iv_entry.pack()
start_button.pack()
file_button.pack()
decode_button.pack()

def openDecfile(event):
    global pathDec
    pathDec = fd.askopenfilename()

file_button.bind('<Button-1>', openDecfile)
def openFile(event):
    global path
    path = fd.askopenfilename()


selectFileButton.bind('<Button-1>', openFile)


def drawGraphics(x, y, title):
    plt.xticks(x)
    plt.bar(x, y)
    plt.title(title)
    plt.figure(1)


def calculateEntropy():
    # Второй критерий рисуется в методе calculateEntropy()
    zeros = 0
    ones = 0
    lenf = 0

    with open(path, "rb") as f:
        byte = f.read(1)
        y1 = []
        while byte != b"":
            byte = bin(int(byte.hex(), base=16))[2:].zfill(8)
            y1.append(byte)
            zeros += byte.count('0')
            ones += byte.count('1')
            lenf += 8
            byte = f.read(1)
    entropy = -(zeros / lenf) * math.log2(zeros / lenf) - (ones / lenf) * math.log2(ones / lenf)
    entropy_label['text'] = f"H(A) = {entropy}"
    print(entropy)
    print(f"zeros {zeros}")
    print(f"ones {ones}")
    y = [zeros, ones]
    x = (0, 1)
    title = "Count bits"
    S = []
    for bits in y1:
        for bit in bits:
            S.append(bit)
    drawGraphics(x, y, title)
    distributionOnPlane(S)
    minAAKF(S)
    plt.show()

def distributionOnPlane(y_bitarray):
    canvas_width = 256
    canvas_height = 256

    def paint(x, y):
        python_green = "#476042"
        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        w.create_oval(x1, y1, x2, y2, fill=python_green)

    master = Tk()
    master.title("Points")
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack(expand=YES, fill=BOTH)
    y = y_bitarray
    print(y_bitarray)
    print(len(y_bitarray))
    y1 = []
    for i in range(0, len(y), 8):
        y1.append(int('0b' + ''.join(y[i:i + 8]), 2))
    print(y1)
    print(len(y1))
    if len(y1) % 2 == 0:
        for i in range(0, len(y1), 2):
            paint(y1[i], y1[i + 1])
    else:
        for i in range(0, len(y1) - 1, 2):
            paint(y1[i], y1[i + 1])


def minAAKF(y1):
    S = []
    for bit in y1:
        S.append(int(bit))
    S1 = S + S

    A = []
    for i in range(len(S) - 1):
        s = S1[i:i + len(S)]
        a = [(-1) ** S[j] * (-1) ** s[j] for j in range(len(S))]
        A.append(sum(a) / len(S))

    x = list(range(len(A)))

    Data2 = {'Index': x,
             'AAKF': A}
    entropy_label['text'] += f'\nmin AAKF = {min(A)}'
    df2 = DataFrame(Data2, columns=['Index', 'AAKF'])
    df2 = df2[['Index', 'AAKF']].groupby('Index').sum()

    window = Tk()
    figure3 = plt.Figure(figsize=(5, 4), dpi=100)
    ax2 = figure3.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure3, window)
    line2.get_tk_widget().pack()
    df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
    ax2.set_title('AAKF')

def selectKeyfile():
    h = hashlib.sha512()
    with open(path, 'rb') as file:
        while True:
            fileBytes = file.read(512)
            if not fileBytes:
                break
            h.update(fileBytes)
    key = h.hexdigest().encode('utf-8')[:16]
    return key
def encode(event):
    key = selectKeyfile()
    if len(iv_entry.get()) > 16:
        iv = iv_entry.get().encode('utf-8')[:16]
    else:
        iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_OFB, iv)
    with open('D:\\for_me\\file_saved\\file.txt', 'rb') as f, open('D:\\for_me\\file_saved\\virus.txt', 'wb') as f1:
        f1.write(iv)
        while True:
            data = f.read(1024)
            n = len(data)
            if n == 0:
                break
            elif n % 16 != 0:
                data += (' ' * (16 - n % 16)).encode()
            ciphertext = cipher.encrypt(data)
            f1.write(ciphertext)
    calculateEntropy()
start_button.bind('<Button-1>', encode)

def decode(event):
    key = selectKeyfile()
    with open(pathDec, 'rb') as f, open(
            'D:\\for_me\\file_saved\\virus1.txt',
            'wb') as f1:
        iv = f.read(16)
        cipher = AES.new(key, AES.MODE_OFB, iv)
        fsz = os.path.getsize(str(pathDec))
        while True:
            data = f.read(1024)
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
root.mainloop()
