from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import filedialog as fd
import glob, os
import mechanize

root = Tk()
report=[]
time_label = Label(root, text='')
url_label = Label(root, text='Введите url адрес')
url_entry = Entry(root, width=50)

depth_label = Label(root, text='Введите глубину анализа ссылок')
depth_entry = Entry(root, width=50)
open_file_button = Button(root, text='Выберите директорию')
start_button = Button(root, text='Стартуем!')

file_extension_button = Button(root, text='Поиск номеров')

enter_line_label = Label(root, text='Введите запрос для google')
enter_line_entry = Entry(root, width=50)
enter_line_button = Button(root, text='Отправить запрос')
directory = ''
#url = 'http://www.antagene.com/en/pkd-polycystic-kidney-diseasebritish-shorthair'
#https://ktodzvoniv.com.ua/

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
    global report

    os.chdir(directory)
    for file in glob.glob("*.html"):
        with open(os.path.join(directory, file), 'rb') as password_list:
            source = password_list.read()
            soup = BeautifulSoup(source, 'lxml')
            results = re.findall(r'\+38\d{7,}', str(soup))
            print("Ссылка " + file + " содержит номер ")
            print(results)

file_extension_button.bind('<Button-1>', search_file)

def enter_line(event):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    br.open('http://google.com').read()
    br.select_form('f')
    br.form['q'] = enter_line_entry.get()
    z = br.submit()
    print(br.links())
enter_line_button.bind('<Button-1>', enter_line)

url_label.pack()
url_entry.pack()
depth_label.pack()
depth_entry.pack()
open_file_button.pack()
start_button.pack()

file_extension_button.pack()

enter_line_label.pack()
enter_line_entry.pack()
enter_line_button.pack()

root.mainloop()






