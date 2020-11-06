from bs4 import BeautifulSoup
import urllib.request


#url = 'http://geocitiessites.com/CapeCanaveral/launchpad/1364/Stars.html'
url = 'http://odeku.edu.ua/language/en/osenu-2/'
def recursiveUrl(url, depth):
    if depth == 5:
        return url
    else:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read())
        newlink = soup.find('a')  # find just the first one
        if len(newlink) == 0:
            return url
        else:
            return url, recursiveUrl(newlink, depth + 1)


def getLinks(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'lxml')
    links = soup.find_all('a', {'class': 'institution'})
    for link in links:
        links.append(recursiveUrl(link, 0))
    return links
print( getLinks(url))