'''
Created on Jun 15, 2015

@author: Crazyfingers
'''
from bs4 import BeautifulSoup

import re
import requests
from requests.exceptions import InvalidURL

rvwTableClass = 'table-striped'
siteurl = "http://www.rottentomatoes.com"







class Review(object):
    
    RowSize = 4
    #number of tds to expect in a row struct
    
    def __init__(self,trow):
        
        if(len(trow) != self.RowSize):
            print("ERROR: input trow has length: ".len(trow))
            print("Review object not created")
            raise ValueError
            
        try:
            verdictSpan = trow[0].find('span')
            self.tomatoScore = verdictSpan.find('span','tMeterScore').string
        except (AttributeError, IndexError) as e:
            self.tomatoScore = 'NA'   
            print("In Review init: Error creating tscore") 
            repr(e)
        #fOrR = verdictSpan.find('span').get('title')
        try:
            self.fOrR = trow[1].find('span').get('class')[2] #3rd string in class attr is fresh/rotten
        except (AttributeError, IndexError) as e:
            self.fOrR = 'VerdictError'   
            print("In Review init: Error creating fOrR") 
            repr(e) 
        try:
            self.MovieTitle = trow[2].a.string
        except (AttributeError, IndexError) as e:
            self.MovieTitle = 'NoTitleFound'
            print("In Review init, Error creating movietitle",) 
            repr(e)
        try:
            self.rvwLink = trow[3].a.get('href')
        except (AttributeError, IndexError) as e:
            self.rvwLink = 'NoLink'
            print("In Review init: Error creating rvwlink") 
            repr(e)
    
    def printInfo(self):
    
        print("-" * 24)
        print("Movie: ",self.MovieTitle)
        print("Verdict: ",self.fOrR)
        print("Tmeter Score: ",self.tomatoScore)
        print("Review Link: ",self.rvwLink)
    



# class for holding this critic's reviews and some metadata 
class Critic(object):

    def __init__(self,homepage):
        
        try:
            self.name = homepage.split('/')[2]
        except:
            self.name = "NAME UNKNOWN"

        self.hp_url = siteurl + homepage 
        self.reviews = []
        
        
        
        

        r  = requests.get(self.hp_url)
        
        try:
            while(True): 
            #iterate through column pages until an invalid link exception is thrown
            
                data = r.text
                soup = BeautifulSoup(data)
                
                #find td elements of class 'center'
                #then look sideways to get the other 
                # tds in the row
                centds = soup.find_all('td','center') 
                
                parsedRows = [] #list for parsed row tags
                
                for td in centds:
                    print("href of center td: ",td.a.get('href'))
             
                    mlink = td
                    rvwtxt = td.findNext('td')
                    tverdict = td.findPrevious('td')
                    tscore = tverdict.findPrevious('td')
                    parsedRows.append((tverdict,tscore,mlink,rvwtxt))
                    #print(parsedRows[len(parsedRows) - 1])
                
                for i,rt in enumerate(parsedRows):
                    try:
                    
                        tempRowObject = Review(rt)
                        self.reviews.append(tempRowObject)
                    except Exception as E:
                        print('At i = ',i,'Exception creating review object: ', E)
                
                nexttag = soup.find('a',text='Next')
                nextpagelink = nexttag.get('href')
                nextpageurl = siteurl + nextpagelink
                print(nextpageurl)
                r  = requests.get(nextpageurl)
                        
        except (InvalidURL,AttributeError) as InvalidLinkEx:
                print("Exiting table parse iteration with: ",repr(InvalidLinkEx))
                    
                
            
    def printVerdicts(self):
        for i,rv in enumerate(self.reviews):
            print(i)
            rv.printInfo()
            
    def printSummary(self):
        print('\n')
        print("=" * 40)
        print("Critic Summary",20 * '-')
        print("=" * 40,'\n')
        print('Name: ',self.name)
        print("Number of Reviews: ", len(self.reviews))
        print("=" * 40,'\n')
    
    def add_review(self,rvw):
        #LBYL, replace this with exception
        if (isinstance(rvw, Review)):
            self.reviews.append(rvw) #add review object to this critic
        else:
            print("Object: ",rvw," is not a Review Object")




url = "http://www.rottentomatoes.com/critic/david-rooney/"


critic1 = Critic("/critic/david-rooney/")

critic1.printVerdicts()
critic1.printSummary()
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