import requests
import sqlite3 as sql
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

url="https://www.etsy.com/in-en/listing/171816901/12-carat-gold-diamond-earrings-14k-white?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-8&frs=1"
browser = webdriver.Firefox(executable_path="C:\\Users\Shubh K\geckodriver.exe")
browser.get(url)
user_agent = {'User-agent': 'Firefox'}
source = requests.get(url ,headers = user_agent).text
soup = BeautifulSoup(source,"lxml")

X=[] 
page= browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a')

for j in range (0,14):
    
    for i in range(0,4):
        review_part=browser.find_element_by_xpath('//*[@id="review-preview-toggle-'+str(i)+'"]')        
        X.append(review_part.text.strip())
        
    #myreviewxpath//*[@id="review-preview-toggle-0"]
    page= browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a')
    page.click()                         
    sleep(5)


import pandas as pd

df1 =pd.DataFrame()
df1['reviews_df'] = X
df1.to_csv('newreview.csv', index = False)
conn = sql.connect('newreview.db')
df1.to_sql('review', conn , index=False)
cursor = conn.cursor()

cursor.execute("SELECT * FROM review")
for record in cursor:
    print (record)
