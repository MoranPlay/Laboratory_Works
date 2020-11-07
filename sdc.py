import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import filedialog as fd
import requests
root = Tk()
url_label = Label(root, text='Введите url адрес')
url_entry = Entry(root, width=50)

links_label = Label(root, text='Введите глубину анализа ссылок')
links_entry = Entry(root, width=50)
open_file_button = Button(root, text='Выберите директорию')
start_button = Button(root, text='Стартуем!')

def openDirectory(event):
    global directory
    directory = fd.askdirectory()


open_file_button.bind('<Button-1>', openDirectory)

url = 'http://www.antagene.com/en/pkd-polycystic-kidney-diseasebritish-shorthair'
# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page.read(), 'lxml')
# for link in soup.find_all('img', attrs={'src': re.compile(".png")}):
#         print(link.get('src'))
img = 'https://client.antagene.com/sites/all/themes/antagene/logo2_en.png'
resource = urllib.request.urlopen(img)
out = open("D:/Магистратура, чёрт побери/КІБЕРБЕЗПЕКА ТА УПРАВЛІННЯ ЗАХИСТОМ ІНФОРМАЦІЙНИХ СИСТЕМ/Лаб 7 Кириловский/img.png", 'wb')
out.write(resource.read())
out.close()

def recursiveUrl(url, depth):
    if depth == 4:
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
        output.write(str(soup))
        newlink = soup.findAll('a', attrs={'href': re.compile("http://")})
        # print("recursive")
        # print(newlink)

        if len(newlink) == 0:
            return url
        else:
            for link in newlink:
                return recursiveUrl(link.get('href'), depth + 1)


def getLinks(url):
    links = [url]
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
    output.write(str(soup))
    #print(soup)
    #links = soup.find_all('a', limit=3)
    for link in soup.findAll('a', attrs={'href': re.compile("http://")}):
        links.append(recursiveUrl(link.get('href'), 0))
    return links

def start(event):
    print(getLinks(url))

start_button.bind('<Button-1>', start)

url_label.pack()
url_entry.pack()
links_label.pack()
links_entry.pack()
open_file_button.pack()
start_button.pack()
root.mainloop()

# page = urllib.request.urlopen(link.get('href'))
#         soup1 = BeautifulSoup(page.read(), 'lxml')
#         for link1 in soup1.find_all('a', limit=2)[1:]:
#             print(link1)
#             links.append(recursiveUrl(link1.get('href'), 0))
#         #print(link.get('href'))