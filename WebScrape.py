import requests
from bs4 import BeautifulSoup
import pickle

# Get all available languages
languages = []
links = []

url = 'https://1000mostcommonwords.com/languages/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
li = soup.select("#content ul > li > a")

for i in li:
    links.append(i.get('href'))
    languages.append(i.text.lower())


# Scrape tables
list_dict = {}
english_dict = {}

for url, language in zip(links, languages):
    word_list = []
    translation_list = []

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table')

    for word in table.find_all('tbody'):
        rows = word.find_all('tr')

        for row in rows:
            element = row.find_all('td')
            word_list.append(element[1].text)
            translation_list.append(element[2].text)

    word_list = word_list[1:]
    translation_list = translation_list[1:]

    list_dict[language] = word_list
    english_dict[language] = translation_list

file = open('data.pkl', 'wb')
pickle.dump({'Original': list_dict, 'Translations': english_dict}, file)
file.close()