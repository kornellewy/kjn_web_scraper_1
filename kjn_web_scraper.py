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

# get the words
def getWordList(url):
    word_list = []
    # raw data
    sorce_code = requests.get(url)
    # convert to txt
    plain_text = sorce_code.text
    # lxml format
    soup = BeautifulSoup(plain_text, 'lxml')

    # find words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        # content
        content = text.text
        # lower case  and split in to arrey
        words = content.lower().split()
        for word in words:
            # remove non-chars
            cleaned_word = clean_word(word)
            if len(cleaned_word) > 0:
                word_list.append(cleaned_word)

    return word_list

# clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def createFrequenctTable(word_list):
    # word count
    word_count = {}
    for word in word_list:
        # index is word
        if word in word_count:
            word_count[word] +=1
        else:
            word_count[word] =1

    return word_count

# remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')
    temp_list = []
    for key, value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list

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
    wikipedia_page_tag = data['query']['search'][0]['title']
    # create new URL
    url = wikipedia_link + wikipedia_page_tag
    page_word_list = getWordList(url)
    # create table of word counts
    page_word_count = createFrequenctTable(page_word_list)
    sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
    # remove stop words
    if (search_mode):
        sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    # sum the total words to calculate the frequencies
    total_words_sum = 0
    for key, value in sorted_word_frequency_list:
        total_words_sum = total_words_sum + value

    # we get top 20 words
    if len(sorted_word_frequency_list) > 20:
        sorted_word_frequency_list = sorted_word_frequency_list[:20]

    # create our final list, words + frequency + percentage
    final_list = []
    for key, value in sorted_word_frequency_list:
        percentage_value = float(value * 100) / total_words_sum
        final_list.append([key, value, round(percentage_value, 4)])

    print_headers = ['Word', 'Frequency', 'Frequency Percentage']

    # print the table with tabulate
    print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

except requests.exceptions.Timeout:
    print("The server didn't respond. Please, try again later.")
