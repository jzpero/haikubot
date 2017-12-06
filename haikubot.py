from bs4 import BeautifulSoup
import urllib2
from textstat.textstat import textstat
import re
import random

def make_haiku(artist):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    req = urllib2.Request('https://genius.com/artists/{}'.format(artist.replace(' ', '-')), headers=headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    #with open('soup.txt','w') as out:
    #    out.write(soup.prettify().encode('utf-8'))

    artist_song_links = []
    for card in soup.findAll('a', {'class': 'mini_card'}):
        artist_song_links.append(card.get('href'))
    #print artist_song_links

    five_list = []
    seven_list = []

    for song_page in artist_song_links:
        #print song_page
        song_req = urllib2.Request(song_page, headers=headers)
        song_response = urllib2.urlopen(song_req)
        html = BeautifulSoup(song_response, 'html.parser')
        [h.extract() for h in html('script')]
        lyrics = html.find("div",class_="lyrics").get_text().encode('utf-8').strip().split('\n')
        for line in lyrics:
            bad = False
            #for profanity in profanities:
            #    if profanity.upper() in line.upper():
            #        bad = True
            #        break
            if '[' in line or ']' in line:
                bad = True
            if len(line) == 0:
                bad = True
            if not bad:
                words = re.findall(u'[A-z\']+',line)
                n = 0
                for word in words:
                    n += textstat.syllable_count(word)
                #print line, n
                if n == 5:
                    five_list.append((line, n))
                if n == 7:
                    seven_list.append((line,n))

    if len(five_list) >= 2 and len(seven_list) >= 1:
        five_pick_one = random.randint(0,len(five_list)-1)
        five_pick_two = random.randint(0, len(five_list) - 1)
        while five_pick_two == five_pick_one:
            five_pick_two = random.randint(0, len(five_list) - 1)
        return '\n'.join([five_list[five_pick_one][0], seven_list[random.randint(0, len(seven_list) - 1)][0], five_list[five_pick_two][0]])

print make_haiku("Gallant")
