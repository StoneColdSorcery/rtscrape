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
        for i,rv in enumerate(self.reviews[:130]):
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



class Movie(object):
    
    def __init__(self,movie_hp):
        self.reviewsURL_topCritics = movie_hp + "/reviews/?type=top_critics"
        self.reviewMap = {}
        try:
            self.movieName = movie_hp.split('/')[-1]
        except Exception as e:
            print('ERROR extracting name')
            repr(e)
            self.movieName = "NAMENOTFOUND"
        r  = requests.get(self.reviewsURL_topCritics)

        data = r.text
        mvsoup = BeautifulSoup(data)
        
        for rowtag in mvsoup.find_all('div','review_table_row'):
            desc = rowtag.find('div','review_desc')
            try:
                rvwLink = desc.find('a').get('href')
            except Exception as e:
                rvwLink = 0
                repr(e)
            #print(rvwLink)
            cname = rowtag.find('div','critic_name').a.string
            
            #print('-' * 45)
            self.reviewMap[cname] = rvwLink
        

    
    def __str__(self):
        try:
            lctemp =  self.movieName.split('_')[0] + " " +  self.movieName.split('_')[1] +' - ' + self.movieName.split('_')[2]
            return lctemp
        except Exception as e:
            repr(e)
            return "OBJECTNAME"
    
    def getMovieInfo(self):
        #extract movie info
        pass
         
        
            
    def printReviewMap(self):
        
        for k in self.reviewMap:
            print('Critic: ',k, " Link: ", self.reviewMap[k])
        print('\n')
        print('-' * 45)    
        print('Found',len(self.reviewMap) ,'reviews for ', self )
        print('-' * 45)

def getTextFromReview(rlink):
    
    tr  = requests.get(rlink)

    tdata = tr.text
    tsoup = BeautifulSoup(tdata)
    
    for par in tsoup.find_all('p'):   
        try:
            print(par.string)
        except Exception as e:
            repr(e)

'''
InsideOut = Movie("http://www.rottentomatoes.com/m/inside_out_2015")
#InsideOut.printReviewMap()
print(InsideOut)
tempdict = InsideOut.reviewMap
tkeys = tempdict.keys()
#getTextFromReview(tempdict['Wesley Morris'])




'''
url = "http://www.rottentomatoes.com/m/inside_out_2015/"


r  = requests.get(url)

data = r.text
soup = BeautifulSoup(data)

for tag in soup.find_all('table','info'):
    #print(tag)
    for inforow in tag.find_all('tr'):
        #print(inforow)
        try:
            for infolink in inforow.find_all('a'):
                print('tag:',infolink.span.get('itemprop'),', value:',infolink.span.string)
        except Exception as e:
                repr(e)

