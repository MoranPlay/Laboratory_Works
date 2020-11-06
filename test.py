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
# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page.read(),'lxml')
# # links = soup.findAll('a', attrs={'href': re.compile("http://" or "https://")})
# # # links = soup.find_all('a', attrs={'a': 'href'})
# print( str(soup))
# print(links)
# for link in links:
#     response = requests.get(link)
#     soup1 = BeautifulSoup(response.text, 'lxml')
#     # page = urllib.request.urlopen(link)
#     # soup1 = BeautifulSoup(page.read())
#     newlink = soup1.findAll('a', attrs={'href': re.compile("http://" or "https://")})
#     print(newlink)


def recursive_url(url, depth):
    if depth == 2:
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        newlink = soup.find_all('a', attrs={'href': re.compile("http://")},limit=2)
        for link in newlink:
            if len(link.get('href')) == 0:
                return url
            else:
                return url, recursive_url(link.get('href'), depth + 1)


def getLinks(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    #print(soup.a)
    links = soup.find_all('a', attrs={'href': re.compile("http://")},limit=2)
    for link in links:
        #print(link.get('href'))
        links.append(recursive_url(link.get('href'), 0))
    return links
print(getLinks(url))

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
