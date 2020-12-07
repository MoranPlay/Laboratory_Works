import math
from tkinter import *
from tkinter import filedialog as fd
import matplotlib.pyplot as plt

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
    plt.figure(2)
    plt.show()


def calculateEntropy(event):
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
    #print(y1)
    entropy = -(zeros / lenf) * math.log2(zeros / lenf) - (ones / lenf) * math.log2(ones / lenf)
    entropy_label['text'] = f"H(A) = {entropy}"
    print(entropy)
    print(f"zeros {zeros}")
    print(f"ones {ones}")
    y = [zeros, ones]
    x = (0, 1)
    title = "Count bits"
    drawGraphics(x, y, title)
    monotoneCheck(y1)



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
    plt.figure(1)
    plt.hist(t)
    plt.show()



root.mainloop()
