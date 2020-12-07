import math
from tkinter import *
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import random
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
path = ''

selectFileButton = Button(root, bg='black', fg='white', text='Select file', width=30)
selectFileButton.pack()

entropy_label = Label(root, text='Entropy')
entropy_label.pack()

start_button = Button(root, text='Стартуем!')
start_button.pack()
global zeros
global ones
global lenf


def openFile(event):
    global path
    path = fd.askopenfilename()


selectFileButton.bind('<Button-1>', openFile)


def drawGraphics(x, y, title):
    plt.xticks(x)
    plt.bar(x, y)
    plt.title(title)
    plt.figure(1)


def calculateEntropy(event):
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
            S.append(int(bit))
    drawGraphics(x, y, title)
    monotoneCheck(S)
    minAAKF(S)
    plt.show()


start_button.bind('<Button-1>', calculateEntropy)


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
    plt.figure(2)
    plt.title("Check for monotony")
    plt.hist(t)
    # plt.show()


def minAAKF(y1):
    S = y1
    # for bits in y1:
    #     for bit in bits:
    #         S.append(int(bit))
    # print(S)
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
    # window.mainloop()


root.mainloop()
