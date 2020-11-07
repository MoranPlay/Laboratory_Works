from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
import requests
from tkinter import filedialog as fd

# root = Tk()
# url_label = Label(root, text='Введите url адрес')
# url_entry = Entry(root, width=50)
#
# links_label = Label(root, text='Введите глубину анализа ссылок')
# links_entry = Entry(root, width=50)
# open_file_button = Button(root, text='Выберите директорию')
# start_button = Button(root, text='Стартуем!')
#
# directory = ''
#
# def open_directory(event):
#     global directory
#     directory = fd.askdirectory()
#
# open_file_button.bind('<Button-1>', open_directory)

url = 'http://odeku.edu.ua/language/en/osenu-2/'


def recursive_url(url, depth):
    newlink = []
    if depth == 2:
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        #newlink = soup.find_all('a', limit=2)
        for link in soup.find_all('a', limit=2):
             #newlink.append(link.get('href'))
             print(link.get('href'))
             return link.get('href'), recursive_url(link.get('href'), depth + 1)
        #     #a_link = str(link.get('href'))
        #     if len(link.get('href')) == 0:
        #         return link.get('href')
        #     else:
        #         return link.get('href')
        #             #, recursive_url(link.get('href'), depth + 1)


def getLinks(url):
    links = []
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    #links = soup.find_all('a', limit=3)
    #print(links)
    for link in soup.find_all('a', limit=3):
        #recursive_url(link.get('href'), 0)
        links.append(recursive_url(link.get('href'), 0))
        #print(link)
        #links.append(link)
    return links
getLinks(url)
#print(getLinks(url))

# def start(event):
#     print('ok')
#
#
#
# start_button.bind('<Button-1>', start)
#
# url_label.pack()
# url_entry.pack()
# links_label.pack()
# links_entry.pack()
# open_file_button.pack()
# start_button.pack()
#
# root.mainloop()
