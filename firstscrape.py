'''
Created on Jun 15, 2015

@author: Crazyfingers
'''
from bs4 import BeautifulSoup

import re
import requests
import urllib

rvwTableClass = 'table-striped'








class Review(object):
    
    def __init__(self,tablerow):
        try:
            self.tverdict = tablerow.contents[0].span.get('class')
        except Exception as E:
            print('exception initializing review object: ',E)
            self.tverdict = 'none'




# class for holding this critic's reviews and some metadata 
class Critic(object):

    def __init__(self,name,homepage):
        self.name = name
        self.hp_url = homepage
        self.reviews = []
        r  = requests.get("http://" +url)
        data = r.text
        self.soup = BeautifulSoup(data)
        
        for tbl in self.soup.find_all('table',rvwTableClass):
            try:
                print(len(tbl)," : ",tbl.get('class'), " : ",tbl.parent)
                self.rvwTableBody = tbl.tbody
            except Exception as E:
                print('Exception in find table loop: ', E)
                self.rvwTableBody = 0
        #create review objects from rows of rvwTableBody
        try:
            self.reviews = [Review(r) for r in self.rvwTableBody.find_all('tr')]
        except Exception as E:
            print('Exception creating review objects: ', E)
            
            
            
    def printtverdicts(self):
        for r in self.reviews:
            print(r.tverdict)
        
    '''
    def add_review(self,rvw):
        #LBYL, replace this with exception
        if (isinstance(rvw, Review)):
            self.reviews.append(rvw) #add review object to this critic
        else:
            print("Object: ",rvw," is not a Review Object")
    '''


url = "www.rottentomatoes.com/critic/david-rooney/"


#critic1 = Critic('David',url)

#critic1.printtverdicts()
#look for 

        

#url = "www.rottentomatoes.com/critic/david-rooney/?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=2"
url = "www.rottentomatoes.com/critic/david-rooney/"
r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)

centds = soup.find_all('td','center')[30:36]
cmprows = []
try:
    for td in centds:
        print("href of center td: ",td.a.get('href'))
#         for nxt in td.findNext('td'):
#             print("contents of the findallnext: ",nxt.contents)     
        mlink = td
        rvwtxt = td.findNext('td')
        tverdict = td.findPrevious('td')
        tscore = tverdict.findPrevious('td')
        cmprows.append((tverdict,tscore,mlink,rvwtxt))
        print(cmprows[len(cmprows) - 1])
except Exception as E:
    print("caught loopy error",E)

for trow in cmprows:
    
    verdictSpan = trow[0].find('span')
    fOrR = verdictSpan.find('span').get('title')
    tomatoScore = verdictSpan.find('span','tMeterScore').string
    MovieTitle = trow[2].a.string
    rvwLink = trow[3].a.get('href')
    
    print("-" * 24)
    print("Movie: ",MovieTitle)
    print("Verdict: ",fOrR)
    print("Tmeter Score: ",tomatoScore)
    print("Review Link: ",rvwLink)
#print(soup.find(id="criticsReviewsChart_main"))
# for link in soup.find(id="criticsReviewsChart_main")
#     #print(link.get('href'))
#     print(link)
    
