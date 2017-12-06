from bs4 import BeautifulSoup
import urllib2
from textstat.textstat import textstat
import re
import random

from nltk.corpus import cmudict
d = cmudict.dict()


def nsyl(word):
    if d.has_key(word.lower()):
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    return textstat.syllable_count(word)

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }

def get_artist_song_links(artist):
    req = urllib2.Request(
        'https://genius.com/artists/{}'.format(artist.replace(' ', '-')), headers=headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    artist_song_links = []
    for card in soup.findAll('a', {'class': 'mini_card'}):
        artist_song_links.append(card.get('href'))
    return artist_song_links

def get_lyrics(song_page):
    song_req = urllib2.Request(song_page, headers=headers)
    song_response = urllib2.urlopen(song_req)
    html = BeautifulSoup(song_response, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text().encode('utf-8').strip().split('\n')
    return lyrics

def make_haiku(artist):
    try:
        artist_song_links = get_artist_song_links(artist)
    except:
        return "Sorry. No haiku or lyrics found."

    five_list = []
    seven_list = []

    for song_page in artist_song_links:
        lyrics = get_lyrics(song_page)
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
                    n += nsyl(word)                
                source = song_page

                #print line, n
                if n == 5:
                    five_list.append((line, n, source))
                if n == 7:
                    seven_list.append((line, n, source))
    
    
    if len(five_list) >= 2 and len(seven_list) >= 1:
        five_pick_one = random.randint(0,len(five_list)-1)
        five_pick_two = random.randint(0, len(five_list) - 1)
        while five_pick_two == five_pick_one:
            five_pick_two = random.randint(0, len(five_list) - 1)

        first_line = five_list[five_pick_one][0]
        second_line = seven_list[random.randint(0, len(seven_list) - 1)][0]
        third_line = five_list[five_pick_two][0]

        haiku = '\n'.join([first_line, second_line, third_line])
        return haiku
    return "Sorry. No haiku or lyrics found."