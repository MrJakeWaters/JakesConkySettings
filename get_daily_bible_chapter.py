#!/usr/bin/python3

import os
import json
import random
import requests
import datetime
from bs4 import BeautifulSoup
from plyer import notification

#curl -X GET https://api.biblesupersearch.com/api/books
file_path = "/home/jacwater/.cache/bible/daily.json"
current = json.load(open(file_path))

output = {
    "refresh_ts": datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
}

if current['date'] != output['date']:
    # get books
    books_url = 'https://api.biblesupersearch.com/api/books'
    books = requests.get(books_url).json()['results']

    # get random book
    book_index = random.randint(0, len(books)-1)
    book = books[book_index]

    # get random chapter
    chapter = random.randint(1, book['chapters'])
    bible_chapter = '%s %s' % (book['shortname'], str(chapter))

    # get verses object
    verse_url = 'https://api.biblesupersearch.com/api?bible=asvs&reference=%s' % (bible_chapter)
    verses = requests.get(verse_url).json()['results'][0]

    # grab indices to properly loop through output object
    # weirdness in the way the object is returned, maybe a cleaner way to do this but whatever
    chapter_verse = verses['chapter_verse']
    verse_indices = verses['verse_index'][chapter_verse] # array that stores keys to verses for chapter
    verse_objects = verses['verses']['asvs'][chapter_verse] # object that stores verses
    text = ''
    for i in verse_indices:
        text = '%s  %s' % (text, verse_objects[str(i)]['text'])

    # set output values to write to hd
    output['chapter'] = bible_chapter
    output['text'] = text
    json.dump(output, open(file_path, 'w'), indent=4)
    print('Bible Chapter updated: %s' % (output['chapter']))
else:
    current['refresh_ts'] = output['refresh_ts']
    json.dump(current, open(file_path, 'w'), indent=4)
    print('Bible Chapter is up-to-date')
