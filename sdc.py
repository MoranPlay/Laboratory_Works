import re

from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.tigerlillies.com'
# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page.read(), 'lxml')
# for link in soup.findAll('a', attrs={'href': re.compile("http://" or "https://")}, limit=23):
#         print(link.get('href'))

def recursiveUrl(url, depth):
    if depth == 5:
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        newlink = soup.findAll('a', attrs={'href': re.compile("http://" or "https://")})
        #print(newlink)

        if len(newlink) == 0:
            return url
        else:
            for link in newlink:
                return recursiveUrl(link.get('href'), depth + 1)


def getLinks(url):
    links = []
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    #print(soup)
    #links = soup.find_all('a', limit=3)
    for link in soup.findAll('a', attrs={'href': re.compile("http://" or "https://")}):
        links.append(recursiveUrl(link.get('href'), 0))

    return links
#getLinks(url)
print(getLinks(url))



# page = urllib.request.urlopen(link.get('href'))
#         soup1 = BeautifulSoup(page.read(), 'lxml')
#         for link1 in soup1.find_all('a', limit=2)[1:]:
#             print(link1)
#             links.append(recursiveUrl(link1.get('href'), 0))
#         #print(link.get('href'))