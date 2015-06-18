'''
Created on Jun 15, 2015

@author: Crazyfingers
'''
from bs4 import BeautifulSoup

import re
import requests
import urllib

rvwTableClass = 'table-striped'





'''


class Review(object):
    
    def __init__(self,trow):
        
        if(len(trow) != 3):
            raise ValueError
        
        self.verdictSpan = trow[0].find('span')
        self.fOrR = self.verdictSpan.find('span').get('title')
        self.tomatoScore = self.verdictSpan.find('span','tMeterScore').string
        self.MovieTitle = trow[2].a.string
        self.rvwLink = trow[3].a.get('href')
    
    
    def printInfo(self):
    
        print("-" * 24)
        print("Movie: ",self.MovieTitle)
        print("Verdict: ",self.fOrR)
        print("Tmeter Score: ",self.tomatoScore)
        print("Review Link: ",self.rvwLink)
    



# class for holding this critic's reviews and some metadata 
class Critic(object):

    def __init__(self,name,homepage):
        self.name = name
        self.hp_url = homepage
        self.reviews = []
        
        r  = requests.get("http://" + homepage)
        data = r.text
        self.soup = BeautifulSoup(data)
        
        #find td elements of class 'center'
        #then look sideways to get the other 
        # tds in the row
        centds = self.soup.find_all('td','center') 
        
        parsedRows = [] #list for parsed row tags
        
        for td in centds:
            print("href of center td: ",td.a.get('href'))
            for nxt in td.findNext('td'):
                print("contents of the findallnext: ",nxt.contents)     
                mlink = td
                rvwtxt = td.findNext('td')
                tverdict = td.findPrevious('td')
                tscore = tverdict.findPrevious('td')
                parsedRows.append((tverdict,tscore,mlink,rvwtxt))
                print(parsedRows[len(parsedRows) - 1])
        
        for r in parsedRows:
            try:
            
                tempRowOject = Review(r)
                self.reviews.append(Revi)
            except Exception as E:
                print('Exception creating review objects: ', E)
            
            
            
    def printVerdicts(self):
        for r in self.reviews:
            r.printInfo()
        
    
    def add_review(self,rvw):
        #LBYL, replace this with exception
        if (isinstance(rvw, Review)):
            self.reviews.append(rvw) #add review object to this critic
        else:
            print("Object: ",rvw," is not a Review Object")




url = "www.rottentomatoes.com/critic/david-rooney/"


critic1 = Critic('David',url)

critic1.printVerdicts()
#look for 


'''

#url = "www.rottentomatoes.com/critic/david-rooney/?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=2"
baseurl = "www.rottentomatoes.com"
pageurl = "/critic/david-rooney/"
r  = requests.get("http://" +baseurl+ pageurl)

data = r.text

soup = BeautifulSoup(data)

nexttag = soup.find('a',text='Next')
print(nexttag.get('href'))
r  = requests.get("http://" +baseurl+ pageurl)
try:
    while(1):
        
        data = r.text
        soup = BeautifulSoup(data)
        nexttag = soup.find('a',text='Next')
        nextpagelink = nexttag.get('href')
        nextpageurl = "http://" +baseurl+ nextpagelink
        print(nextpageurl)
        r  = requests.get(nextpageurl)
except Exception as e:
    print("exception:",e)

centds = soup.find_all('td','center')



'''
cmprows = []
try:
    for td in centds:
        print("href of center td: ",td.a.get('href'))
        #for nxt in td.findNext('td'):
            #print("contents of the findnext: ",nxt.contents)     
        mlink = td
        rvwtxt = td.findNext('td')
        tverdict = td.findPrevious('td')
        tscore = tverdict.findPrevious('td')
        cmprows.append((tverdict,tscore,mlink,rvwtxt))
        print(cmprows[len(cmprows) - 1])
except Exception as E:
    print("caught loopy error",E)


nReviewsParsed = len(cmprows)
for trow in cmprows:
    
    verdictSpan = trow[0].find('span')
    try:
        tomatoScore = verdictSpan.find('span','tMeterScore').string
    except AttributeError:
        tomatoScore = 'NA'    
    
    #fOrR = verdictSpan.find('span').get('title')
    try:
        fOrR = trow[1].find('span').get('class')[2] #3rd string in class attr is fresh/rotten
    except AttributeError:
        fOrR = 'VerdictError'   

    MovieTitle = trow[2].a.string
    rvwLink = trow[3].a.get('href')
    
    print("-" * 24)
    print("Movie: ",MovieTitle)
    print("Verdict: ",fOrR)
    print("Tmeter Score: ",tomatoScore)
    print("Review Link: ",rvwLink)

print("-" * 50)
print("Parsed ",nReviewsParsed, "reviews")
#print(soup.find(id="criticsReviewsChart_main"))
# for link in soup.find(id="criticsReviewsChart_main")
#     #print(link.get('href'))
#     print(link)
    
'''