import math
from tkinter import *
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import numpy as np

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


def calculateEntropy(event):
    zeros = 0
    ones = 0
    lenf = 0

    with open(path, "rb") as f:
        byte = f.read(1)
        while byte != b"":
            byte = bin(int(byte.hex(), base=16))[2:].zfill(8)
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
    plt.xticks((0, 1))
    plt.bar((0, 1), y)
    plt.title(u'Count bits')
    plt.show()


start_button.bind('<Button-1>', calculateEntropy)

root.mainloop()
