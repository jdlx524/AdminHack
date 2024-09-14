import csv
import html
import re

import requests
import time
import json

maxThings = -1
printWait = 2
requestSize = 100
totalResults = 20000
text_file = "../all_crawl/text1.csv"
link_file = "../all_crawl/links1"
id_dic = {}
now_id = 1

def requestJSON(url):
    while True:
        try:
            r = requests.get(url)
            if r.status_code != 200:
                print('error code', r.status_code)
                time.sleep(5)
                continue
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    return r.json()

requestWait = 0.5

thing = 'submission'

i = 0
with open(text_file, 'w', newline='') as file1, open(link_file, 'w') as file2:
    writer = csv.writer(file1)
    writer.writerow(['ID', 'Tag', 'Title', 'Content'])
    created_utc = ''
    json1 = []
    with open("../computerscience_submissions/computerscience_submissions", 'r') as file:
        for idx, line in enumerate(file):
            json_obj = json.loads(line.strip())
            json1.append(json_obj)

    doneHere = False
    for post in json1:
        title = post['title']
        content = post['selftext']
        if "Study abroad programs" in title:
            print(title)
        tag = ''
        if title+content in id_dic or content in ["[removed]", "[deleted]"]:
            continue
        id_dic[title+content] = now_id
        now_id += 1
        text = html.unescape(content)
        urls = re.findall(r'(?:https?:\/\/)?(?:[\w\-]+\.)+[a-zA-Z]{2,3}(?:\/[\w\-.\/?%&=;]*)?', text)  # find url in content words
        urls.append(post.get("url_overridden_by_dest", ''))  # find url in normal link form
        # id and urls: seperated by white space
        if post['link_flair_text']:
            tag = post.get('link_flair_text')
        else:
            tag = 'None'
        created_utc = post["created_utc"]
        writer.writerow([now_id-1, tag, title, content])
        file2.write(str(now_id-1)+' ')
        for url in urls:
            if url: file2.write(url+' ')
        file2.write('\n')
