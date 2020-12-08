import pathlib
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import filedialog as fd
from datetime import datetime
import glob, os

# root = Tk()
#
# time_label = Label(root, text='')
# url_label = Label(root, text='Введите url адрес')
# url_entry = Entry(root, width=50)
#
# depth_label = Label(root, text='Введите глубину анализа ссылок')
# depth_entry = Entry(root, width=50)
# open_file_button = Button(root, text='Выберите директорию')
#
# file_extension_label = Label(root, text='Введите розширение файла для поиска')
# file_extension_entry = Entry(root, width=50)
#
# start_button = Button(root, text='Стартуем!')
#
# time_label['text'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# directory = ''
url = 'http://www.antagene.com/en/pkd-polycystic-kidney-diseasebritish-shorthair'
pathDec = 'D:\Магистратура, чёрт побери\КІБЕРБЕЗПЕКА ТА УПРАВЛІННЯ ЗАХИСТОМ ІНФОРМАЦІЙНИХ СИСТЕМ\Лаб 7 Кириловский'
os.chdir(pathDec)
for file in glob.glob("*.html"):
    with open(os.path.join(pathDec, file), 'rb') as password_list:
        source = password_list.read()
        soup = BeautifulSoup(source, 'lxml')
        for link in soup.findAll(['link', 'a', 'img', 'script']):
            href = link.get('src')
            if str(href).endswith(".js"):
                if str(href).startswith("http"):
                    resource = urllib.request.urlopen(href)
                    # out = open(path + "/file_saved/" + href.split("/")[-1].split("?")[0], 'wb')
                    # out.write(resource.read())
                    # out.close()
                    # print(href)
                else:
                    if str(href).startswith("//"):
                        resource = urllib.request.urlopen("https:" + href)
                    else:
                        resource = urllib.request.urlopen(os.path.splitext(file)[0] + href)
                out = open(pathDec + "/file_saved/" + href.split("/")[-1].split("?")[0], 'wb')
                out.write(resource.read())
                out.close()



# def openDirectory(event):
#     global directory
#     directory = fd.askdirectory()
#
# open_file_button.bind('<Button-1>', openDirectory)
#
# def get_image(soup, url):
#     for link in soup.find_all('img'):
#         webpage_url = url
#         src = link.get('src')
#         new_url = urljoin(webpage_url, src)
#         resource = urllib.request.urlopen(new_url)
#         out = open(directory + "/" + new_url.split("/")[-1].split("?")[0], 'wb')
#         out.write(resource.read())
#         out.close()
#         soup = str(soup).replace(src, new_url.split("/")[-1].split("?")[0])
#     return str(soup)
#         #return src, new_url.split("/")[-1].split("?")[0]
#
# def recursiveUrl(url, depth):
#     if depth == int(depth_entry.get()):
#         return url
#     else:
#         page = urllib.request.urlopen(url)
#         soup = BeautifulSoup(page.read(), 'lxml')
#         #soup = get_image(soup, url)
#         #links_image = get_image(soup, url)
#         #print(links_image)
#         output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
#         output.write(get_image(soup, url))
#         newlink = soup.findAll('a', attrs={'href': re.compile("")}, limit=5)
#         if len(newlink) == 0:
#             return url
#         else:
#             for link in newlink:
#                 new_url_link = link.get('href')
#                 if new_url_link.startswith('http://'):
#                     return recursiveUrl(new_url_link, depth + 1)
#                 else:
#                     return recursiveUrl(urljoin(url, new_url_link), depth + 1)
#
#
# def getLinks(url):
#     links = [url]
#     page = urllib.request.urlopen(url)
#     soup = BeautifulSoup(page.read(), 'lxml')
#     get_image(soup, url)
#     #soup = get_image(soup, url)
#     output = open(directory + '/' + urlparse(url).hostname + '.html', 'w', encoding='utf-8')
#     output.write(get_image(soup, url))
#     for link in soup.findAll('a', attrs={'href': re.compile(urlparse(url).hostname + "/")}, limit=5):
#         new_url_link = link.get('href')
#         #links.append(recursiveUrl(new_url_link, 0))
#         if new_url_link.startswith('http://'):
#             links.append(recursiveUrl(new_url_link, 0))
#         else:
#             links.append(recursiveUrl(urljoin(url, new_url_link), 0))
#     return links

# def search_file():
#     os.chdir(directory)
#     for file in glob.glob("*.html"):
#         print(file)
#         soup = BeautifulSoup(file, 'lxml')
#         for link in soup.find_all('img'):
#             webpage_url = url
#             src = link.get('src')
#             new_url = urljoin(webpage_url, src)
#             resource = urllib.request.urlopen(new_url)
#             out = open(directory + "/file_saved/" + new_url.split("/")[-1].split("?")[0], 'wb')
#             out.write(resource.read())
#             out.close()
# soup = BeautifulSoup(str(soup).replace(src, new_url.split("/")[-1].split("?")[0]), 'lxml')


# def start(event):
#     getLinks(url)
#     #search_file()
# start_button.bind('<Button-1>', start)


# time_label.pack()
# url_label.pack()
# url_entry.pack()
# depth_label.pack()
# depth_entry.pack()
# open_file_button.pack()
# file_extension_label.pack()
# file_extension_entry.pack()
# start_button.pack()
# root.mainloop()
