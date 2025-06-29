import os
import json
import random
import requests
import datetime
from bs4 import BeautifulSoup
'''
bibles = requests.get('https://api.scripture.api.bible/v1/bibles', headers=headers).json()['data']
for bible in bibles:
    print(bible)
'''
# copying requests
# curl -X GET --header "Accept: text/javascript" --header "api-key: $API_BIBLE_KEY" https://api.scripture.api.bible/v1/bibles | jq . > bibles.json
# curl -X GET "https://api.scripture.api.bible/v1/bibles/06125adad2d5898a-01/books" -H  "accept: application/json" -H  "api-key: $API_BIBLE_KEY" | jq . > books.json

output = {
    "refresh_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
}
file_path = "/home/jacwater/.cache/bible/%s.json" % (output['date'])

if os.path.exists(file_path):
    # file already exists for the day then by pass
    pass
else:
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

    # create json file
    with open(file_path, 'w') as f:
        # Write the data to the file
        json.dump(output, f, indent=4)

    print(output['text'])
