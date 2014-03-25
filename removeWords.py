#! /usr/bin/python

import re

# remove these words before indexing, this depends upon the what we are interested in   


class Filter:
    """ Class to filter out words that we are not interested in """
    def __init__(self):
        self._regex_pats = []
        list = ['TOP 10', 'The latest articles', '\d+[-.]\d+[-.]\d+',\
            'Search', 'you can do a relevance descending search for two or more search criterion',\
            'Your search criterion has to be at least 4 letters long otherwise your request will be rejected', \
            'Keyword', 'powered by', 'Navigation', 'Users online' , 'With an entry like', \
            'All rights reserved','You can','Template/CSS by', 'phpMyFAQ logo by','\d+ out of \d+',\
            'Your proposal will not be published right away, but will be released by the administrator upon receipt',\
            'Notice:','webmaster','word1','word2','Ask your question','Please separate the keywords with space only',\
            'Tags','completely useless','Questions in','Average rating','ID #\d+','Categories with entries','Records in this category','Help','Contact \d+',\
            'The structure of the FAQ','Related entries','Revision','You can either search the or let the search for keywords','Propose a translation for',\
            'SEO powered by','completely useless','most valuable','views','\d+ views:','Proposal for FAQ','under the','\d+ Entries','Infra FAQ','powered by phpMyFAQ']
        for regex in list:
            self._regex_pats.append(re.compile(regex))

    def remove_words(self, rawtext):
	clean_text = []
        for text in rawtext:
            text = text.strip()
            for pat in self._regex_pats:
                if ((pat.search(text) or len(text) < 2)):
                   break
                if not re.search(r'\w',text):
                   break
	    else:
                clean_text.append(text)
	#print "Filter %s"%clean_text
        return clean_text
