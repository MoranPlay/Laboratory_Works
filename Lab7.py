import urllib
import webbrowser
from urllib.parse import urlparse
import img as img
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


url = 'http://geocitiessites.com/CapeCanaveral/launchpad/1364/Stars.html'


def openDirectory(event):
    global directory
    directory = fd.askdirectory()
    #print(directory)


open_file_button.bind('<Button-1>', openDirectory)


def start(event):
   # url = url_entry.get()
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    print(urlparse(url).hostname)
    # output = open(directory + '/' + urlparse(url).hostname + '.html', 'w')
    # output.write(str(soup))
    #webbrowser.open(url)
    # quotes = soup.find_all('span', class_='text')
    quotes = soup.findAll('a', attrs={'href': re.compile("http://" or "https://")})
    for link in quotes:
        #webbrowser.open(link.get('href'))

        # soup1 = BeautifulSoup(requests.get(link.get('href'), stream=True).text, 'lxml')
        # output = open(directory + '/' + urlparse(link.get('href')).hostname + '.html', 'w')
        #output.write(str(soup1))
        print(link.get('href'))
        #img = urllib.request.urlopen(link.get('href')).read()
    # for link in soup.select("img[src^=http]"):
    #     if "http" in link.get('src'):
    #         lnk = link.get('src')
    #         #webbrowser.open(lnk)
    #         print(lnk)

    # p = requests.get(img)
    # out = open("...\img.jpg", "wb")
    # out.write(p.content)
    # out.close()

start_button.bind('<Button-1>', start)

url_label.pack()
url_entry.pack()
links_label.pack()
links_entry.pack()
open_file_button.pack()
start_button.pack()
root.mainloop()
