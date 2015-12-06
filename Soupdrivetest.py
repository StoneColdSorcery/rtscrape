from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import re
import requests
from requests.exceptions import InvalidURL



'''
driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
'''

driver = webdriver.Firefox()
driver.get("http://www.rottentomatoes.com/browse/dvd-all/?services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;vudu&genres=2")
html_source = driver.page_source
driver.close()


soup = BeautifulSoup(html_source)
#print(soup.prettify()) 
try:
    for movietag in soup.find_all('div','mb-movie'):
        try:  
            mvinfotag = movietag.find('div','movie_info')
            mvtitle = mvinfotag.a.h3.string
            mvlink = mvinfotag.a.get('href')
            print('-' * 40)
            print('movie:',mvtitle)
            print('link:',mvlink)
        except Exception as e:
            print('caught exception in movietag processing:')
            repr(e) 
except Exception as e:
    print('genre outer exception:')
    repr(e)

'''
try:
    for tag in soup.find_all('div','body_main'):
        #print(tag.get('class'))
        for mctag in tag.find_all('div',id='main_container'):            
            for mctag2 in mctag.find_all('div',id='main-row'):                
                for mctag3 in mctag2.find_all('div',id='content-column'):         
                    for mctag4 in mctag3.find_all('div',id='movies-collection'):           
                        #print(mctag4)
                        for mctag5 in mctag4.find_all('div','mb-movies'):
                            
                            for movietag in mctag5.find_all('div','mb-movie'):
                            
                                try:  
                                    mvinfotag = movietag.find('div','movie_info')
                                    mvtitle = mvinfotag.a.h3.string
                                    mvlink = mvinfotag.a.get('href')
                                    print('-' * 40)
                                    print('movie:',mvtitle)
                                    print('link:',mvlink)
                                except Exception as e:
                                    print('caught exception in movietag processing:')
                                    repr(e) 
                                

except Exception as e:
    print('genre outer exception:')
    repr(e)
'''