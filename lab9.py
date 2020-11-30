import random
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math
import numpy

zeros=0
ones=0
lenf=0

with open("D:\\for_me\\1.jpg", "rb") as f:

    byte = f.read(1)
    while byte != b"":
        byte=bin(int(byte.hex(),base=16))[2:].zfill(8)
        zeros+=byte.count('0')
        ones+=byte.count('1')
        lenf+=8
        byte = f.read(1)

print(-(zeros/lenf)*math.log2(zeros/lenf)-(ones/lenf)*math.log2(ones/lenf))
with open("D:\\for_me\\file.txt", "rb") as f:
    Bytes = numpy.fromfile(f, dtype="uint8")
    print(Bytes)
    Bits = numpy.unpackbits(Bytes)
    print(Bits)




S=Bits
# numpy.save('example_1', S)
# a= numpy.load('example_1.npy')
# for i in range(0,400):
#         S.append(random.randint(0,1))

# with open("D:\\for_me\\file.txt", 'w') as f1:
#     f1.write(str(S))
S1=S+S

A=[]
for i in range(len(S)-1):
    s=S1[i:i+len(S)]
    a=[(-1)**S[j]*(-1)**s[j] for j in range(len(S))]
    A.append(sum(a)/len(S))

x=list(range(len(A)))


Data2 = {'Index': x,
        'AAKF': A}

df2 = DataFrame(Data2,columns=['Index','AAKF'])
df2 = df2[['Index', 'AAKF']].groupby('Index').sum()

window = Tk()
figure2 = plt.Figure(figsize=(40,30), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, window)
line2.get_tk_widget().pack()
df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
ax2.set_title('AAKF')

window.mainloop()
