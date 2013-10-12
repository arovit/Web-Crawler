#!/usr/bin/python 

import re
import BeautifulSoup
import urllib
import sys
import sys
import removeWords

def processHTML(urlrequest):
    html = urllib.urlopen(urlrequest).read().decode('iso-8859-1').encode('utf-8')
    soup = BeautifulSoup.BeautifulSoup(html, smartQuotesTo=None)
    texts = soup.findAll(text=True)
    return texts


def processSoup(soup):
    #print "processing soup"
    texts = soup.findAll(text=True)
    return texts

def visible(texts, filter_obj):
    returnText = []
    global display
    for element in texts:
        if element.parent.name in ['option','legend', 'label', 'span', 'img','style','a','script', '[document]', 'License']:
            continue
        elif re.match('<!--.*-->', str(element)) or str(element).\
             startswith('DOCTYPE html PUBLIC') or str(element).startswith("http:"):
            continue
	elif str(element).strip().startswith('<') and str(element).strip().endswith('>') or  str(element).strip() == "" :
            continue
        #print "PARENT: %s"%element.parent.name , "ELEMENT:%s"%str(element)
        liststr = str(element).split("\n")
	liststr = cleanText(liststr) 
        liststr = filter_obj.remove_words(liststr)
        returnText.extend(liststr)
    return returnText

def cleanText(texts):
    #print "cleaning the text"
    indexText = []
    for word in texts:
        if not word in unWantedWords:
            word = re.sub(r"&#?\d*[a-zA-Z]*;",'',word) # Remove coded values
            word = word.strip('\t\r\f[]\./{}()') 
            #print "After stripping",word  
            indexText.append(word)
    return indexText

def getVisibleText(readthisurl, soup=None, filter_obj = None):
    #print "reading ",readthisurl
    global unWantedWords
    global display
    if not  filter_obj:
        filter_obj = removeWords.Filter()
    unWantedWords = ['.', ',', 'the', 'to', 'a', 'an']
    if soup:
        display = False
        indexText = '\n'.join(visible(processSoup(soup), filter_obj))
    else:
        display = True
        indexText = '\n'.join(visible(processHTML(readthisurl), filter_obj))
    print "final",indexText
    return indexText


if __name__ == "__main__":
    global display
    getVisibleText(readthisurl=sys.argv[1])
