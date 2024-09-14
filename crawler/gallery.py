import sys
import time
import requests
import os
import urllib.request as request
import json


def download(index: int, url: str, name: str, file_name: str):
    """
        download content in url
    """
    response = requests.get(url)
    suffix = ''
    if "preview.redd.it" in url:
        pos1 = url.find("?")
        pos2 = pos1-1
        while url[pos2] != '.':
            pos2 -= 1
        suffix = url[pos2:pos1]
    else:
        for i in range(len(url) - 1, 0, -1):
            if url[i] == '.':
                suffix = url[i:]
                break
    os.makedirs('pic_result/' + file_name + '/' + str(index), exist_ok=True)
    with open('pic_result/' + file_name + '/' + str(index) + '/' + name + suffix, 'wb') as f:
        f.write(response.content)


def gallery_manage(index: int, url: str, file_name: str, num: int):
    """
        download thing in gallery
    """
    gallery_data = []
    for _ in range(5):
        try:
            gallery_page = request.urlopen(url)
            gallery_data = json.load(gallery_page)
            break
        except:
            time.sleep(2)
    if not gallery_data:
        return num
    gallery_info = gallery_data[0].get('data', {}).get('children', None)
    os.makedirs('pic_result/' + file_name + '/' + str(index), exist_ok=True)
    for info in gallery_info:
        if "media_metadata" not in info['data']:
            return num
        pic_dict = info['data']["media_metadata"]
        if not pic_dict:
            return num
        for pic in pic_dict.values():
            if 'u' not in pic['s']: break
            raw_url = pic['s']['u'].replace('amp;', '')
            suffix = ''
            response = requests.get(raw_url)
            for i in range(len(raw_url) - 1, 0, -1):
                if raw_url[i] == '?':
                    j = i - 1
                    while raw_url[j] != '.':
                        j -= 1
                    suffix = raw_url[j:i]  # with .
                    break
            with open('pic_result/' + file_name + '/' + str(index) + '/' + str(num) + suffix, 'wb') as f:
                f.write(response.content)
            num += 1
    return num


def main():
    os.makedirs('../pic_result', exist_ok=True)
    file_name = sys.argv[1]
    linkdir_path = '../link_result/'
    os.makedirs('pic_result/' + file_name, exist_ok=True)
    with open(linkdir_path + file_name, 'r') as file:
        links = file.readlines()
    links = [link.strip() for link in links]
    for idx, link in enumerate(links):
        # gfycat is ignored, it provides gif
        if 'i.imgur.com' in link or 'i.redd.it' in link or 'redgifs.com' in link or "preview.redd.it" in link:
            download(idx, link, '1', file_name)
        elif 'www.reddit.com/gallery/' in link:
            gallery_name = ''
            for i in range(len(link) - 1, 0, -1):
                if link[i] == '/':
                    gallery_name = link[i + 1:]
                    break
            url_g = 'https://www.reddit.com/comments/' + gallery_name + '.json'
            gallery_manage(idx, url_g, file_name, 1)


if __name__ == "__main__":
    main()
