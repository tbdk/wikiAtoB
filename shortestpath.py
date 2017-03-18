##############################################
###### Script by Tobias ######################
###### http://github.com/tbdk ################
##############################################

# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import time
from datetime import timedelta
import winsound

start_time = time.monotonic()
MAX_DEPTH = 2		# max "depth" we're willing to look for a specific article, to minimize excess traverse.
CUR_DEPTH = 0		# the current number of articles "down" the program is / current depth.
PATH = []
pagesVisited = set() # a collection of all articles already visited, to keep progress from going backwards.



def getArticleObj(articleUrl):
  """Returns an article as a beautifulsoup object"""
  try:
  	html = urlopen("https://en.wikipedia.org" + articleUrl)
  except URLError as e:
    print("Something's wrong with the Url: " + articleUrl)
    return e
    
  bsObj = BeautifulSoup(html, "html.parser")
  return bsObj

def traverse_path(linkObj):
	global MAX_DEPTH, CUR_DEPTH, PATH, start_time, end_time

	articleUrl = linkObj.attrs["href"]
	try:
		html = urlopen("https://en.wikipedia.org" + articleUrl)
	except URLError as e:
		print("Something's wrong with the Url: " + articleUrl)
		return e

	articleObj = BeautifulSoup(html, "html.parser") # without "html.parser" it throws a complaint.
	# we're only interested in internal links starting with "wikipedia.org/wiki/"
	links = articleObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")) 
	title = articleObj.title.get_text()
	pagesVisited.add(articleUrl)
	PATH.append(articleUrl + " -> ")

	# feedback
	print("*******************************")
	print(title)
	print(articleUrl)
	print("CURRENT DEPTH: " + str(CUR_DEPTH)) # feedback
	print("PATH: ", PATH)
	end_time = time.monotonic()
	print("RUNTIME: " + str(timedelta(seconds=end_time - start_time)))
	
	if title == dest_article_title:
		print("We found it! WE FOUND IT!!! WUUUHUUUUUUUU!")
		print("It was " + str(CUR_DEPTH) + " deep!")
		end_time = time.monotonic()
		print("And it only took: " + str(timedelta(seconds=end_time - start_time)))
		#winsound.Beep(500,10000)
		quit()
	elif CUR_DEPTH == MAX_DEPTH:
		print("We're too deep, this is taking us nowhere... Getting back on track...")
		CUR_DEPTH = CUR_DEPTH - 1 # depth at previous article
		del PATH[-1]
		return
	else:
		for linkObj in links:
			if linkObj.attrs["href"] in pagesVisited:
				return
			else:
				CUR_DEPTH = CUR_DEPTH + 1 # going one article deeper.
				traverse_path(linkObj)


mainArticleUrl = "/wiki/John_Locke"
mainArticle = getArticleObj(mainArticleUrl) # Start article
main_article_title = mainArticle.title.get_text() # format: "Kevin Bacon - Wikipedia"
links = mainArticle.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
pagesVisited.add(mainArticleUrl)

destArticle = getArticleObj("/wiki/Philosophy")
dest_article_title = destArticle.title.get_text()

for linkObj in links:
	if linkObj.attrs["href"] in pagesVisited:
		pass
	else:
		link = linkObj.attrs["href"]
		pagesVisited.add(link)
		CUR_DEPTH = 0
		PATH = []
		PATH.append(mainArticleUrl + " -> ")
		traverse_path(linkObj)
 