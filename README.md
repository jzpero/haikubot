# haikubot
Live on [Twitter](https://twitter.com/hai_cudi)

## What I Do:
Give me the name of an artist, and I'll try to come up with a random haiku using their lyrics.

### Algorithm:
- Search genius.com for the artist
- Scrape top songs links from that artist
- Scrape song pages for lyrics
- Process lyrics line by line:
    - Inclusion criteria: 5 or 7 syllables
    - Exclusion criteria: verse header
- Generate a random haiku


### Problems:
- Natural language processing is difficult, and the counting of syllables is very hard given the diversity of words in song lyrics. I used a combination of NLTK's corpus dictionary and textstat as a backup. Sometimes the syllable count is off.
- Does not store the lyrics locally, so is slowed down by the HTML requests
- Only handles requests via DMs right now, because I don't want the bot to be banned for returing haikus with profanity or other inappropriate words publically.

## Dependencies:
- tweepy for Twitter API handling
- textstat and NLTK for syllable processing
- BeautifulSoup4 for HTML parsing
- urllib2 for web requests

