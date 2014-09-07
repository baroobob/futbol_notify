"""
Module for retrieving a web page's source
"""

import sys
import urllib.request
from bs4 import BeautifulSoup

  #url = 'http://espn.go.com/watchespn/index/_/startDate/'
if len(sys.argv) > 1: 
  url = sys.argv[1]
else:
  print("Please provide a full URL as an argument.")
  exit()

# get the web page source
try:
  page = urllib.request.urlopen(url)
except:
  print("Unable to open " + url + ".  Did you provide the FULL URL?")
  exit()
  
# parse the spaghetti mess of html
soup = BeautifulSoup(page)

# make the source more human readable
print(soup.prettify())

