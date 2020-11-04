import webbrowser
from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import filedialog as fd

root = Tk()
url_label = Label(root, text='Введите url адрес')
url_entry = Entry(root, width=50)

links_label = Label(root, text='Введите глубину анализа ссылок')
links_entry = Entry(root, width=50)
open_file_button = Button(root, text='Выберите директорию')
start_button = Button(root, text='Стартуем!')


# url = 'http://geocitiessites.com/CapeCanaveral/launchpad/1364/Stars.html'


def openDirectory(event):
    global directory
    directory = fd.askdirectory()
    # print(directory)


open_file_button.bind('<Button-1>', openDirectory)


def start(event):
    url = url_entry.get()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    output = open(directory + '/text.txt', 'w')
    output.write(str(soup))
    webbrowser.open(url)
    # quotes = soup.find_all('span', class_='text')
    quotes = soup.findAll('a', attrs={'href': re.compile("http://")}, limit=int(links_entry.get()))
    for link in quotes:
        webbrowser.open(link.get('href'))

        print(link.get('href'))
    for link in soup.select("img[src^=http]"):
        if "http" in link.get('src'):
            lnk = link.get('src')
            webbrowser.open(lnk)
            print(lnk)


start_button.bind('<Button-1>', start)

url_label.pack()
url_entry.pack()
links_label.pack()
links_entry.pack()
open_file_button.pack()
start_button.pack()
root.mainloop()
