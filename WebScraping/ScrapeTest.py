from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
import re
import random
import datetime
import lxml
import time
import csv

#lxml also a html parser
#html5lib is html parser

random.seed(datetime.datetime.now())

class product:
    def __init__(self, name, price, sold, lastDay, link):
        self.name = name
        self.price = price
        self.sold = sold
        self.link = link
        self.lastDay = lastDay
        self.numSold = int(sold.split()[0].replace(',',''))
        self.comp = int(float(price.replace(',',''))*self.numSold)
    
    def __str__(self):
        return str(self.name) + "\n" + str(self.price) + "\n" + str(self.sold) + "\n" + str(self.lastDay) + "\n" + str(self.comp) + "\n" + str(self.link)

f = open('output', 'w')

def search(item):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=' + item.replace(' ','_') + '&_sacat=0'
    return url

#print(search('mug'))
#input() reads from stdin
#print(bs1.find_all('ul', {'class':{'srp-results srp-grid clearfix'}}))

#test = bs1.find_all('ul')

#items = bs1.find_all('ul', {'class':{'srp-results srp-grid clearfix'}})
#ul = bs1.find_all('ul', {'class':{'srp-results srp-grid clearfix'}})
#tester = bs1.find_all('li', class_="s-item")
#for c in ul:
#    for j in c.find_all('li', class_="s-item"):
#        print(j)
#        print("-"*20)
        
#<h1 class="it-ttl" itemprop="name" id="itemTitle"><span class="g-hdn">Details about  &nbsp;</span>THE NORTH FACE Venture Men's Rain Jacket TNF BLACK-TNF WHITE sz S - XXL MSRP $99</h1>
        
def processItem(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
#    print(bs)
#    print(bs.find_all('h1'))
#    return
    name = bs.find('h1', itemprop="name", id="itemTitle").text[16:]
    price = bs.find_all(['span'], class_='notranslate', itemprop='price')[0].attrs['content']
    sold = bs.find_all('a', class_='vi-txt-underline')
    if len(sold) == 0:
        sold = "0 sold"
    else:
        sold = bs.find_all('a', class_='vi-txt-underline')[0].text
    lastDay = bs.find_all('span', style="font-weight:bold;")
    if len(lastDay) == 0:
        lastDay = "None Sold"
    else:
        lastDay = str(lastDay[0].text.split()[0]) + " " + str(lastDay[0].text.split()[1])
    #can be zero
    result = product(name, price, sold, lastDay, url)
    return result
    print(name, price, sold, lastDay[0].text.split()[0:2])
    
#processItem('https://www.ebay.com/itm/THE-NORTH-FACE-Venture-Mens-Rain-Jacket-TNF-BLACK-TNF-WHITE-sz-S-XXL-MSRP-99/133396007573?hash=item1f0f058a95:m:mzcrbNK94PjXsVmgWbK3Iig')
items = []

counter = 0
def processPage(url, page):
    global counter
    if page == 1:
        return 1
        
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')    
    listItems = bs.find_all('ul', class_= re.compile("(srp-results srp-)(grid|list)( clearfix)"))[0].find_all('li', class_="s-item")

    #print(len(listItems))
    pattern = re.compile("(https://www.ebay.com/itm/)([A-Za-z0-9\-])*[/][0-9]+[?]((epid=[0-9]+)*&*)(hash=item)([0-9A-Za-z]|:|_|~|-)+")
    #counter = 0
    for item in listItems:
#        if counter == 10:
#            break
        x = item.find_all("a", class_="s-item__link")
        for j in x:
            if pattern.match(j.attrs["href"]):
                #print(j.attrs["href"])
                counter += 1
                #print('-'*20, ' ', counter)
                items.append(processItem(j.attrs["href"]))
                #items.append(j.attrs["href"])
#                f.write(str(j.attrs["href"]))
#                f.write('\n\n')
#                f.write('-'*20+ ' '+ str(counter) + '\n\n')
    
    nextPage = bs.find_all('a', class_="pagination__next")
    #print(len(nextPage), nextPage[0].attrs["href"])
    processPage(nextPage[0].attrs["href"], page+1)

def comparator(a, b):
    if a.comp == b.comp:
        return a.numSold < b.numSold
    return a.comp < b.comp
    
def mergeSort(array, l, r):
    if r - l <= 2:
        if comparator(array[l], array[r]):
            array[l], array[r] = array[r], array[l]
        return
        
    mid = (l+r)//2
    mergeSort(array,l, mid)
    mergeSort(array, mid+1,r)
    merge(array, l, mid+1, r)
    
def merge(array, l, m, r):
    temp = []
    a = l
    b = m
    while (a < m or b <= r):
        if a == m:
            temp.append(array[b])
            b += 1
        elif b > r:
            temp.append(array[a])
            a += 1
        elif comparator(array[a], array[b]):
            temp.append(array[b])
            b += 1
        else:
            temp.append(array[a])
            a += 1
    for i in range(len(temp)):
        array[i+l] = temp[i]
            
processPage(search(str(input())), 0)
#print(len(items))

mergeSort(items, 0, len(items)-1)
    
#processItem('https://www.ebay.com/itm/Portwest-US440-Classic-Waterproof-Rain-Jacket-wth-Pack-Away-Hood-Sealed-Seams/262823792213?hash=item3d3184ce55:m:muzP4u8iql29rLuFHzqlOhQ')

for i in items:
    print(i)
    print("-"*20, "\n\n")

f.close()
exit()

def validSite(url):
    try: 
        html = urlopen(url)
        return True
    except HTTPError as e:
        return False
    except URLError as e:
        return False
    

#https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=jackets&_sacat=0

