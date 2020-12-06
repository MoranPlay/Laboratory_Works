from tkinter import *
from os.path import basename
from pandas import DataFrame
from bitarray import bitarray
from Cryptodome.Cipher import AES
from tkinter import filedialog as fd
from itertools import product, combinations

import os
import re
import time
import math
import random
import string
import hashlib
import pathlib

import numpy as np
import matplotlib.pyplot as plt

root = Tk()

analyzeFileBtn = Button(root, bg='black', fg='white', text='Select file', width=50)
analyzeFileBtn.pack()

resultLabel = Label(root, bg='black', fg='white', text='', width=50)
resultLabel.pack()

selectKeyfile = Button(root, bg='black', fg='white', text='Select key file', width=50)
selectKeyfile.pack()

encryptFileBtn = Button(root, bg='black', fg='white', text='Encrypt', width=50)
encryptFileBtn.pack()


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def analyzeString(string):
    global zeros
    zeros = 0
    global ones
    global barr
    global y
    barr = bitarray(tobits(string))
    resultLabel['text'] += 'Статистика ключа:\n'
    y = []
    ones = 0
    for bit in barr:
        if bit == True:
            y.append(1)
            ones += 1
        else:
            y.append(0)
            zeros += 1
    overall = zeros + ones
    resultLabel['text'] += f'\nШанс 0: {zeros / overall}'
    resultLabel['text'] += f'\nШанс 1: {ones / overall}'
    calculateEntropy()
    seriesAnalyzer(barr)
    monotoneCheck(barr)


def readFileAndInit(fileName):
    global zeros
    zeros = 0
    global ones
    global barr
    global y
    barr = bitarray()
    y = []
    ones = 0
    resultLabel['text'] += f'{basename(fileName)}:\n'
    with open(fileName, 'rb') as file:
        barr.fromfile(file)
    for bit in barr:
        if bit == True:
            y.append(1)
            ones += 1
        else:
            y.append(0)
            zeros += 1
    overall = zeros + ones
    resultLabel['text'] += f'0%: {zeros / overall}'
    resultLabel['text'] += f'\n1%: {ones / overall}'
    calculateEntropy()
    seriesAnalyzer(barr)
    monotoneCheck(barr)
    plt.show()


def seriesAnalyzer(bitarr):
    seriesList = []
    for i in range(2, 6):
        series = product('01', repeat=i)
        for ser in series:
            seriesList.append(str(''.join(ser)))
    y = []
    for series in seriesList:
        count = len([m.start() for m in re.finditer(series, str(bitarr))])
        y.append(count)
    buildDiagram(seriesList, y)


def buildDiagram(x, y):
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.bar(x, y)
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=90)
    plt.legend()
    # plt.show()


def selectFileClick(event):
    resultLabel['text'] = ''
    selectedFile = fd.askopenfilename(parent=root, title='Выберите файл')
    readFileAndInit(selectedFile)


def calculateEntropy():
    global y
    global zeros
    global ones
    overall = zeros + ones
    pZ = zeros / overall
    pO = ones / overall
    h = 0
    for bit in y:
        if bit == 0:
            h += pZ * math.log2(pZ)
        else:
            h += pO * math.log2(pO)
    h = h * -1
    print(f'H(A): {h}')
    resultLabel['text'] += f'\nH(A): {h}'


def generate_random(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def encryptFile(file, readyKey):
    iv = generate_random(16).encode()
    aes = AES.new(readyKey, AES.MODE_CBC, iv)
    outputname = f'{os.path.basename(file)}.enc'
    print(outputname)
    with open(outputname, 'wb') as output:
        output.write(iv)
        with open(file, 'rb') as input:
            while True:
                data = input.read(2048)
                n = len(data)
                if n == 0:
                    break
                elif n % 16 != 0:
                    data += (' ' * (16 - n % 16)).encode()
                encd = aes.encrypt(data)
                output.write(encd)
    readFileAndInit(outputname)


def encFileClick(event):
    global key
    resultLabel['text'] = ''
    selectedFile = fd.askopenfilename(parent=root, title='Выберите файл')
    encryptFile(selectedFile, key.encode()[0:24])


def selectKeyfileClick(event):
    selectedFile = fd.askopenfilename(parent=root, title='Выберите файл')
    resultLabel['text'] = ''
    h = hashlib.sha512()
    with open(selectedFile, 'rb') as file:
        while True:
            fileBytes = file.read(512)
            if not fileBytes:
                break
            h.update(fileBytes)
    global key
    key = h.hexdigest()
    analyzeString(key)
    readFileAndInit(selectedFile)


def monotoneCheck(y1):
    vozr = 0
    ub = 0
    t = []
    for i in range(1, len(y1)):
        if y1[i] > y1[i - 1] and ub == 0:
            vozr += 1

        elif y1[i] > y1[i - 1] and ub != 0:
            t.append(ub)
            ub = 0
            vozr += 1

        if y1[i] < y1[i - 1] and vozr == 0:
            ub += 1
        elif y1[i] < y1[i - 1] and vozr != 0:
            t.append(vozr)
            vozr = 0
            ub += 1

        if y1[i] == y1[i - 1] and vozr == 0:
            ub += 1
        elif y1[i] == y1[i - 1] and ub == 0:
            vozr += 1
    fig = plt.figure(2)
    plt.hist(t)


analyzeFileBtn.bind('<Button-1>', selectFileClick)
encryptFileBtn.bind('<Button-1>', encFileClick)
selectKeyfile.bind('<Button-1>', selectKeyfileClick)

root.mainloop()

# import random
# from tkinter import *
# from pandas import DataFrame
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# import math
# import numpy
#
# zeros=0
# ones=0
# lenf=0
#
# with open("D:\\for_me\\1.jpg", "rb") as f:
#
#     byte = f.read(1)
#     while byte != b"":
#         byte=bin(int(byte.hex(),base=16))[2:].zfill(8)
#         zeros+=byte.count('0')
#         ones+=byte.count('1')
#         lenf+=8
#         byte = f.read(1)
#
# print(-(zeros/lenf)*math.log2(zeros/lenf)-(ones/lenf)*math.log2(ones/lenf))
# with open("D:\\for_me\\file.txt", "rb") as f:
#     Bytes = numpy.fromfile(f, dtype="uint8")
#     print(Bytes)
#     Bits = numpy.unpackbits(Bytes)
#     print(Bits)
#
#
#
#
# S=Bits
# # numpy.save('example_1', S)
# # a= numpy.load('example_1.npy')
# # for i in range(0,400):
# #         S.append(random.randint(0,1))
#
# # with open("D:\\for_me\\file.txt", 'w') as f1:
# #     f1.write(str(S))
# S1=S+S
#
# A=[]
# for i in range(len(S)-1):
#     s=S1[i:i+len(S)]
#     a=[(-1)**S[j]*(-1)**s[j] for j in range(len(S))]
#     A.append(sum(a)/len(S))
#
# x=list(range(len(A)))
#
#
# Data2 = {'Index': x,
#         'AAKF': A}
#
# df2 = DataFrame(Data2,columns=['Index','AAKF'])
# df2 = df2[['Index', 'AAKF']].groupby('Index').sum()
#
# window = Tk()
# figure2 = plt.Figure(figsize=(40,30), dpi=100)
# ax2 = figure2.add_subplot(111)
# line2 = FigureCanvasTkAgg(figure2, window)
# line2.get_tk_widget().pack()
# df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
# ax2.set_title('AAKF')
#
# window.mainloop()
