from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import filedialog as fd
from datetime import datetime
import glob, os

root = Tk()

time_label = Label(root, text='')
url_label = Label(root, text='Введите url адрес')
url_entry = Entry(root, width=50)

depth_label = Label(root, text='Введите глубину анализа ссылок')
depth_entry = Entry(root, width=50)
open_file_button = Button(root, text='Выберите директорию')
start_button = Button(root, text='Стартуем!')

file_extension_label = Label(root, text='Введите расширение файла для поиска')
file_extension_entry = Entry(root, width=50)
file_extension_button = Button(root, text='Поиск')


time_label['text'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
directory = ''
#url = 'http://www.antagene.com/en/pkd-polycystic-kidney-diseasebritish-shorthair'


def openDirectory(event):
    global directory
    directory = fd.askdirectory()


open_file_button.bind('<Button-1>', openDirectory)


def get_image(soup, url):
    for link in soup.find_all('img'):
        webpage_url = url
        src = link.get('src')
        new_url = urljoin(webpage_url, src)
        resource = urllib.request.urlopen(new_url)
        out = open(directory + "/" + new_url.split("/")[-1].split("?")[0], 'wb')
        out.write(resource.read())
        out.close()
        soup = str(soup).replace(src, new_url.split("/")[-1].split("?")[0])
    return str(soup)
    # return src, new_url.split("/")[-1].split("?")[0]


def recursiveUrl(url, depth):
    if depth == int(depth_entry.get()):
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
        output.write(get_image(soup, url))
        newlink = soup.findAll('a', attrs={'href': re.compile("")}, limit=5)
        if len(newlink) == 0:
            return url
        else:
            for link in newlink:
                new_url_link = link.get('href')
                if new_url_link.startswith('http://'):
                    return recursiveUrl(new_url_link, depth + 1)
                else:
                    return recursiveUrl(urljoin(url, new_url_link), depth + 1)


def getLinks(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    get_image(soup, url)
    output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
    output.write(get_image(soup, url))
    for link in soup.findAll('a', attrs={'href': re.compile(urlparse(url).hostname + "/")}, limit=5):
        new_url_link = link.get('href')
        if new_url_link.startswith('http://'):
            recursiveUrl(new_url_link, 0)
        else:
            recursiveUrl(urljoin(url, new_url_link), 0)


def start(event):
    if (depth_entry.get() != ''):
        getLinks(url_entry.get())
    else:
        depth_label['text'] = 'НАПИСАНО ЖЕ Введите глубину анализа ссылок'

start_button.bind('<Button-1>', start)

def search_file(event):
    extension = file_extension_entry.get()
    if extension != '':
        os.chdir(directory)
        for file in glob.glob("*.html"):
            with open(os.path.join(directory, file), 'rb') as password_list:
                source = password_list.read()
                soup = BeautifulSoup(source, 'lxml')
                for link in soup.findAll(['link', 'a', 'img', 'script']):
                    href = link.get('src')
                    if str(href).endswith("." + file_extension_entry.get()):
                        if str(href).startswith("http"):
                            resource = urllib.request.urlopen(href)
                        else:
                            if str(href).startswith("//"):
                                resource = urllib.request.urlopen("https:" + href)
                            else:
                                resource = urllib.request.urlopen(os.path.splitext(file)[0] + href)
                        out = open(directory + "/file_saved/" + href.split("/")[-1].split("?")[0], 'wb')
                        out.write(resource.read())
                        out.close()
    else:
        file_extension_label['text'] = 'Расширение введи'

file_extension_button.bind('<Button-1>', search_file)


time_label.pack()
url_label.pack()
url_entry.pack()
depth_label.pack()
depth_entry.pack()
open_file_button.pack()
start_button.pack()
file_extension_label.pack()
file_extension_entry.pack()
file_extension_button.pack()
root.mainloop()
