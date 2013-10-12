#! /usr/bin/python

import re
import urllib2
import optparse
from urlparse import urljoin
from traceback import format_exc 
from Queue import Queue, Empty

from BeautifulSoup import BeautifulSoup, SoupStrainer

from getPageContent import getVisibleText
from removeWords import Filter
#from engine import MyEngine, MySchema TODO

class Crawler(object):
    """ A simple Web Crawler implementation keeping in mind the purpose of it""" 
    def __init__(self, options):
        self.starturl = options.starturl
        self.maxdeep = options.depth
        self.pattern = options.pattern
        self.visited = []  # Need to optimise this 
	self.queue = Queue()
        self.baseurl = options.baseurl
	self.count = 0 	
        self.filterwords = Filter()
        #self.engine =  MyEngine('indexdir', MySchema) TODO

    def crawl(self):
	self.visited.append(self.starturl)
        self.queue.put((self.starturl,0))
        while True:
            try:
                (url, level) = self.queue.get() 
		self.count += 1
		print "Level", level, ": ", self.count," :",url 
                if level == self.maxdeep:
                    break 
		self._getalllinks(url,level+1)
                if self.queue.empty():
                    break
            except Exception, e:
                print "ERROR: Can't crawl url to search '%s' (%s)" % (url, e)
                print format_exc()
    		break 	

    def _getalllinks(self, url, level=0):
	try:
            page = urllib2.urlopen(url).read() 
            soup = BeautifulSoup(page)
	except Exception, e:
            print "ERROR: Can't process url '%s' (%s)" % (url, e) 
	    print format_exc()
 	    raise
	try:
           text = getVisibleText(url, soup=soup, filter_obj=self.filterwords)
           final_text = text.strip('\n ')
           if final_text:
               print "Final text from this url : \n%s\n"%final_text
               #self.engine._add_document(content=unicode(final_text), path = unicode(url))
	except Exception, e:
            print "ERROR: Can't add url to search '%s' (%s)" % (url, e) 
	    print format_exc()
 	    return
        if self.pattern:
            link_pat = SoupStrainer('a', href=re.compile(self.pattern))
        else:
            link_pat = SoupStrainer('a')
        links = BeautifulSoup(page, parseOnlyThese=link_pat)
        for link in links:
            if not link.get('href', None):
                continue  
            url = link['href'].strip('/')
            url = urljoin(self.baseurl,url)
            check = url.split('/')
            if url not in self.visited and not check[-1].startswith('#'):  # found  while experimenting url=url/#comments
                self.queue.put((url, level))
 		self.visited.append(url)
            

#class WebPage:
#    def __init__(url,visible_text):
#        self.url = url
#        self.text = visible_text


def parse_options():
    "parse_options() -> opts, args" 
    parser = optparse.OptionParser(usage="usage: %prog -s <url> [options]",
				   version="%prog 1.0") 
    parser.add_option("-q", "--quiet",
		      action="store_true", default=False, dest="quiet",
	              help="Enable quiet mode")
    parser.add_option("-d", "--maxdepth",
		      action="store", type="int", default=3, dest="depth",
		      help="Maximum depth to traverse") 
    parser.add_option("-p", "--urlpattern",
                      action="store", type="string", default=None,\
		      dest="pattern", help="Crawler restricted to this pattern , for more than one pattern - pat1|pat2")
    parser.add_option("-s", "--starturl",
 	              action="store", type="string", default=None,\
		      dest='starturl', help="Start crawling from this url"\
		      "from this url")
    parser.add_option("-b","--baseurl",
                      action="store", type="string", default=None, dest="baseurl",
		      help="Append this string at the begining of incomplete url") 

    opts, args=parser.parse_args()
    if not opts.starturl:
       parser.print_help() 
       raise SystemExit, 1
    return opts, args


def main():
    opts, args=parse_options() 
    crawler = Crawler(opts)
    crawler.crawl() 

if __name__ == "__main__":
    main()
