#!/usr/bin/python3

import os
import json
import random
import requests
import datetime
from bs4 import BeautifulSoup
from plyer import notification

'''
bibles = requests.get('https://api.scripture.api.bible/v1/bibles', headers=headers).json()['data']
for bible in bibles:
    print(bible)
'''
# copying requests
# curl -X GET --header "Accept: text/javascript" --header "api-key: $API_BIBLE_KEY" https://api.scripture.api.bible/v1/bibles | jq . > bibles.json
# curl -X GET "https://api.scripture.api.bible/v1/bibles/06125adad2d5898a-01/books" -H  "accept: application/json" -H  "api-key: $API_BIBLE_KEY" | jq . > books.json

file_path = "/home/jacwater/.cache/bible/daily.json"
current = json.load(open(file_path))

output = {
    "refresh_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
}

time_since_last_refresh = (datetime.datetime.now() - datetime.datetime.strptime(current['refresh_ts'], "%Y-%m-%d %H:%M:%S")).days

if current['date'] != output['date']:
    headers = {
        'content-type': 'application/json',
        'api-key': os.getenv('API_BIBLE_KEY'),
    }

    # get books
    bible_id = '06125adad2d5898a-01'
    books_url = 'https://api.scripture.api.bible/v1/bibles/%s/books' % (bible_id)
    books = requests.get(books_url, headers=headers).json()['data']

    # get random book index
    book_index = random.randint(0, len(books)-1)

    # get chapters
    chapters_url = 'https://api.scripture.api.bible/v1/bibles/%s/books/%s/chapters' % (bible_id, books[book_index]['id'])
    chapters = requests.get(chapters_url, headers=headers).json()['data']

    # random chapter index
    chapter_index = random.randint(0, len(chapters)-1)

    # get verses
    verses_url = 'https://api.scripture.api.bible/v1/bibles/%s/chapters/%s/verses' % (bible_id, chapters[chapter_index]['id'])
    verses = requests.get(verses_url, headers=headers).json()['data']

    # return all verses
    output['chapter'] = chapters[chapter_index]['reference']
    chapter_text = ''
    for i, verse in enumerate(verses):
        verses_url = 'https://api.scripture.api.bible/v1/bibles/%s/verses/%s' % (bible_id, verse['id'])
        content = requests.get(verses_url, headers=headers).json()['data']
        xml = BeautifulSoup(content['content'], 'xml')
        text = xml.get_text()
        if text is not None:
            verse_identifier = '[%s]' % (str(i+1))
            chapter_text = '%s %s' % (chapter_text, text.replace(str(i+1), verse_identifier))
    output['text'] = chapter_text

    # write new output to json and set message
    json.dump(output, open(file_path, 'w'), indent=4)
    bible_message = 'INFO: Updating Daily Bible Chapter - %s' % (output['chapter'])
else:
    # update timestamp of last poll and write update to json file
    current['refresh_ts'] = output['refresh_ts']
    current['date'] = output['date']
    json.dump(current, open(file_path, 'w'), indent=4)

    # set message
    bible_message = 'INFO: Bible Chapter is already up-to-date - %s' % (current['chapter'])

# send message to desktop
notification.notify(
    title='Bible Scripture Agent',
    message=bible_message,
    app_name='BibleScriptureAgent',
    timeout=360
)
