import datetime
import webbrowser
import requests 
from bs4 import BeautifulSoup

def runescapeLookup (user, skill):

    constUrl = 'http://services.runescape.com/m=hiscore/compare?user1='
    userurl = constUrl + user
    dicty = ['total', 'attack', 'defence', 'strength', 'constitution', 'ranged', 'prayer', 'magic',  'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecrafting', 'hunter', 'construction', 'summoning', 'dungeoneering', 'divination', 'invention' ]
    skills = []

    rawHTMLForRsLookup = requests.get(userurl)
    parsedUserHTML = BeautifulSoup(rawHTMLForRsLookup.text, 'html.parser')
    filteredUserTable = parsedUserHTML.find('table', attrs={'class' : 'headerBgLeft'})
    filteredUserBody = filteredUserTable.find('tbody')
    filtereduserRows = filteredUserBody.find_all('tr')

    for row in filtereduserRows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        skills.append([ele for ele in cols if ele])

    for item in dicty:
        hehe = dict(zip(dicty, skills))
    if skill != 0:
        return hehe.get(skill)
    else:
        return hehe

def rsWikiLookup (lookup):
    constUrl = 'http://runescape.wikia.com/wiki/Special:Search?query='
    wikiurl = constUrl + lookup
    print (wikiurl)
    rawHTMLForWikiLookup = requests.get(wikiurl)
    parsedWikiHTML = BeautifulSoup(rawHTMLForWikiLookup.text, 'html.parser')
    filteredWikiHTML = parsedWikiHTML.find('ul', attrs={'class' : 'Results'})
    for link in filteredWikiHTML.find_all('a'):
        finalLink = (link.get('href'))
        return finalLink
    

