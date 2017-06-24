
import requests
from bs4 import BeautifulSoup
import re


class entry:
    #Class to save each entry information

    def __init__(self, number, points, comments, tittle):

        self.number = number        #Number of the entry in the webpage
        self.points = points        #Points received by the entry
        self.comments = comments    #Comments received by the entry
        self.tittle =tittle         #Title of the entry

    def __str__(self):

        #Defines message for when a print(entry) function is called
        return ('Entry number: '+ str(self.number)+ ' Tittle: "'+ str(self.tittle)+ '" with '+ str(self.points)+' points'+ ' and '+ str(self.comments)+ ' comments')


def webCrawler():

    # Webcrawler that downloads the webpage
    web = requests.get('https://news.ycombinator.com/')

    return web


def extract(webPage):


    #Regex to extract relevant information
    num_r = re.compile(r'rank">(\d+)\.')
    com_r = re.compile(r'(\d+)&nbsp;comment|(discuss)')
    points_r = re.compile(r'(\d+) points')
    vote_r = re.compile(r'>\d+\.</span></td>      <td(.)')
    tittle_r = re.compile(r'storylink">(.*?)</a|nofollow">(.*?)</a')


    #Using the previously defined regex, extract the information
    num = re.findall(num_r,webPage.content.decode('utf-8'))
    pts = re.findall(points_r, webPage.content.decode('utf-8'))
    com = re.findall(com_r,webPage.content.decode('utf-8'))
    vote = re.findall(vote_r,webPage.content.decode('utf-8'))
    tittle = re.findall(tittle_r,webPage.content.decode('utf-8'))

    return (num,pts,com,vote,tittle)



def save(num,pts,com,vote,tittle):
     objs = list()  # list of objects to save the information
     dummy_com = ''
     dummy_tittle = ''

     # Loop to correct the information from different entries (There is always an entry without votes or comments
     # This loop also saves the tittle, votes, number and comments of each entry in an entry object in the list 'objs'
     for i in range(0, 30):
         if vote[i] == '>': pts.insert(i, 0); com.insert(i, [0,0])


         for j in com[i]:
             if j != '': dummy_com = j
             if dummy_com == 'discuss': dummy_com = 0  # If we have discuss instead of a number of comments then the entry has 0 comments

         for k in tittle[i]:
             if k != '': dummy_tittle = k

         objs.append(entry(num[i], pts[i], dummy_com, dummy_tittle))

     return objs


def sort(objs):
    more = list()
    less = list()

    #Divide entries by the number of words in the tittle
    for i in objs:
        if (len(i.tittle.split(' ')) > 5):
            more.append(i)
        if (len(i.tittle.split(' ')) <= 5):
            less.append(i)

    #Sort by comments and points
    more.sort(key=lambda x: int(x.comments), reverse=True)
    less.sort(key=lambda x: int(x.points), reverse=True)

    return (more, less)

if __name__ == "__main__":

    #Download the webpage
    webPage = webCrawler()

    #Take the relevant information of each entry (number of entry, points,comments and title)
    #The vote variable helps when correcting the list given that one entry does not have comments or points
    num,pts,com,vote,tittle = extract(webPage)

    #Save each entry as a'entry' object in a list
    entries = save(num,pts,com,vote,tittle)

    #Divide the entries by the number of words in the tittle (more or less/equal than five)
    #and sort them by number of comments and points respectively.
    more, less = sort(entries)



    print('Entries with more than five words by number of comments:\n')
    for i in more: print(i)

    print('--------------------------------------------------')

    print('Entries with less than five words by number of points:\n')
    for i in less: print(i)

    pass