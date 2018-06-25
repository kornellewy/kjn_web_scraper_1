# imprts
from bs4 import BeautifulSoup
import requests
import operator
import re
import json
# form list of list make 1 table
from tabulate import tabulate
import sys
# library for disposal without valuable words
from stop_words import get_stop_words

# get data from link (default wiki)
wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"

if (len(sys.argv)<2):
    print('Enter valid string')
    exit()

# get search word
string_query = sys.argv[1]
# remove stop words
if(len(sys.argv) > 2):
    search_mode = True
else:
    search_mode = False

# create URL
url = wikipedia_api_link + string_query

try:
    response = requests.get(url)
    data = json.loads(response.content.decode('utf-8'))
    # format this data
    wikipedia_page_tag = data['query']['search']['0']['title']
    # create new URL
    url = wikipedia_link + wikipedia_page_tag







print("koniec pleców")
